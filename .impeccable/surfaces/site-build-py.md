---
version: 1
slug: "site-build-py"
primary_target: "site/build.py"
related_targets: []
---

Scope: GitHub Pages site (index, per-model page, matrix). Mode: Operate.
Audience/job: switch owner finds their model, picks OEM (first install) or Custom (already on RTL Playground), downloads, verifies SHA-256; maintainer scans build health.
Constraints: static, no dead links (14 retained nightlies), labels by when to use each file, dark only. User 2026-10-30: previous designs too busy, generic, file hard to find; wants clean, simple, responsive "crisp product page". Chose the canon direction; craft bar Linear/Vercel and Raycast/Tailscale download pages.

## Direction contract

THESIS: A plain, well-made download page. One column, top nav, no sidebar, no badges wall. Refuses dashboard chrome.

OWN-WORLD: Neutral dark (#0b0c0e ground, #141518 surface, #26272c lines), indigo accent #6e79f6 for buttons and links only, Radix-like green/red for state. System sans, real type scale, 12px radius surfaces, borders not shadows.

STORY: Visitor searches by box name or board code, opens the model, reads which of two files fits, downloads, copies the SHA-256.

FIRST VIEWPORT: Index: headline, one-line lede, large search, then the switch list. Model page: back link, model name, board-check lede, amber board-check warning (twin note folded in), then a Download section: OEM panel stacked above Custom (user answer 2026-10-30), each with "For board X only", button, filename, full hash and copy. Home: 14-day strip under search, favourites section above the list.

FORM: Category standard played straight (canon). seed: none (unavailable)

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
