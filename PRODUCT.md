# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack
Static site on GitHub Pages, regenerated after each Nightly. Generator: delegated — user only requires the output to be static; chosen a dependency-free Python (stdlib) script in this repo so the nightly workflow needs no extra toolchain.

## Users
Owners of a specific cheap 2.5G/10G Realtek RTL8372/RTL8373 switch who want to run RTL Playground firmware. They arrive knowing the name on the box or the PCB marking, not upstream's board codes. Job: find their model, pick the right file for how they flash, download it. Secondary: maintainers checking which Machines built.

## Product Purpose
Unofficial nightly firmware for every Machine in logicog/RTLPlayground. Success: a user reaches the correct file for their switch and flashing method without reading the build system.

## Positioning
Every Machine, every night, under its own model name — including aliases upstream shares config between — with no local toolchain needed.

## Operating Context
Two files per Machine per Nightly:
- **OEM** (`…-oem_upgrade.bin`): uploaded once through the switch's original vendor web UI to move to RTL Playground. Only for managed switches still on stock firmware.
- **Custom** (`….bin`): the RTL Playground image itself; uploaded through RTL Playground's own web UI on a switch already running it, or written directly to the flash chip with a SOIC-8 clip (the only route for unmanaged switches).
Flashing the wrong Machine's image can brick a switch; upstream asks users to double-check the machine type.

## Capabilities and Constraints
- Machine list, display model name (`MACHINE_MODEL`) and chipset come from upstream `machine/*.h`; board code is the Machine name.
- History = the last 14 Dated nightlies (older releases are deleted; never link to them).
- Per Nightly changelog = upstream commits since the previous Nightly; commits touching a Machine's own files are relevant to that Machine.
- A Machine may fail a given Nightly; its page then offers its last successful build.
- Not known per Machine: managed/unmanaged status, flash size, retail names beyond `MACHINE_MODEL`. Do not infer these.

## Brand Commitments
Unofficial build mirror; must not present itself as the upstream project.

## Evidence on Hand
Real data only: GitHub Releases of this repo, upstream git history, `machine/*.h`, upstream `doc/supported_devices.md` (linkable, not machine-mapped).

## Product Principles
- The right file beats more files: label OEM vs Custom by when to use each.
- Name things the way the box does; board codes are secondary.
- Dense and scannable over decorated.
- Never show a link that 404s.
