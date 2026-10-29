# Decision: Toolchain image in GHCR keyed by SDCC patch hash

Status: accepted
Date: 2026-10-29

## Context
Upstream needs SDCC 4.6.0 with its own patches applied. Stock or distro SDCC miscompiles the firmware. On a cold run, every `make` downloads SDCC from SourceForge and builds it, which takes minutes and fails when SourceForge is flaky. A Nightly runs one build job per Machine, about 57 of them.

## Decision
Build the toolchain once into a container image. The image is upstream's Dockerfile plus the patched SDCC, installed at `/opt/toolchain/sdcc-<cksum>`. Push it to `ghcr.io/<owner>/rtl-playground-toolchain:sdcc-<cksum>`. `<cksum>` uses the same formula as upstream's Makefile, `cat sdcc/* | cksum`, so a new upstream patch automatically gives a new tag.

- A Nightly builds the image first if its tag is missing.
- A weekly job rebuilds the current tag to pick up Debian updates, deletes untagged versions, and keeps the 3 newest.
- Build jobs symlink `/opt/toolchain` to `toolchain/`, so upstream's Makefile finds the compiler unchanged.

## Consequences
- Build jobs never touch SourceForge, and the environment matches upstream's Dockerfile.
- The image formula depends on upstream's Makefile toolchain path and cksum rule. If upstream changes either, make silently rebuilds SDCC in every job: slow but correct.
- Only 3 toolchains are kept. Rebuilding an older Nightly may require rebuilding its image.

## Supersedes
None
