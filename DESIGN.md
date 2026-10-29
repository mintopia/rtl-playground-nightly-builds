---
name: RTL Playground Nightly Builds
description: A restrained build dashboard for unofficial nightly firmware of Realtek RTL8372/RTL8373 switches.
colors:
  brand-blue: "#0f4c88"
  brand-blue-deep: "#0a3866"
  brand-ink: "#ffffff"
  brand-soft: "#cfe0f3"
  ok-green: "#1d8a4f"
  ok-bg: "#e2f4ea"
  ok-ink: "#0d5a32"
  partial-amber: "#b07800"
  partial-bg: "#fdf1d6"
  partial-ink: "#6b4700"
  fail-red: "#c8372d"
  fail-bg: "#fde6e3"
  fail-ink: "#8f1f17"
  none-grey: "#8a96a4"
  chip-8372-bg: "#dfeaf8"
  chip-8372-ink: "#0d4479"
  chip-8373-bg: "#dcf1e8"
  chip-8373-ink: "#0b5c40"
  warn-bg: "#fff4d6"
  warn-ink: "#5c4300"
  warn-edge: "#e8c360"
  hero-ok: "#7ee2a8"
  hero-partial: "#f5c04a"
  hero-fail: "#ff8f86"
  ground: "#f6f8fb"
  surface: "#ffffff"
  ink: "#141a22"
  quiet: "#566170"
  rule: "#e1e6ec"
  field: "#8a96a4"
  head: "#f1f4f8"
  row-hover: "#eef4fb"
  row-target: "#f0f6fd"
typography:
  display:
    fontFamily: "Overpass, system-ui, -apple-system, Segoe UI, Roboto, sans-serif"
    fontSize: "40px"
    fontWeight: 800
    lineHeight: 1.1
    letterSpacing: "-0.025em"
  headline:
    fontFamily: "Overpass, system-ui, -apple-system, Segoe UI, Roboto, sans-serif"
    fontSize: "32px"
    fontWeight: 800
    lineHeight: 1.1
    letterSpacing: "-0.025em"
  title:
    fontFamily: "Overpass, system-ui, -apple-system, Segoe UI, Roboto, sans-serif"
    fontSize: "19px"
    fontWeight: 800
    letterSpacing: "-0.01em"
  title-sm:
    fontFamily: "Overpass, system-ui, -apple-system, Segoe UI, Roboto, sans-serif"
    fontSize: "16px"
    fontWeight: 800
  wordmark:
    fontFamily: "Overpass, system-ui, -apple-system, Segoe UI, Roboto, sans-serif"
    fontSize: "18px"
    fontWeight: 800
    letterSpacing: "-0.01em"
  body:
    fontFamily: "Overpass, system-ui, -apple-system, Segoe UI, Roboto, sans-serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.5
    fontFeature: "\"tnum\" 1"
  body-sm:
    fontFamily: "Overpass, system-ui, -apple-system, Segoe UI, Roboto, sans-serif"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: "Overpass, system-ui, -apple-system, Segoe UI, Roboto, sans-serif"
    fontSize: "13px"
    fontWeight: 700
  badge:
    fontFamily: "Overpass, system-ui, -apple-system, Segoe UI, Roboto, sans-serif"
    fontSize: "12px"
    fontWeight: 700
    lineHeight: 1.5
  mono:
    fontFamily: "Overpass Mono, ui-monospace, SF Mono, Menlo, Consolas, monospace"
    fontSize: "13px"
    fontWeight: 400
    fontFeature: "\"liga\" 0, \"calt\" 0"
  mono-chip:
    fontFamily: "Overpass Mono, ui-monospace, SF Mono, Menlo, Consolas, monospace"
    fontSize: "12px"
    fontWeight: 600
    lineHeight: 1.5
rounded:
  key: "3px"
  cell: "4px"
  sm: "6px"
  md: "8px"
  panel: "10px"
  card: "12px"
  pill: "999px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "16px"
  gutter: "20px"
  lg: "32px"
  section: "44px"
  xl: "56px"
