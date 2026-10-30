#!/usr/bin/env python3
"""Generate the static firmware site from this repo's releases and an upstream checkout."""
import argparse
import html
import json
import os
import re
import shutil
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

UPSTREAM = "logicog/RTLPlayground"
SITE = "RTL Playground Nightly Builds"
RETAIN = 14  # dated nightlies kept by nightly.yml (KEEP_NIGHTLIES)
ASSET_RE = re.compile(r"^rtlplayground-(.+)-(\d{8})-(.+?)(-oem_upgrade)?\.bin$")
TAG_RE = re.compile(r"^nightly-(\d{8})-([0-9a-f]+)$")
SHA_RE = re.compile(r"\b[0-9a-f]{40}\b")
e = html.escape


def parse_asset(name):
    m = ASSET_RE.match(name)
    return (m.group(3), "oem" if m.group(4) else "custom") if m else None


def load_machines(upstream):
    mdir = upstream / "machine"
    names = sorted({p.stem for p in mdir.glob("*.h")} & {p.stem for p in mdir.glob("*.c") if not p.stem.endswith("_init")})
    machines = {}
    for n in names:
        h = (mdir / f"{n}.h").read_text(errors="replace")
        model = re.search(r'#define\s+MACHINE_MODEL\s+"([^"]+)"', h)
        chip = re.search(r"#define\s+MACHINE_CHIPSET\s+(\w+)", h)
        files = set()
        for f in (f"{n}.c", f"{n}.h", f"{n}_init.c"):
            p = mdir / f
            if p.exists():
                files.add(f"machine/{f}")
                files.add(os.path.relpath(p.resolve(), upstream.resolve()))
        machines[n] = {"model": model.group(1) if model else n, "chip": chip.group(1) if chip else "", "files": files}
    for n, m in machines.items():
        m["twins"] = [k for k, o in machines.items() if k != n and o["model"] == m["model"]]
    return machines


def load_nightlies(releases):
    out = []
    for r in releases:
        m = TAG_RE.match(r["tag_name"])
        if not m:
            continue
        sha = SHA_RE.search(r.get("body") or "")
        n = {"tag": r["tag_name"], "url": r["html_url"], "date": datetime.strptime(m.group(1), "%Y%m%d"),
             "sha": sha.group(0) if sha else m.group(2), "files": {}, "sums": None,
             "failed": set(re.findall(r"^- (\S+)$", r.get("body") or "", re.M))}
        for a in r["assets"]:
            if a["name"] == "SHA256SUMS":
                n["sums"] = a["browser_download_url"]
            elif p := parse_asset(a["name"]):
                n["files"].setdefault(p[0], {})[p[1]] = a
        out.append(n)
    return sorted(out, key=lambda n: (n["date"], n["tag"]), reverse=True)


def commits_between(upstream, old, new):
    """Commits in old..new as (sha, subject, changed paths); None when unknown."""
    if not old:
        return None
    if old == new:
        return []
    try:
        log = subprocess.run(["git", "-C", str(upstream), "log", "--format=%x1e%H%x1f%s", "--name-only", f"{old}..{new}"],
                             check=True, capture_output=True, text=True).stdout
    except subprocess.CalledProcessError:
        return None
    commits = []
    for chunk in log.split("\x1e")[1:]:
        head, _, paths = chunk.partition("\n")
        sha, _, subject = head.partition("\x1f")
        commits.append((sha, subject, set(filter(None, paths.split("\n")))))
    return commits


def fmt(d, year=False):
    return d.strftime("%-d %b %Y" if year else "%-d %b")


def size(a):
    return f"{a['size'] // 1024} KiB"


def icon(paths, size=16):
    return (f'<svg class="i" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths}</svg>')


EXT = icon('<path d="M7 17 17 7M8 7h9v9"/>', 14)
SEARCH = icon('<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>', 18)
CHEVRON = icon('<path d="m9 6 6 6-6 6"/>')
BACK = icon('<path d="m15 6-6 6 6 6"/>')
DOWNLOAD = icon('<path d="M12 4v11m0 0-4-4m4 4 4-4M5 20h14"/>')
STAR = icon('<path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1-5.4-2.9-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/>', 18)
WARN = icon('<path d="M12 3 2 20h20zM12 10v4M12 17v.5"/>', 18)
LOGO = ('<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
        '<rect x="2" y="7" width="20" height="10" rx="2"/><path d="M6 11v2M10 11v2M14 11v2M18 11v2"/></svg>')


