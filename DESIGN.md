---
name: RTL Playground Nightly Builds
description: A plain, well-made dark download page for unofficial RTL8372/RTL8373 switch firmware.
colors:
  ground: "#0b0c0e"
  surface: "#141518"
  surface-raised: "#1b1c20"
  line: "#26272c"
  line-strong: "#34353b"
  ink: "#ededef"
  ink-secondary: "#a1a2aa"
  ink-muted: "#8a8b93"
  indigo: "#6e79f6"
  indigo-fill: "#5059d8"
  indigo-fill-hover: "#4650c8"
  indigo-text: "#a5acff"
  on-indigo: "#ffffff"
  built-green: "#46a758"
  failed-red: "#e5484d"
  failed-red-text: "#ff8589"
  caution-amber: "#f5a524"
  caution-amber-text: "#ffc062"
  favourite-yellow: "#ffd60a"
typography:
  display:
    fontFamily: "-apple-system, BlinkMacSystemFont, \"Segoe UI Variable Text\", \"Segoe UI\", Roboto, \"Helvetica Neue\", sans-serif"
    fontSize: "clamp(28px, 4.2vw, 40px)"
    fontWeight: 700
    lineHeight: 1.12
    letterSpacing: "-0.025em"
  title:
    fontFamily: "-apple-system, BlinkMacSystemFont, \"Segoe UI Variable Text\", \"Segoe UI\", Roboto, \"Helvetica Neue\", sans-serif"
    fontSize: "17px"
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: "-0.01em"
  lede:
    fontFamily: "-apple-system, BlinkMacSystemFont, \"Segoe UI Variable Text\", \"Segoe UI\", Roboto, \"Helvetica Neue\", sans-serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.55
  body:
    fontFamily: "-apple-system, BlinkMacSystemFont, \"Segoe UI Variable Text\", \"Segoe UI\", Roboto, \"Helvetica Neue\", sans-serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.55
    fontFeature: "\"tnum\""
  field:
    fontFamily: "-apple-system, BlinkMacSystemFont, \"Segoe UI Variable Text\", \"Segoe UI\", Roboto, \"Helvetica Neue\", sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.55
  small:
    fontFamily: "-apple-system, BlinkMacSystemFont, \"Segoe UI Variable Text\", \"Segoe UI\", Roboto, \"Helvetica Neue\", sans-serif"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.55
  label:
    fontFamily: "-apple-system, BlinkMacSystemFont, \"Segoe UI Variable Text\", \"Segoe UI\", Roboto, \"Helvetica Neue\", sans-serif"
    fontSize: "13px"
    fontWeight: 500
    lineHeight: 1.4
  mono:
    fontFamily: "ui-monospace, \"SF Mono\", SFMono-Regular, Menlo, Consolas, monospace"
    fontSize: "12.5px"
    fontWeight: 400
    lineHeight: 1.6
rounded:
  cell: "5px"
  code: "6px"
  control-sm: "7px"
  control: "8px"
  button: "9px"
  field: "10px"
  surface: "12px"
  pill: "99px"
spacing:
  xxs: "4px"
  xs: "8px"
  sm: "12px"
  md: "16px"
  lg: "24px"
  xl: "32px"
  xxl: "48px"
  page-bottom: "64px"
  page-max: "1040px"
  label-column: "220px"
components:
  button-download:
    backgroundColor: "{colors.indigo-fill}"
    textColor: "{colors.on-indigo}"
    rounded: "{rounded.button}"
    padding: "0 16px"
    height: "44px"
  button-download-hover:
    backgroundColor: "{colors.indigo-fill-hover}"
  button-copy:
    backgroundColor: "{colors.surface-raised}"
    textColor: "{colors.ink}"
    rounded: "{rounded.control-sm}"
    padding: "0 12px"
    height: "32px"
  input-search:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.field}"
    padding: "0 48px 0 44px"
    height: "48px"
  panel:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.surface}"
    padding: "24px"
  list-row:
    textColor: "{colors.ink}"
    padding: "14px 18px"
    height: "64px"
  list-row-hover:
    backgroundColor: "{colors.surface-raised}"
  favourite-toggle:
    textColor: "{colors.ink-muted}"
    rounded: "{rounded.control}"
    size: "44px"
  favourite-toggle-on:
    textColor: "{colors.favourite-yellow}"
  tag:
    backgroundColor: "{colors.surface-raised}"
    textColor: "{colors.ink-secondary}"
    rounded: "{rounded.pill}"
    padding: "1px 8px"
  board-warning:
    textColor: "{colors.caution-amber-text}"
    rounded: "{rounded.field}"
    padding: "12px 16px"
  nav-link:
    textColor: "{colors.ink-secondary}"
    rounded: "{rounded.control}"
    padding: "6px 10px"