components:
  band:
    backgroundColor: "{colors.brand-blue}"
    textColor: "{colors.brand-ink}"
    typography: "{typography.wordmark}"
    padding: "14px 20px"
  nav-link:
    textColor: "{colors.brand-soft}"
    padding: "14px 0"
  nav-link-current:
    textColor: "{colors.brand-ink}"
  hero:
    backgroundColor: "{colors.brand-blue}"
    textColor: "{colors.brand-ink}"
    typography: "{typography.display}"
    padding: "28px 0 30px"
  status-cell-ok:
    backgroundColor: "{colors.ok-green}"
    rounded: "{rounded.cell}"
    height: "28px"
  status-cell-partial:
    backgroundColor: "{colors.partial-amber}"
    rounded: "{rounded.cell}"
    height: "28px"
  status-cell-fail:
    backgroundColor: "{colors.fail-red}"
    rounded: "{rounded.cell}"
    height: "28px"
  status-cell-none:
    rounded: "{rounded.cell}"
    height: "28px"
  panel:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.panel}"
  table-head:
    backgroundColor: "{colors.head}"
    textColor: "{colors.quiet}"
    typography: "{typography.label}"
    padding: "11px 16px"
  table-cell:
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    padding: "11px 16px"
  chip-8372:
    backgroundColor: "{colors.chip-8372-bg}"
    textColor: "{colors.chip-8372-ink}"
    typography: "{typography.mono-chip}"
    rounded: "{rounded.pill}"
    padding: "2px 8px"
  chip-8373:
    backgroundColor: "{colors.chip-8373-bg}"
    textColor: "{colors.chip-8373-ink}"
    typography: "{typography.mono-chip}"
    rounded: "{rounded.pill}"
    padding: "2px 8px"
  badge-failed:
    backgroundColor: "{colors.fail-bg}"
    textColor: "{colors.fail-ink}"
    typography: "{typography.badge}"
    rounded: "{rounded.pill}"
    padding: "2px 9px"
  badge-this-model:
    backgroundColor: "{colors.partial-bg}"
    textColor: "{colors.partial-ink}"
    typography: "{typography.badge}"
    rounded: "{rounded.pill}"
    padding: "2px 9px"
  pick-card:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.card}"
    padding: "20px 22px"
  pick-card-primary:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.card}"
    padding: "20px 22px"
  button-download-primary:
    backgroundColor: "{colors.brand-blue}"
    textColor: "{colors.brand-ink}"
    rounded: "{rounded.md}"
    padding: "0 18px"
    height: "46px"
  button-download-primary-hover:
    backgroundColor: "{colors.brand-blue-deep}"
  button-download:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.brand-blue}"
    rounded: "{rounded.md}"
    padding: "0 18px"
    height: "46px"
  button-download-hover:
    backgroundColor: "{colors.row-hover}"
  button-copy:
    textColor: "{colors.brand-blue}"
    typography: "{typography.label}"
    rounded: "{rounded.sm}"
    padding: "4px 10px"
    height: "32px"
  input-filter:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    padding: "8px 14px"
    height: "46px"
    width: "400px"
  notice-warn:
    backgroundColor: "{colors.warn-bg}"
    textColor: "{colors.warn-ink}"
    rounded: "{rounded.md}"
    padding: "10px 14px"
  matrix-pair:
    backgroundColor: "{colors.ok-bg}"
    textColor: "{colors.ok-ink}"
    typography: "{typography.badge}"
    rounded: "{rounded.sm}"
    padding: "2px"
---

# Design System: RTL Playground Nightly Builds

## Overview

**Creative North Star: "The Plain Build Board"**

A clean, confident build dashboard for a hobby firmware. One brand-blue band runs across the top of every page and, on the index, flows straight into a blue hero that carries the title, the last-run line and a 14-night history strip. Below it, everything sits on a pale-grey ground in white rounded panels: a filter, a dense switch table, download cards, a commit list, a history table. Status is told in plain colour and plain words, never in metaphor.

