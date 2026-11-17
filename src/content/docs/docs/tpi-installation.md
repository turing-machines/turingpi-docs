---
title: "Installation"
description: "You can download prebuilt binaries for your preferred platform from the releases page of the BMC-Firmware repository."
head:
  - tag: title
    content: "Installation | TPI | Turing Pi 2 | Turing Pi Docs"
lastUpdated: 2025-11-12
---

## Prebuilt binaries

### Releases

You can download prebuilt binaries for your preferred platform from the [releases](https://github.com/turing-machines/BMC-Firmware/releases) page of the BMC-Firmware repository.

TODO: [http://firmware.turingpi.com](http://firmware.turingpi.com) ?

### Nightly GitHub builds

Alternatively, a GitHub action runner builds packages for every commit to the [source](https://github.com/turing-machines/tpi) repository. To download them, navigate to [build actions](https://github.com/turing-machines/tpi/actions/workflows/build.yml), choose a workflow run and scroll to the "Artifacts" section.

## Package managers

### Arch User Repository (AUR)

The package is available in the [AUR](https://aur.archlinux.org/packages/tpi).

## Building from source

### Installation via cargo

To automatically download, build and install from source, invoke the following command (requires Rust toolchain installed):

`cargo install tpi`

### Building

It's also possible to clone the repository and issue a `cargo build --release`.