---

# Design System: RTL Playground Nightly Builds

## Overview

**Creative North Star: "The Well-Made Download Page"**

A neutral, near-black page that does one job: get a switch owner to the one correct file for their board. It plays the category standard straight, in the register of Linear, Vercel, Raycast and Tailscale download pages: one centred column under a sticky top bar, system sans with a real type scale, borders instead of shadows, and a single indigo accent spent on links and the download button. No sidebar, no dashboard chrome, no badge wall.

Density is calm but not sparse. Headings are short and heavy, supporting text steps down through two greys, and data (board codes, filenames, hashes, commit SHAs) is set in monospace and allowed to wrap rather than truncate. State is carried by a small Radix-like palette: green built, red failed, amber caution. A yellow star marks favourites.

The site is dark only. There is no light theme, and none should be added.

**Key Characteristics:**
- Dark only; `color-scheme: dark`.
- One page column, max 1040px, centred; nothing inside it carries its own narrow width cap.
- Flat tonal layering: ground, surface, raised surface, separated by 1px lines.
- One accent hue (indigo) for interaction; state colours used only for state.
- Monospace for machine data; tabular numerals everywhere.
- Everything that lists nights is ordered newest first.

## Colors

A cool near-black neutral ramp with one indigo accent and a small set of state colours.

### Primary
- **Indigo** (`indigo`): accent hue for focus ring tint, search focus border, logo mark, row highlight on `:target`, text selection. Not used as a large fill.
- **Indigo Fill** (`indigo-fill`): the download button background only. White text on it is 5.6:1. Hover deepens to **Indigo Fill Hover** (`indigo-fill-hover`).
- **On Indigo** (`on-indigo`): white label text on the download button; also the board code inside the amber warning and text selection.
- **Indigo Text** (`indigo-text`): every link, the expand control, `<summary>`, and the focus outline. Readable on ground and surface.

### Secondary
- **Built Green** (`built-green`): a successful build. Strip cells, matrix dots, state dots.
- **Failed Red** (`failed-red`): a failed build (cells, dots). Text that says "failed" uses **Failed Red Text** (`failed-red-text`).
- **Caution Amber** (`caution-amber`): partial builds and the tint behind caution notes. Copy in those notes uses **Caution Amber Text** (`caution-amber-text`).

### Tertiary
- **Favourite Yellow** (`favourite-yellow`): the filled star on a favourited switch. Used for nothing else.

### Neutral
- **Ground** (`ground`): page background, also behind the translucent top bar (85% mix + blur).
- **Surface** (`surface`): panels, lists, tables, search input, download panels.
- **Surface Raised** (`surface-raised`): hover fill for rows and nav links, tags, copy button, board-code chip, expanded commit rows, "no nightly" strip cells.
- **Line** (`line`): 1px dividers and surface borders.
- **Line Strong** (`line-strong`): input and control borders, borders inside raised areas, "no nightly" matrix dot.
- **Ink** (`ink`): primary text.
- **Ink Secondary** (`ink-secondary`): ledes, descriptions, table headers, footer, nav links at rest.
- **Ink Muted** (`ink-muted`): metadata, placeholders, icons at rest, filenames, the dashed "not included" outline. Kept at this value for legibility on surface; do not darken it.

### Named Rules
**The One Accent Rule.** Indigo is the only interaction colour. Links, focus and the download button use it; nothing decorative does.

