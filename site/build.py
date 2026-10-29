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


def page(title, root, body, current, wide=False, script=""):
    nav = [("Models", f"{root}"), ("Matrix", f"{root}matrix/"), ("Releases", f"https://github.com/{os.environ.get('GITHUB_REPOSITORY', 'mintopia/rtl-playground-nightly-builds')}/releases"),
           ("Upstream", f"https://github.com/{UPSTREAM}")]
    links = "".join(f'<a href="{e(u)}"{" aria-current=page" if t == current else ""}>{t}</a>' for t, u in nav)
    w = " wide" if wide else ""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title if title == SITE else f"{title} – {SITE}")}</title><link rel="stylesheet" href="{root}style.css"></head>
<body><a class="skip" href="#main">Skip to content</a>
<header class="band"><div class="wrap{w}"><a class="name" href="{root}">{SITE}</a><nav aria-label="Site">{links}</nav></div></header>
<main id="main" class="wrap{w}">{body}</main>
<footer class="wrap{w}">Unofficial nightly builds of <a href="https://github.com/{UPSTREAM}">{UPSTREAM}</a>. Check the model and board match your switch before flashing.</footer>
{f"<script>{script}</script>" if script else ""}
</body></html>"""


def badge(text, kind):
    return f'<span class="badge {kind}">{text}</span>'


def breakable(s):
    return e(s).replace("-", "-<wbr>").replace("_", "_<wbr>")


def sha_link(sha):
    return f'<a class="sha" href="https://github.com/{UPSTREAM}/commit/{sha}">{sha[:7]}</a>'


def commit_items(commits, machine):
    return "".join(f'<li>{sha_link(sha)} <span>{e(subject)}</span>{badge("this model", "mine") if machine and paths & machine["files"] else ""}</li>'
                   for sha, subject, paths in commits)


def commit_list(commits, machine=None, cap=None):
    if commits is None:
        return '<p class="quiet">Earlier history not available.</p>'
    if not commits:
        return '<p class="quiet">No upstream changes since the previous nightly.</p>'
    if machine:
        commits = sorted(commits, key=lambda c: not (c[2] & machine["files"]))
    head, rest = (commits[:cap], commits[cap:]) if cap else (commits, [])
    more = f'<details class="more"><summary>Show {len(rest)} more</summary><ul class="commits">{commit_items(rest, machine)}</ul></details>' if rest else ""
    return f'<ul class="commits">{commit_items(head, machine)}</ul>{more}'


def plural(n, word, many=None):
    return f"{n} {word if n == 1 else many or word + 's'}"


def chip(c):
    return f'<span class="chip chip-{e(c[-4:])}">{e(c)}</span>' if c else ""


def strip(stops, legend):
    """Last RETAIN days ending at the newest nightly. stops: (date, state, href, label), newest first."""
    by_day = {}
    for d, state, href, label in stops:
        by_day.setdefault(d.date(), (state, href, label))
    end = stops[0][0]
    cells = []
    for i in range(RETAIN - 1, -1, -1):
        day = (end - timedelta(days=i))
        state, href, label = by_day.get(day.date(), ("gap", None, f"{fmt(day)}: no nightly"))
        attrs = f'class="cell {state}" aria-label="{e(label)}" title="{e(label)}"'
        cells.append(f'<li><a href="{e(href)}" {attrs}></a></li>' if href else f'<li><span role="img" {attrs}></span></li>')
    keys = "".join(f'<span><i class="cell {k}"></i>{t}</span>' for k, t in legend + [("gap", "No nightly")])
    return (f'<div class="history-strip"><ol class="strip" style="--n:{RETAIN}">{"".join(cells)}</ol>'
            f'<div class="strip-foot"><span>{fmt(end - timedelta(days=RETAIN - 1))}</span><span>{fmt(end)}</span></div><p class="keys">{keys}</p></div>')


def search_key(*parts):
    return re.sub(r"[^a-z0-9]", "", " ".join(parts).lower())


def by_model(machines):
    return sorted(machines.items(), key=lambda kv: (kv[1]["model"].lower(), kv[0]))


FILTER_JS = """const k=s=>s.toLowerCase().replace(/[^a-z0-9]/g,''),q=document.getElementById('q'),rows=[...document.querySelectorAll('#models tbody tr')],count=document.getElementById('count'),none=document.getElementById('none');
function run(){const t=k(q.value);let n=0;for(const r of rows){const s=!t||r.dataset.q.includes(t);r.hidden=!s;n+=s}
count.textContent=t?`${n} of ${rows.length} switches`:'';none.hidden=n>0;history.replaceState(null,'',q.value?'?q='+encodeURIComponent(q.value):location.pathname)}
q.addEventListener('input',run);const p=new URLSearchParams(location.search).get('q');if(p){q.value=p;run()}
addEventListener('keydown',ev=>{if(ev.key==='/'&&document.activeElement!==q){ev.preventDefault();q.focus()}});"""

COPY_JS = """for(const b of document.querySelectorAll('.copy'))b.addEventListener('click',async()=>{
try{await navigator.clipboard.writeText(b.dataset.copy);b.textContent='Copied'}catch{b.textContent='Copy failed'}setTimeout(()=>b.textContent='Copy',2000)});"""


def build_index(machines, nightlies):
    latest = nightlies[0] if nightlies else None
    if latest:
        built = sum(1 for m in machines if m in latest["files"])
        summary = (f'<p class="summary">Last nightly <a href="{e(latest["url"])}">{fmt(latest["date"], True)}</a> from upstream {sha_link(latest["sha"])}. '
                   f'{built} of {len(machines)} switches built.</p>')
        stops = []
        for n in nightlies:
            ok, fail = sum(1 for x in machines if x in n["files"]), len(n["failed"])
            state = "ok" if not fail else ("partial" if ok else "fail")
            stops.append((n["date"], state, n["url"], f'{fmt(n["date"])}: {ok} of {ok + fail} built'))
        board = strip(stops, [("ok", "All built"), ("partial", "Some failed"), ("fail", "All failed")])
    else:
        summary, board = '<p class="summary">No nightly builds yet. The first one runs at 02:00 UTC.</p>', ""
    rows = []
    for name, m in by_model(machines):
        good = next((n for n in nightlies if name in n["files"]), None)
        if not nightlies:
            cell = '<span class="quiet">Not built yet</span>'
        elif not good:
            cell = badge("No build", "fail")
        elif good is latest:
            cell = fmt(good["date"])
        else:
            cell = f'{badge("Failed", "fail")} <span class="quiet using">using {fmt(good["date"])}</span>'
        rows.append(f'<tr data-q="{search_key(m["model"], name, m["chip"])}"><td><a href="m/{e(name)}/">{e(m["model"])}</a><span class="sub"><span class="code">{e(name)}</span> {chip(m["chip"])}</span></td>'
                    f'<td class="code board">{e(name)}</td><td class="board">{chip(m["chip"])}</td><td class="num">{cell}</td></tr>')
    body = f"""<section class="hero"><h1>Firmware for {len(machines)} switches</h1>{summary}{board}</section>