def page(title, root, body, current, script=""):
    repo = os.environ.get("GITHUB_REPOSITORY", "mintopia/rtl-playground-nightly-builds")
    nav = "".join(f'<a href="{e(u)}"{" aria-current=page" if t == current else ""}>{t}</a>'
                  for t, u in (("Switches", root or "./"), ("Build matrix", f"{root}matrix/")))
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="dark">
<title>{e(title if title == SITE else f"{title} – {SITE}")}</title><link rel="stylesheet" href="{root}style.css"></head>
<body><a class="skip" href="#main">Skip to content</a>
<header class="bar"><div class="bar-in"><a class="brand" href="{root or './'}" aria-label="RTL Playground Nightly, home">{LOGO}<span>RTL Playground <span class="brand-sub">Nightly Builds</span></span></a>
<nav aria-label="Site">{nav}<a href="https://github.com/{UPSTREAM}">GitHub{EXT}</a></nav></div></header>
<main id="main">{body}</main>
<footer class="foot"><div class="foot-in"><p>Unofficial nightly builds of <a href="https://github.com/{UPSTREAM}">{UPSTREAM}</a></p>
<a href="https://github.com/{e(repo)}/releases">All releases</a></div></footer>
{f"<script>{script}</script>" if script else ""}
</body></html>"""


def breakable(s):
    return e(s).replace("-", "-<wbr>").replace("_", "_<wbr>")


def sha_link(sha):
    return f'<a class="sha" href="https://github.com/{UPSTREAM}/commit/{sha}">{sha[:7]}</a>'


def commit_items(commits, machine):
    return "".join(f'<li>{sha_link(sha)}<span>{e(subject)}</span>{"<span class=tag>This board</span>" if machine and paths & machine["files"] else ""}</li>'
                   for sha, subject, paths in commits)


def commit_list(commits, machine=None, cap=None):
    if commits is None:
        return '<p class="mut">Earlier history not available.</p>'
    if not commits:
        return '<p class="mut">No upstream changes since the previous nightly.</p>'
    if machine:
        commits = sorted(commits, key=lambda c: not (c[2] & machine["files"]))
    head, rest = (commits[:cap], commits[cap:]) if cap else (commits, [])
    more = f'<details class="more"><summary>Show {len(rest)} more</summary><ul class="commits">{commit_items(rest, machine)}</ul></details>' if rest else ""
    return f'<ul class="commits">{commit_items(head, machine)}</ul>{more}'


def plural(n, word, many=None):
    return f"{n} {word if n == 1 else many or word + 's'}"


def strip(stops, legend):
    """Last RETAIN days ending at the newest nightly. stops: (date, state, href, label), newest first."""
    by_day = {}
    for d, state, href, label in stops:
        by_day.setdefault(d.date(), (state, href, label))
    end = stops[0][0]
    cells = []
    for i in range(RETAIN):
        day = (end - timedelta(days=i))
        state, href, label = by_day.get(day.date(), ("gap", None, f"{fmt(day)}: no nightly"))
        attrs = f'class="cell {state}" aria-label="{e(label)}" title="{e(label)}"'
        cells.append(f'<li><a href="{e(href)}" {attrs}></a></li>' if href else f'<li><span role="img" {attrs}></span></li>')
    keys = "".join(f'<span><i class="cell {k}"></i>{t}</span>' for k, t in legend + [("gap", "No nightly")])
    return (f'<div class="history-strip"><ol class="strip" style="--n:{RETAIN}">{"".join(cells)}</ol>'
            f'<div class="strip-foot"><span>{fmt(end)}</span><span>{fmt(end - timedelta(days=RETAIN - 1))}</span></div><p class="keys">{keys}</p></div>')


def search_key(*parts):
    return re.sub(r"[^a-z0-9]", "", " ".join(parts).lower())


def by_model(machines):
    return sorted(machines.items(), key=lambda kv: (kv[1]["model"].lower(), kv[0]))


FAV_JS = """const FK='rtlp-favourites';function favs(){try{const f=JSON.parse(localStorage.getItem(FK));return Array.isArray(f)?f:[]}catch{return[]}}
function toggleFav(id){const f=favs(),i=f.indexOf(id);i<0?f.push(id):f.splice(i,1);try{localStorage.setItem(FK,JSON.stringify(f))}catch{}}
function markFavs(){const f=favs();for(const b of document.querySelectorAll('.fav')){const on=f.includes(b.dataset.id);b.setAttribute('aria-pressed',on);
b.setAttribute('aria-label',`${on?'Remove':'Add'} ${b.dataset.name} ${on?'from':'to'} favourites`);const t=b.querySelector('.fav-text');if(t)t.textContent=on?'Favourite':'Add to favourites'}}
"""

FILTER_JS = FAV_JS + """const k=s=>s.toLowerCase().replace(/[^a-z0-9]/g,''),q=document.getElementById('q'),all=[...document.querySelectorAll('#models li')],count=document.getElementById('count'),none=document.getElementById('none'),
favUl=document.getElementById('favlist'),favSec=document.getElementById('favs'),allHead=document.getElementById('all-head');
function renderFavs(){favUl.replaceChildren(...favs().map(id=>all.find(r=>r.dataset.id===id)).filter(Boolean).map(r=>r.cloneNode(true)));markFavs();run()}
function run(){const t=k(q.value);let n=0;for(const r of [...all,...favUl.children]){const s=!t||r.dataset.q.includes(t);r.hidden=!s;if(all.includes(r))n+=s}
favSec.hidden=![...favUl.children].some(r=>!r.hidden);allHead.hidden=favSec.hidden;
count.textContent=t?`${n} of ${all.length} switches`:'';none.hidden=n>0;history.replaceState(null,'',q.value?'?q='+encodeURIComponent(q.value):location.pathname)}
addEventListener('click',ev=>{const b=ev.target.closest('.fav');if(!b)return;const inFav=favUl.contains(b),id=b.dataset.id;toggleFav(id);renderFavs();
if(inFav)(favUl.querySelector(`.fav[data-id="${CSS.escape(id)}"]`)||all.find(r=>r.dataset.id===id).querySelector('.fav')).focus()});
q.addEventListener('input',run);const p=new URLSearchParams(location.search).get('q');if(p){q.value=p;run()}
addEventListener('keydown',ev=>{if(ev.key==='/'&&document.activeElement!==q){ev.preventDefault();q.focus()}});
renderFavs();"""

MODEL_JS = FAV_JS + """document.documentElement.classList.add('js');
for(const b of document.querySelectorAll('.expand'))b.addEventListener('click',()=>{const o=b.getAttribute('aria-expanded')!=='true';
b.setAttribute('aria-expanded',o);document.getElementById(b.getAttribute('aria-controls')).classList.toggle('open',o)});
markFavs();document.querySelector('.fav').addEventListener('click',ev=>{toggleFav(ev.currentTarget.dataset.id);markFavs()});
"""

COPY_JS = """for(const b of document.querySelectorAll('.copy'))b.addEventListener('click',async()=>{
try{await navigator.clipboard.writeText(b.dataset.copy);b.textContent='Copied'}catch{b.textContent='Copy failed'}setTimeout(()=>b.textContent='Copy',2000)});"""

NO_NIGHTLY = "No nightly builds yet. The first one runs at 02:00 UTC."


def block(title, desc, body):
    return (f'<section class="block"><div class="block-label"><h2>{title}</h2>{f"<p>{desc}</p>" if desc else ""}</div>'
            f'<div class="block-body">{body}</div></section>')


def state(kind, text):
    return f'<span class="state {kind}"><i></i>{text}</span>'


def fav_button(name, m, text=False):
    label = '<span class="fav-text">Add to favourites</span>' if text else ""
    return (f'<button type="button" class="fav{" fav-lg" if text else ""}" data-id="{e(name)}" data-name="{e(m["model"])} ({e(name)})" aria-pressed="false" '
            f'aria-label="Add {e(m["model"])} ({e(name)}) to favourites">{STAR}{label}</button>')


def build_index(machines, nightlies):
    latest = nightlies[0] if nightlies else None
    if latest:
        built = sum(1 for m in machines if m in latest["files"])
        status = (f'Last built <a href="{e(latest["url"])}">{fmt(latest["date"], True)}</a> from upstream {sha_link(latest["sha"])}. '
                  f'{built} of {len(machines)} switches built.')
        stops = []
        for n in nightlies:
            ok, fail = sum(1 for x in machines if x in n["files"]), len(n["failed"])
            st = "ok" if not fail else ("partial" if ok else "fail")
            stops.append((n["date"], st, n["url"], f'{fmt(n["date"])}: {ok} of {ok + fail} built'))
        board = (f'<div class="hero-strip"><h2>Last {RETAIN} days</h2>' +
                 strip(stops, [("ok", "All built"), ("partial", "Some failed"), ("fail", "All failed")]) + '</div>')
    else:
        status, board = NO_NIGHTLY, ""
    rows = []
    for name, m in by_model(machines):
        good = next((n for n in nightlies if name in n["files"]), None)
        if not nightlies:
            st = state("none", "Not built yet")
        elif not good:
            st = state("fail", "No build")
        elif good is latest:
            st = state("ok", fmt(good["date"]))
        else:
            st = state("fail", f'Failed, using {fmt(good["date"])}')
        twin = f'<span class="tag warn" title="Same model name as {e(", ".join(m["twins"]))}">Check board</span>' if m["twins"] else ""
        rows.append(f'<li data-id="{e(name)}" data-q="{search_key(m["model"], name, m["chip"])}"><a href="m/{e(name)}/"><span class="row-main"><span class="name">{e(m["model"])}</span>{twin}'
                    f'<span class="row-sub"><code>{breakable(name)}</code>{e(m["chip"])}</span></span>{st}{CHEVRON}</a>{fav_button(name, m)}</li>')
    body = f"""<section class="hero"><h1>{SITE}</h1>
