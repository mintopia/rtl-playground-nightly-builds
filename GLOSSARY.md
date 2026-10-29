# Glossary

**Upstream**: `logicog/RTLPlayground`, the firmware project this repo builds. Not the `mintopia` fork.

**Machine**: one buildable switch model, named the way upstream's `machine/` directory names it (e.g. `DEFAULT_8C_1SFP`). Every Machine is built and published under its own name, even when it is an alias sharing hardware config with another Machine.

**Custom image**: the main RTL Playground image for a Machine, for switches already running RTL Playground or for writing straight to the flash chip.

**OEM upgrade image**: a second image per Machine, uploaded once through the vendor's stock web UI to move from OEM firmware to RTL Playground. The first-install file for managed switches.

**Nightly**: one scheduled build of every Machine from a single Upstream commit. Machines that fail are left out; the Nightly still counts.

**Dated nightly**: the permanent GitHub Release for one Nightly. The last 14 are kept.

**Rolling nightly**: the `nightly` GitHub Release, which always points at the most recent Nightly.

**Toolchain image**: the container image holding the patched SDCC compiler and build dependencies that every Machine build runs in.