Density is deliberate. Tables run tight (11px by 16px cells), numbers are tabular, board codes and hashes drop into Overpass Mono, and the only decoration is the status colour itself. The site started from a departure-timetable concept and was softened, at the owner's request, into a plain dashboard; the timetable conceits (split-flap type, footnote letters, strike-through cancellations) are rejected outright.

The OEM upgrade card always comes first and is the only one drawn as primary. The wrong file can brick a switch, so the visual hierarchy does the explaining before anyone reads the copy.

**Key Characteristics:**
- One brand-blue band; the index hero extends it full-bleed.
- Pale-grey ground, white panels with a hairline border and a soft two-layer shadow.
- Status colour system: green built, amber some failed, red failed, dashed grey not included.
- Pill chips per chipset (blue 8372, green 8373) and red "Failed" pill badges.
- Overpass for words, Overpass Mono for codes, hashes and chip labels.
- OEM card first and primary; Custom second and outlined.
- Full light and dark themes driven by the same custom properties.

## Colors

A cool, low-chroma neutral world with one saturated blue and a strict traffic-light status set; colour carries meaning, not mood.

### Primary
- **Firmware Blue** (brand-blue): The band, the index hero, the primary download button, the primary card's 2px border, links and the focus ring. In dark mode the band keeps a near-identical blue while links and focus lift to a light sky (#8fc1f3) for contrast.
- **Deep Firmware Blue** (brand-blue-deep): Hover state of the primary download button only.
- **Band Mist** (brand-soft): Secondary text on blue (nav links at rest, hero summary, strip dates and legend) and the 3px focus halo around the filter input.

### Secondary (status)
- **Built Green** (ok-green), with **Built Wash** (ok-bg) and **Built Ink** (ok-ink): History cells for a fully built night; the matrix OEM/Custom pair tile and its link text.
- **Partial Amber** (partial-amber), with partial-bg / partial-ink: History cells for a night where some switches failed; also the "this model" commit badge.
- **Failed Red** (fail-red), with fail-bg / fail-ink: History cells for a failed night; the "Failed" and "No build" pill badges.
- **Absent Grey** (none-grey): The 2px dashed outline of a "not included" cell. Never filled.
- **On-blue status set** (hero-ok, hero-partial, hero-fail): Lighter status colours used only for cells inside the blue hero, where the standard set would sink into the band. Not-included cells on blue use translucent white.

### Tertiary (chipset)
- **8372 Blue Chip** (chip-8372-bg / chip-8372-ink) and **8373 Green Chip** (chip-8373-bg / chip-8373-ink): Chipset pills. Each chipset owns one fixed pair.

### Neutral
- **Cool Ground** (ground): Page background behind panels.
- **Panel White** (surface): Panels, cards, input fill, sticky matrix row headers.
- **Graphite Ink** (ink): Body text and file names.
- **Slate Quiet** (quiet): Summaries, table headers, board codes, footnotes.
- **Hairline** (rule): Panel borders, row dividers, footer rule.
- **Field Grey** (field): Input and Copy button borders.
- **Header Tint** (head), **Row Hover** (row-hover), **Row Target** (row-target): Table header fill, hover row and anchored-row highlight.
- **Notice Cream** (warn-bg / warn-ink / warn-edge): The single fallback notice when the latest nightly failed for a switch.

### Named Rules
**The Status-Only Colour Rule.** Green, amber and red mean built, some failed and failed. They are never used decoratively, and no other hue may stand in for a status.

**The One Blue Rule.** Firmware Blue is the only brand colour. It marks the band, the hero, links and the one primary action per view; nothing else gets a saturated fill.

**The Paired Theme Rule.** Every colour token has a dark counterpart in the same custom property (see the sidecar). New colours are added to both themes or not at all.

## Typography

