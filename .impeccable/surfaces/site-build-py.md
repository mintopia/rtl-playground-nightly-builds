---
version: 1
slug: "site-build-py"
primary_target: "site/build.py"
related_targets: []
---

Scope: GitHub Pages site (index, per-model page, matrix). Mode: Operate.
Audience/job: switch owner finds their model, picks OEM (first install) or Custom (already on RTL Playground), downloads, verifies SHA-256; maintainer scans build health.
Constraints: static, no dead links (14 retained nightlies), labels by when to use each file. User pinned: "less gimmicky timetable, just look good"; OEM first.

## Direction contract

THESIS: A clean, confident build dashboard for a hobby firmware: one brand-blue band, white panels, status shown with plain badges and a 14-night history strip. Refuses gimmicks (timetable conceits, footnote letters, strike-through cancellations).

OWN-WORLD: Brand blue #0f4c88 band and index hero; pale-grey ground with white rounded panels; Overpass + Overpass Mono; green/amber/red/dashed-grey status cells; pill chips per chipset (blue 8372, green 8373); red "Failed" pills.

STORY: The visitor finds their switch by name, reads which file fits their situation, downloads it and can copy its SHA-256, and trusts the date and upstream commit behind it.

FIRST VIEWPORT: Index: band flows into hero (title, last-run line, history strip with legend), then filter and the switch table panel. Model page: name, board/chip/links, its own history strip, then Latest build with two cards, OEM first and primary.

FORM: Departure timetable, candidate 7 of 7, softened to a plain dashboard at the user's request. seed: none (unavailable)

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