**The State Means State Rule.** Green, red and amber appear only where they report a build result or a caution. Yellow appears only on an active favourite star.

**The Dark Only Rule.** One theme. No `prefers-color-scheme: light` branch, no theme toggle.

## Typography

**Display Font:** system UI sans (`-apple-system`, Segoe UI Variable, Roboto fallback)
**Body Font:** the same system sans
**Label/Mono Font:** `ui-monospace` / SF Mono / Menlo / Consolas, ligatures off

**Character:** native, quiet and precise. Weight and size do the hierarchy; the mono face marks anything a user might compare or paste.

### Hierarchy
- **Display** (700, clamp 28–40px, 1.12, -0.025em, balanced wrap): one per page; site name on home, model name on model pages, "Build matrix".
- **Title** (600, 17px, 1.3, -0.01em): section headings (block labels, download panel names, "Favourites").
- **Lede** (400, 17px; 16px under 640px, ink-secondary, pretty wrap): the single line under the display heading.
- **Body** (400, 15px, 1.55, tabular numerals): default text; list row names at 550.
- **Field** (16px): search input text, and the lede under 640px.
- **Small** (14px): descriptions, nav, notes, tables, commit lists. **Label** (13px): table headers, row metadata, strip dates, legends, footer.
- **Mono** (12.5–13px, 1.6): board codes, filenames, SHA-256, commit SHAs.

### Named Rules
**The Underscore Break Rule.** Board codes and filenames break only at underscores (the build inserts break opportunities there); never mid-token, never truncated with an ellipsis. Hashes may break anywhere.

**The Tabular Rule.** Numerals are tabular site-wide so dates, sizes and counts align in columns.

## Layout

A single centred column (`page-max`, 1040px) with 24px side padding (16px under 640px). The top bar inner row and the footer share the same width, so the header, content and footer edges align. The matrix page uses the same column width as every other page; its table scrolls horizontally inside its own wrapper when it doesn't fit.

Pages open with 48px of top padding (32px on mobile) and end with 64px. Content sections on the model page are **blocks**: a two-column grid with a 220px label column (title, one-line description, related links) and a fluid body, a 48px column gap, a 1px top rule and 32px above it. Under 640px blocks collapse to one column and the label's links run horizontally.

Spacing steps are 4, 8, 12, 16, 24, 32, 48 and 64px.

Breakpoints: 640px (single-column blocks, full-width download button, brand subtitle and nav icons hidden), 480px (tighter top bar).

### Named Rules
**The One Bound Rule.** Only the page container is width-bounded. Text, inputs, panels, lists and tables inside it fill the column; never add a narrow `max-width` to a paragraph, search field or panel.

**The Newest First Rule.** Every history (14-day strip, build table, matrix columns) reads newest on the left or top.

## Elevation & Depth

Flat. Depth comes from tonal steps (ground → surface → raised surface) and 1px borders, not shadows. The only blur is the sticky top bar's translucent backdrop. Box-shadow appears only as a state response: the 3px indigo focus halo on the search field and the 3px green halo on a hovered matrix dot.

### Named Rules
**The Borders Not Shadows Rule.** Surfaces are separated by 1px `line` borders. No drop shadows at rest.

## Shapes

Softly rounded rectangles. Large surfaces (panels, lists, tables) use a 12px radius; the search field and caution notes 10px; the download button 9px; small controls 7–8px; inline code chips 6px; strip cells 5px; tags are full pills. Status is drawn as circles: 8px state dots, 14px matrix dots. "No nightly" is a smaller 6px grey dot in the matrix and a raised-surface cell in the strip; "not included" is a hollow outline.

## Components

### Buttons
- **Shape:** gently rounded (9px), 44px tall.
- **Download (primary):** indigo fill, white 600-weight label, leading download icon, file size pushed right at 80% opacity. Minimum 320px wide on desktop, full width under 640px. The only filled button in the system.
- **Hover / Focus:** fill darkens; focus shows the global 2px indigo-text outline, 2px offset.
- **Copy (secondary):** 32px tall, raised-surface fill, strong-line border; border lightens to ink-muted on hover.
- **Expand (text):** indigo-text label with a chevron that rotates when open; toggles a full-width commit row below its table row.

