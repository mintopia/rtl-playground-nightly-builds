# Nightly builds of RTL Playground for all switches

Nightly firmware for every machine in [logicog/RTLPlayground](https://github.com/logicog/RTLPlayground), published as [releases](../../releases):

- `nightly` — always the latest build
- `nightly-YYYYMMDD-<sha>` — the last 14 nightly builds

Each release has `rtlplayground-<version>-<sha>-YYYYMMDD-<MACHINE>.bin`, `…-oem_upgrade.bin` (OEM web UI installer) and `SHA256SUMS`. Machines that failed to build are listed in the release notes.

Builds are skipped when upstream hasn't changed; run the **Nightly** workflow with `force` to rebuild anyway. The compiler toolchain image is rebuilt weekly (see [ADR 0001](docs/decisions/0001-toolchain-image-keyed-by-sdcc-hash.md)).