**Display Font:** Overpass (with system-ui, -apple-system, Segoe UI, Roboto, sans-serif), self-hosted at 400, 600 and 800.
**Label/Mono Font:** Overpass Mono (with ui-monospace, SF Mono, Menlo, Consolas, monospace), self-hosted at 400 and 600.

**Character:** A highway-signage grotesque with a matching mono: plain, legible at small sizes, and engineered rather than styled. Heavy 800 headings against 400 body give hierarchy without size inflation.

### Hierarchy
- **Display** (800, 40px, 1.1, -0.025em): Index hero title only. 30px under 640px.
- **Headline** (800, 32px, 1.1, -0.025em): Page title (model name, "Build matrix"). 26px under 640px. Balanced wrapping.
- **Title** (800, 19px, -0.01em): Section headings ("Latest build", "History"), with an optional 15px quiet note inline on the baseline.
- **Title small** (800, 16px): Download card headings.
- **Wordmark** (800, 18px, -0.01em): Site name in the band.
- **Body** (400, 15px, 1.5, tabular numerals site-wide): All running text and table cells. Card use-text capped at 60ch, commit lists at 82ch.
- **Body small** (400, 14px): Quiet notes, breadcrumbs, meta rows.
- **Label** (700, 13px): Table headers, Copy button, strip dates and legend (400).
- **Badge** (700, 12px): Status pills and matrix pair links.
- **Mono** (400, 13px, ligatures off): Board codes, SHAs, file names, hashes. **Mono chip** (600, 12px): chipset pills.

### Named Rules
**The Mono-Means-Machine Rule.** Overpass Mono is for strings a user might type, compare or copy (board codes, hashes, file names, chipsets). Human names stay in Overpass.

**The No Uppercase Rule.** Headers and labels are sentence case at weight, never letter-spaced capitals.

## Layout

A single centred column, max 1120px with a 20px gutter; the matrix page goes full width. The main column opens 32px below the band and closes 56px above the footer; sections are separated by 44px above each title. The index hero cancels the top padding and paints the band colour full-bleed with a border-image so the blue reads as one continuous slab.

The history strip is a 14-column equal-fraction grid with 4px gaps, capped at 720px, with oldest-to-newest dates under its ends and a legend beneath. Download cards use an auto-fit grid (min 300px, 16px gap), so they sit side by side on desktop and stack OEM-over-Custom on phones.

Under 640px: tables tighten to 10px by 12px, board and chipset columns collapse into a sub-line under the model name, strip cells drop to 24px, download buttons stretch full card width, and the matrix row header stops being sticky. Coarse pointers get taller matrix links (32px). Tables scroll horizontally inside their panel; the page itself never scrolls sideways.

## Elevation & Depth

Nearly flat. Panels and cards lift off the grey ground with a hairline border plus one soft two-layer shadow; nothing else casts a shadow. In dark mode the shadow collapses to a single tight dark line and depth comes from the surface being a step lighter than the ground.

### Shadow Vocabulary
- **Panel lift** (`box-shadow: 0 1px 2px rgb(16 34 56 / 0.06), 0 4px 14px rgb(16 34 56 / 0.06)`): Panels and download cards. Dark: `0 1px 2px rgb(0 0 0 / 0.3)`.
- **Focus halo** (`box-shadow: 0 0 0 3px` Band Mist): Filter input focus only.
- **Current tab underline** (`box-shadow: inset 0 -3px 0` brand-ink): The active nav link in the band.