<p class="lede">Unofficial builds for {len(machines)} Realtek RTL8372 and RTL8373 switches. Find yours by the name on the box or the code printed on the board.</p>
<label class="search">{SEARCH}<span class="vh">Find your switch</span><input id="q" type="search" placeholder="Model, board code or chipset" autocomplete="off" aria-keyshortcuts="/"><kbd aria-hidden="true">/</kbd></label>
<p class="status">{status} <span id="count" aria-live="polite"></span></p>{board}</section>
<section id="favs" class="favs" hidden><h2>Favourites</h2><ul class="list" id="favlist"></ul></section>
<h2 id="all-head" class="list-head" hidden>All switches</h2>
<ul class="list" id="models">{''.join(rows)}</ul>
<p class="empty" id="none" hidden>No switch matches. Try the code printed on the board, or the chipset, for example RTL8373.</p>"""
    return page(SITE, "", body, "Switches", script=FILTER_JS)


def anchor(n):
    return f'n-{n["tag"]}'


def build_model(name, m, nightlies, changes):
    latest = nightlies[0] if nightlies else None
    good = next((n for n in nightlies if name in n["files"]), None)
    twins = ", ".join(f'<a href="../{e(t)}/"><code>{e(t)}</code></a>' for t in m["twins"])
    notes = f'{twins} {"has" if len(m["twins"]) == 1 else "have"} the same model name. ' if twins else ""
    chip = f', {e(m["chip"])}' if m["chip"] else ""
    built = f'<p class="built">Built {fmt(good["date"], True)} from upstream {sha_link(good["sha"])}</p>' if good else ""

    def head(extra=""):
        return (f'<a class="back" href="../../">{BACK}All switches</a><header class="head"><div class="title-row"><h1>{e(m["model"])}</h1>{fav_button(name, m, True)}</div>'
                f'<p class="lede">Board <code class="board">{e(name)}</code>{chip}.</p>'
                f'<p class="brick">{WARN}<span>{notes}Check <code>{e(name)}</code> matches the code printed on your switch\'s board before flashing. Another board\'s image can brick it. '
                f'<a href="https://github.com/{UPSTREAM}/blob/main/doc/supported_devices.md">Not sure? See the supported devices list</a></span></p>'
                f'{built}{extra}</header>')
    about = block("About this board", "Where this build's board definition comes from upstream.",
                  f'<dl class="kv panel"><dt>Definition</dt><dd><a href="https://github.com/{UPSTREAM}/blob/main/machine/{e(name)}.c"><code>machine/{e(name)}.c</code></a></dd>'
                  f'<dt>Devices</dt><dd><a href="https://github.com/{UPSTREAM}/blob/main/doc/supported_devices.md">Supported devices list</a></dd></dl>')
    if not good:
        msg = "No successful build in the last 14 days." if nightlies else NO_NIGHTLY
        return page(m["model"], "../../", head() + f'<p class="empty panel">{msg}</p>' + about, "", script=MODEL_JS)
    failed = f'<p class="note">The {fmt(latest["date"])} nightly failed for this switch. These are the {fmt(good["date"])} files.</p>' if good is not latest else ""
    f = good["files"][name]
    uses = [("oem", "OEM upgrade", "Managed switch, still on vendor firmware",
             "Upload this once through the switch's original web interface to move it to RTL Playground."),
            ("custom", "Custom", "Already on RTL Playground, or any unmanaged switch",
             "Upload this through RTL Playground's web interface. On an unmanaged switch, write it to the flash chip with a SOIC-8 clip.")]
    picks = []
    for key, label, when, use in uses:
        a = f.get(key)
        if a:
            digest = (a.get("digest") or "").removeprefix("sha256:")
            hash_row = (f'<div class="hash"><div class="hash-head"><span>SHA-256</span><button type="button" class="copy" data-copy="{digest}" '
                        f'aria-label="Copy SHA-256 of {label}">Copy</button></div><code>{digest}</code></div>') if digest else ""
            dl = (f'<a class="btn" href="{e(a["browser_download_url"])}">{DOWNLOAD}Download {label}<span class="size">{size(a)}</span></a>'
                  f'<p class="fname"><code>{breakable(a["name"])}</code></p>{hash_row}')
        else:
            dl = '<p class="mut">Not built this night.</p>'
        picks.append(f'<section class="pick"><h2>{when}</h2><p class="use">{use}</p><p class="for">For board <code>{e(name)}</code> only</p>{dl}</section>')
    links = [f'<a href="https://github.com/{UPSTREAM}#readme">Flashing instructions</a>',
             f'<a href="{e(good["sums"])}">SHA256SUMS</a>' if good["sums"] else ""]
    dls = block("Download", "Pick the file for the firmware your switch runs now."
                f'<span class="links">{"".join(x for x in links if x)}</span>', f'<div class="picks">{"".join(picks)}</div>')
    log = block("Changes in this build", "Upstream commits since the previous nightly. Ones touching this board come first."
                f'<span class="links"><a href="https://github.com/{UPSTREAM}/blob/main/CHANGELOG.md">Upstream changelog</a></span>',
                f'<div class="panel">{commit_list(changes[good["tag"]], m, cap=8)}</div>')

    def st(n):
        return "ok" if name in n["files"] else "fail" if name in n["failed"] else "none"
    word = {"ok": "built", "fail": "failed", "none": "not in this nightly"}
    hist = []
    for n in nightlies:
        nf = n["files"].get(name)
        c = changes[n["tag"]]
        when = fmt(n["date"], True)
        extra = ""
        if c:
            cid = f'c-{n["tag"]}'
            detail = (f'<button type="button" class="expand" aria-expanded="false" aria-controls="{cid}">{plural(len(c), "commit")}{CHEVRON}</button>')
            extra = f'<tr class="changes-row" id="{cid}"><td colspan="5">{commit_list(c, m)}</td></tr>'
        else:
            detail = '<span class="mut">None</span>' if c == [] else '<span class="mut">Earliest kept</span>'
        if nf:
            def link(k, label):
                a = nf.get(k)
                return f'<a href="{e(a["browser_download_url"])}" aria-label="{label}, {when}">{label}</a>' if a else '<span class="mut">Not built</span>'
            files = f'<td>{link("oem", "OEM")}</td><td>{link("custom", "Custom")}</td>'
        elif name in n["failed"]:
            files = f'<td colspan="2">{state("fail", "Failed")}</td>'
        else:
            files = '<td colspan="2"><span class="mut">Not included</span></td>'
        same_day = sum(1 for x in nightlies if x["date"] == n["date"]) > 1
        hist.append(f'<tr id="{anchor(n)}"><td class="date">{when}{f"<span class=sub>{sha_link(n["sha"])}</span>" if same_day else ""}</td><td class="up">{sha_link(n["sha"])}</td>{files}<td>{detail}</td></tr>{extra}')
    history = block("Build history", f"The last {RETAIN} days. Select a day to jump to its files.",
               strip([(n["date"], st(n), f'#{anchor(n)}', f'{fmt(n["date"])}: {word[st(n)]}') for n in nightlies],
                       [("ok", "Built"), ("fail", "Failed"), ("none", "Not included")])
               + f'<div class="table-wrap"><table class="t"><caption class="vh">Nightly builds for {e(m["model"])}</caption>'
               f'<thead><tr><th scope="col">Nightly</th><th scope="col" class="up">Upstream</th><th scope="col">OEM</th><th scope="col">Custom</th>'
               f'<th scope="col">Changes</th></tr></thead><tbody>{"".join(hist)}</tbody></table></div>')
    return page(m["model"], "../../", head(failed) + dls + log + history + about, "", script=MODEL_JS + COPY_JS)


def latest_per_day(nightlies):
    seen = set()
    return [n for n in nightlies if not (n["date"] in seen or seen.add(n["date"]))]


def build_matrix(machines, nightlies):
    nightlies = latest_per_day(nightlies)
    head = '<header class="head"><h1>Build matrix</h1>'
    if not nightlies:
        return page("Build matrix", "../", head + f'</header><p class="empty panel">{NO_NIGHTLY}</p>', "Build matrix")
    by_day = {n["date"]: n for n in nightlies}
    end = nightlies[0]["date"]
    days = [end - timedelta(days=i) for i in range(RETAIN)]
    cols = "".join(f'<th scope="col"><a href="{e(by_day[d]["url"])}">{d.day}<span>{d:%b}</span></a></th>' if d in by_day
                   else f'<th scope="col" class="gapcol">{d.day}<span>{d:%b}</span></th>' for d in days)
    rows = []
    for name, m in by_model(machines):
        cells = []
        for d in days:
            n = by_day.get(d)
            st = "gap" if not n else "ok" if name in n["files"] else "fail" if name in n["failed"] else "none"
            label = f'{fmt(d)}: {({"gap": "no nightly", "ok": "built", "fail": "failed", "none": "not included"})[st]}'
            dot = f'class="dot {st}" title="{label}"'
            cells.append(f'<td><a href="../m/{e(name)}/#{anchor(n)}" {dot} aria-label="{e(m["model"])}, {label}"></a></td>' if st == "ok"
                         else f'<td><span role="img" {dot} aria-label="{label}"></span></td>')
        rows.append(f'<tr><th scope="row"><a href="../m/{e(name)}/"><span class="name">{e(m["model"])}</span><code>{breakable(name)}</code></a></th>{"".join(cells)}</tr>')
    keys = "".join(f'<span><i class="dot {k}"></i>{t}</span>' for k, t in (("ok", "Built"), ("fail", "Failed"), ("none", "Not included"), ("gap", "No nightly")))
    body = ('<div class="matrix-page">' + head + f'<p class="lede">Every switch over the last {RETAIN} days, newest first. Select a green dot to get that night\'s files.</p>'
            f'<p class="keys">{keys}</p></header>'
            f'<div class="table-wrap matrix-wrap"><table class="t matrix"><caption class="vh">Builds per switch and night</caption>'
            f'<thead><tr><th scope="col">Switch</th>{cols}</tr></thead><tbody>{"".join(rows)}</tbody></table></div></div>')
    return page("Build matrix", "../", body, "Build matrix")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--upstream", type=Path, required=True)
    ap.add_argument("--releases", type=Path, required=True, help="JSON from the GitHub releases API")
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    machines = load_machines(a.upstream)
    nightlies = load_nightlies(json.loads(a.releases.read_text()))
    changes = {n["tag"]: commits_between(a.upstream, nightlies[i + 1]["sha"] if i + 1 < len(nightlies) else None, n["sha"])
               for i, n in enumerate(nightlies)}
    shutil.rmtree(a.out, ignore_errors=True)
    (a.out / "matrix").mkdir(parents=True)
    shutil.copy(Path(__file__).with_name("style.css"), a.out / "style.css")
    (a.out / "index.html").write_text(build_index(machines, nightlies))
    (a.out / "matrix" / "index.html").write_text(build_matrix(machines, nightlies))
    for name, m in machines.items():
        d = a.out / "m" / name
        d.mkdir(parents=True)
        (d / "index.html").write_text(build_model(name, m, nightlies, changes))
    print(f"{len(machines)} switches, {len(nightlies)} nightlies -> {a.out}")


if __name__ == "__main__":
    main()
