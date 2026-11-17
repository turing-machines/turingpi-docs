---
title: "Intro & Specs"
description: "BMC, or Baseboard Management Controller, is a specialized microcontroller that is built into the motherboard of a computer or server. It monitors the…"
head:
  - tag: title
    content: "BMC Intro and Specs | Turing Pi2 | Turing Pi Docs"
lastUpdated: 2025-11-12
---

BMC, or Baseboard Management Controller, is a specialized microcontroller that is built into the motherboard of a computer or server. It monitors the system's hardware and provides remote management capabilities, such as power control or temperature monitoring.

The Turing Pi 2 board is equipped with an Allwinner T113-S3, which provides BMC functionality. This is essentially a mini-computer built into the motherboard. It has features you would expect from a PC, such as a dual-core processor, RAM, and flash storage, albeit in a limited capacity. The best part is that it runs on Linux OS, yes, really!

|                        |                                       |
| :--------------------- | :------------------------------------ |
| **Controller**         | Allwinner T113-S3                     |
| **Processor**          | ARM Cortex-A7 Dual-Core               |
| **Memory**             | 128 MB DDR3                           |
| **Storage**            | 1 GB NAND Flash Memory (MX35LF1GE4AB) |
| **Additional Storage** | microSD card slot                     |

## Control BMC

Most functionality of The BMC can be controlled using both the `tpi` application and web UI. The `tpi` application provides a command line interface, whereas the web interface provides a more user-friendly experience. More information on installing tpi can be found in the [TPI](/docs/tpi-installation) section.

## User Interface (UI) or Graphical User Interface (GUI)

The UI can be found at [https://turingpi/](https://turingpi/) (sometimes, depending on your local network: [https://turingpi.local/](https://turingpi.local/)) find out more on the [UI](/docs/turing-pi2-bmc-ui) pages.

## Open source

All software related to the Turing-Pi is open source. We continually work to enhance our BMC firmware, providing a solid foundation for optimal management and control of your system's hardware. Our open-source approach allows anyone to access and modify the source code to accommodate their needs. This transparency and collaboration fosters a more robust BMC firmware that benefits all users.

:::note
⚙️ **[Github Repo](https://github.com/turing-machines/BMC-Firmware)**
:::
