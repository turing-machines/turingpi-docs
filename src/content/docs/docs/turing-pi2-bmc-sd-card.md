---
title: "BMC SD Card"
description: "The Turing Pi 2 board includes an SD card slot located on its back. This slot is directly linked to the Board Management Controller (BMC), which tries to…"
head:
  - tag: title
    content: "BMC SD Card | Turing Pi2 | Turing Pi Docs"
lastUpdated: 2025-11-12
---

The Turing Pi 2 board includes an SD card slot located on its back. This slot is directly linked to the Board Management Controller (BMC), which tries to access (or "mount") the SD card during the startup process. This feature allows you to use the SD card for storing things like ISO images, personalized scripts, or programs.

When using an SD card, it's important to know the compatible file systems:

* exFAT: This is the preferred choice if you're using a Windows system.
* NTFS: If you're using this with a Windows system, make sure to eject the card safely. If not done, the Linux system on the BMC might face issues, causing it to limit the SD card's usage to read-only mode.
* FAT32: Try to avoid this one, as it has some limitations.
* EXT4

Once an SD card is inserted, the system automatically sets it up under the **/mnt/sdcard** directory.