### Named Rules
**The One Shadow Rule.** There is exactly one elevation. Emphasis comes from border weight (the primary card's 2px blue border), not from a bigger shadow.

## Shapes

Softly rounded rectangles throughout, with radius growing with the object: 3px legend keys, 4px strip cells, 6px small controls and matrix tiles, 8px inputs, buttons and notices, 10px panels, 12px download cards. Chips and badges are full pills (999px). Borders are 1px hairlines; the only 2px strokes are the primary card border and the dashed outline of a not-included cell.

## Components

### Band and navigation
- **Style:** Full-width Firmware Blue bar; wordmark left, nav right, wrapping to a second row on phones.
- **States:** Links rest in Band Mist, turn white on hover; the current page is white with a 3px inset underline. Focus rings switch to white on blue.

### Index hero
- **Style:** Continues the band in the same blue. Display title, a Band Mist summary with white links, then the history strip using the on-blue status set.

### History strip (signature)
- **Cells:** 28px tall (24px on phones), 4px radius, one per retained nightly, oldest left. Filled green, amber or red; not-included is a transparent cell with a 2px dashed grey outline.
- **Behaviour:** Each cell links to its nightly (index) or its history row (model page). Hover lifts 2px and brightens 10% over 150ms ease-out; reduced motion removes it.
- **Legend:** 12px swatches with 3px radius and a short label, always shown.

### Panels and tables
- **Panel:** White, 10px radius, hairline border, panel lift shadow, horizontal scroll inside.
- **Table:** Header row in Header Tint with quiet 13px bold labels; hairline row dividers; hover row in Row Hover (hover-capable pointers only); `:target` row in Row Target. Model names bold, underline only on hover.

### Chips
- **Style:** Mono 12px/600 pill, 2px by 8px, one fixed colour pair per chipset (blue 8372, green 8373). Informational only, never interactive.

### Badges
- **Failed / No build:** Red wash pill, 12px/700, 2px by 9px. Used wherever a build is missing because it failed: index "Latest build", model history, matrix cells. On the index it is followed by a quiet "using <date>" fallback.
- **This model:** Amber wash pill beside commits that touched the switch's own files.

### Download cards
- **OEM upgrade (primary, always first):** White card, 12px radius, 2px Firmware Blue border, 20px by 22px padding. Heading, when-to-use text, a solid blue 46px download button with the file size in lighter weight, the mono file name and a truncated SHA-256 with Copy.
- **Custom (second):** Same card with a hairline border; download button outlined in blue, Row Hover fill on hover.
- **Button press:** 1px down on active; background transitions 150ms ease-out.

### Copy button
- **Style:** Transparent, 1px Field Grey border, 6px radius, 32px min height, blue 13px bold text. Label swaps to "Copied" for 2s.

### Filter input
- **Style:** 46px tall, 8px radius, 1px Field Grey border, white fill, 16px text (no iOS zoom), up to 400px wide beside a bold "Find your switch" label.
- **Focus:** Border turns blue and a 3px Band Mist halo replaces the outline. `/` focuses it.

### Fallback notice
- **Style:** Notice Cream fill, 1px warn-edge border, 8px radius. One per model page, only when the latest nightly failed for that switch.

### Matrix pair
- **Style:** A green-wash 6px tile holding stacked OEM and Custom links (12px/700, Built Ink); link fills Built Green with white text on hover. Absent nights show a quiet en dash.

## Do's and Don'ts

### Do:
- **Do** keep the OEM upgrade card first and primary (2px blue border, solid blue button); Custom follows, outlined.
- **Do** show build state with the four-state cell set: green built, amber some failed, red failed, dashed grey not included.
- **Do** use the on-blue status set (hero-ok, hero-partial, hero-fail) for any strip that sits on the brand blue.
- **Do** mark every failed build with the red "Failed" pill, and pair it with the fallback date where one exists.
- **Do** set board codes, hashes, file names and chipsets in Overpass Mono with ligatures off.
- **Do** put new content in white panels on the grey ground, with the one panel shadow and a hairline border.
- **Do** define every new colour as a custom property in both light and dark themes.

### Don't:
- **Don't** add timetable gimmicks: no departure-board or split-flap styling, no footnote letters, no strike-through "cancelled" builds. The owner explicitly asked for a plain dashboard.
- **Don't** use green, amber or red for anything other than build status.
- **Don't** introduce a second brand colour or a second saturated fill beside Firmware Blue.
- **Don't** make the Custom card primary or put it before OEM.
- **Don't** stack shadows or raise a card's shadow for emphasis; use border weight.
- **Don't** set labels in letter-spaced uppercase.