<label class="filter"><span>Find your switch</span><input id="q" type="search" placeholder="Model, board or chipset" autocomplete="off" aria-keyshortcuts="/"></label>
<p class="quiet" id="count" aria-live="polite"></p>
<div class="panel scroll"><table id="models"><caption class="vh">Switches and their latest nightly build</caption>
<thead><tr><th scope="col">Model</th><th scope="col" class="board">Board</th><th scope="col" class="board">Chipset</th><th scope="col" class="num">Latest build</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>
<p class="empty" id="none" hidden>No switch matches. Try the PCB marking or the chipset, for example RTL8373.</p>"""
    return page(SITE, "", body, "Models", script=FILTER_JS)


def anchor(n):
    return f'n-{n["date"]:%Y%m%d}'


def build_model(name, m, nightlies, changes):
    latest = nightlies[0] if nightlies else None
    good = next((n for n in nightlies if name in n["files"]), None)
    head = (f'<p class="crumb"><a href="../../">All switches</a></p><h1>{e(m["model"])}</h1>'
            f'<p class="summary meta"><span>Board <span class="code">{e(name)}</span></span>{chip(m["chip"])}'
            f'<a href="https://github.com/{UPSTREAM}/blob/main/machine/{e(name)}.c">Machine definition</a>'
            f'<a href="https://github.com/{UPSTREAM}/blob/main/doc/supported_devices.md">Supported devices</a></p>')
    if nightlies:
        def state(n):
            return "ok" if name in n["files"] else "fail" if name in n["failed"] else "none"
        word = {"ok": "built", "fail": "failed", "none": "not in this nightly"}
        head += strip([(n["date"], state(n), f'#{anchor(n)}', f'{fmt(n["date"])}: {word[state(n)]}') for n in nightlies],
                      [("ok", "Built"), ("fail", "Failed"), ("none", "Not included")])
    if not good:
        msg = "No successful build in the retained nightlies." if nightlies else "No nightly builds yet. The first one runs at 02:00 UTC."
        return page(m["model"], "../../", head + f'<p class="empty">{msg}</p>', "")
    warn = "" if good is latest else f'<p class="warn">The {fmt(latest["date"])} nightly failed for this switch. Showing the {fmt(good["date"])} build.</p>'
    f = good["files"][name]
    uses = [("oem", "OEM upgrade", "First install. Your switch still runs its original firmware and has a vendor web interface (managed switches): upload this once there."),
            ("custom", "Custom", "Your switch already runs RTL Playground: upload this through its web interface. Also the image to write straight to the flash chip with a SOIC-8 clip.")]
    cards = []
    for key, label, use in uses:
        a = f.get(key)
        if a:
            digest = (a.get("digest") or "").removeprefix("sha256:")
            hash_row = (f'<p class="hash"><span class="quiet">SHA-256</span> <span class="code" title="{digest}">{digest[:16]}…</span>'
                        f'<button type="button" class="copy" data-copy="{digest}" aria-label="Copy SHA-256 of {label}">Copy</button></p>') if digest else ""
            dl = (f'<a class="dl" href="{e(a["browser_download_url"])}">Download {label} <span class="size">{size(a)}</span></a>'
                  f'<span class="code fname">{breakable(a["name"])}</span>{hash_row}')
        else:
            dl = '<p class="quiet">Not built this night.</p>'
        cards.append(f'<div class="pick{" primary" if key == "oem" else ""}"><h3>{label}</h3><p class="use">{use}</p>{dl}</div>')
    meta = [f"Upstream {sha_link(good['sha'])}", f'<a href="{e(good["sums"])}">SHA256SUMS</a>' if good["sums"] else "",
            f'<a href="https://github.com/{UPSTREAM}#readme">Flashing instructions</a>']
    latest_blk = (f'<h2>Latest build <span class="h-note">{fmt(good["date"], True)}</span></h2>{warn}'
                  f'<p class="confirm">For <b>{e(m["model"])}</b> with board <span class="code">{e(name)}</span>. Check this matches your switch before flashing.</p>'
                  f'<div class="picks">{"".join(cards)}</div><p class="meta small">{"".join(f"<span>{x}</span>" for x in meta if x)}</p>')
    log = (f'<h2>Changes in this build</h2>{commit_list(changes[good["tag"]], m, cap=8)}'
           f'<p class="quiet"><a href="https://github.com/{UPSTREAM}/blob/main/CHANGELOG.md">Upstream changelog</a></p>')
    hist = []
    for n in nightlies:
        nf = n["files"].get(name)
        c = changes[n["tag"]]
        when = fmt(n["date"], True)
        if c:
            detail = f'<details><summary>{len(c)}<span class="long"> {"commit" if len(c) == 1 else "commits"}</span></summary>{commit_list(c, m)}</details>'
        else:
            detail = '<span class="quiet">None</span>' if c == [] else '<span class="quiet">Earliest retained</span>'
        if nf:
            def link(k, label):
                a = nf.get(k)
                return f'<a href="{e(a["browser_download_url"])}" aria-label="{label}, {when}">{label}</a>' if a else '<span class="quiet">Not built</span>'
            files = f'<td>{link("oem", "OEM")}</td><td>{link("custom", "Custom")}</td>'
        elif name in n["failed"]:
            files = f'<td colspan="2">{badge("Failed", "fail")}</td>'
        else:
            files = '<td colspan="2"><span class="quiet">Not included</span></td>'
        hist.append(f'<tr id="{anchor(n)}"><td class="date">{when}<span class="sub">{sha_link(n["sha"])}</span></td><td class="up">{sha_link(n["sha"])}</td>{files}<td>{detail}</td></tr>')
    history = (f'<h2>History</h2><div class="panel scroll"><table class="history"><caption class="vh">Nightly builds for {e(m["model"])}</caption>'
               f'<thead><tr><th scope="col">Nightly</th><th scope="col" class="up">Upstream</th><th scope="col">OEM</th><th scope="col">Custom</th>'
               f'<th scope="col">Changes</th></tr></thead><tbody>{"".join(hist)}</tbody></table></div>')
    return page(m["model"], "../../", head + latest_blk + log + history, "", script=COPY_JS)


def build_matrix(machines, nightlies):
    if not nightlies:
        return page("Build matrix", "../", '<h1>Build matrix</h1><p class="empty">No nightly builds yet. The first one runs at 02:00 UTC.</p>', "Matrix")
    cols = "".join(f'<th class="num" scope="col"><a href="{e(n["url"])}">{fmt(n["date"])}</a></th>' for n in nightlies)
    rows = []
    for name, m in by_model(machines):
        cells = []
        for n in nightlies:
            nf = n["files"].get(name)
            when = fmt(n["date"])
            if nf:
                links = "".join(f'<a href="{e(nf[k]["browser_download_url"])}" aria-label="{label}, {when}">{short}</a>'
                                for k, short, label in (("oem", "OEM", "OEM upgrade"), ("custom", "Custom", "Custom")) if k in nf)
                cells.append(f'<td><span class="pair">{links}</span></td>')
            elif name in n["failed"]:
                cells.append(f'<td>{badge("Failed", "fail")}</td>')
            else:
                cells.append('<td><span class="quiet" aria-hidden="true">–</span><span class="vh">Not included</span></td>')
        rows.append(f'<tr><th scope="row"><a href="../m/{e(name)}/"><span class="mname">{e(m["model"])}</span><span class="code">{e(name)}</span></a></th>{"".join(cells)}</tr>')
    body = (f'<h1>Build matrix</h1><p class="summary">{len(machines)} switches across {"the last " if len(nightlies) > 1 else ""}{plural(len(nightlies), "nightly", "nightlies")}. '
            f'Each night links its OEM upgrade and Custom images.</p><div class="panel scroll matrix-wrap"><table class="matrix"><caption class="vh">Builds per switch and night</caption>'
            f'<thead><tr><th scope="col">Switch</th>{cols}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>')
    return page("Build matrix", "../", body, "Matrix", wide=True)


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
    shutil.copytree(Path(__file__).with_name("fonts"), a.out / "fonts")
    (a.out / "index.html").write_text(build_index(machines, nightlies))
    (a.out / "matrix" / "index.html").write_text(build_matrix(machines, nightlies))
    for name, m in machines.items():
        d = a.out / "m" / name
        d.mkdir(parents=True)
        (d / "index.html").write_text(build_model(name, m, nightlies, changes))
    print(f"{len(machines)} switches, {len(nightlies)} nightlies -> {a.out}")


if __name__ == "__main__":
    main()