### Chips
- **Tag:** pill, raised-surface fill, 12px secondary text. "Check board" variant uses an amber tint with amber text.
- **Board code:** mono inline chip, raised-surface fill, strong-line border, 6px radius.

### Cards / Containers
- **Corner Style:** 12px.
- **Background:** surface on ground.
- **Shadow Strategy:** none (see Elevation & Depth).
- **Border:** 1px line.
- **Internal Padding:** 24px for download panels (20px mobile); 4px 18px for list-like panels.

### Inputs / Fields
- **Search:** full column width, 48px tall, surface fill, strong-line border, 10px radius, 16px text, leading search icon, trailing `/` key hint that hides on focus or input.
- **Focus:** border turns indigo plus a 3px indigo halo at 25%.

### Navigation
- **Top bar:** sticky, 56px, translucent ground with blur and a bottom line. Brand (indigo logo mark, "RTL Playground" plus muted "Nightly Builds") on the left; text nav links on the right in ink-secondary, raised-surface hover fill, ink for the current page. Under 640px the subtitle and nav icons drop.
- **Back link:** small secondary-text link with leading chevron above the model heading.
- **Footer:** one line of 13px secondary text, same width as the column.

### Switch List
One surface card of rows, 64px minimum. Each row: model name (550 weight) with optional "Check board" tag, mono board code and chipset underneath, a build state dot and label, a chevron that nudges 2px right on hover, then a 44px favourite star toggle outside the link. The star is ink-muted outline at rest and filled favourite-yellow when pressed. Favourites render as a separate list above "All switches".

### Board-Check Warning
Amber-tinted note (amber 10% over ground, amber 35% border, 10px radius) with a warning icon, amber text and the board code in white mono. Sits under the model lede, before any download; any twin-model note is folded into it.

### Download Panels
OEM panel stacked above Custom, never side by side. Each panel: title, one-line "when to use", "For board `X` only", the download button, the filename in muted mono, then a ruled SHA-256 section with the full hash (select-all) and a Copy button.

### History Strip
Fourteen equal cells in a grid, newest first, 28px tall, 5px radius: green built, amber partial, red failed, dashed outline not included, raised surface for no nightly. Dates at both ends, legend below. Linked cells brighten on hover. Appears on the home page (under search) and the model page (above the build table).

### Build Table and Matrix
Tables sit in a surface card with horizontal overflow, 13px secondary headers, 1px row rules, and a 10% indigo highlight on the `:target` row. Commit lists expand into a full-width raised-surface row. The matrix shows one coloured dot per switch per day for all 14 days, with a sticky model column carrying name and board code.

## Do's and Don'ts

### Do:
- **Do** keep the site dark only.
- **Do** let every text block, input, panel and table fill the 1040px column.
- **Do** stack the OEM panel above the Custom panel, each with "For board X only".
- **Do** show the full SHA-256 with a Copy button under every download.
- **Do** order every history newest first and always show all 14 days.
- **Do** draw the matrix as one dot per day, in the same column width as other pages.
- **Do** use indigo-fill (white text, 5.6:1) for the download button and indigo-text for links.
- **Do** use favourite-yellow only for an active favourite star.
- **Do** break board codes only at underscores.

### Don't:
- **Don't** add a light theme or theme toggle.
- **Don't** put a narrow max-width on text, the search field or panels inside the page column.
- **Don't** place OEM and Custom side by side.
- **Don't** add a sidebar, dashboard chrome or a wall of badges.
- **Don't** use drop shadows to separate surfaces.
- **Don't** use green, red or amber decoratively, or indigo as a large background fill.
- **Don't** darken the muted grey below ink-muted.
- **Don't** truncate board codes, filenames or hashes.

## Known Gaps

Accessibility items deferred by the user, not rules:
- Copy result is not announced to assistive tech.
- The favourite button is announced twice (label plus pressed text).
- Matrix and strip dots convey state by colour alone (titles and labels exist, no shape difference beyond "none" and "gap").
