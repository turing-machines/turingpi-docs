---
title: "Firmware upgrade"
description: "Firmware in version 2.x overhauls the flashing method and how the images are built. We drop the dependency on Phoenix Suit, but this also means we cannot…"
head:
  - tag: title
    content: "Firmware upgrade | BMC | Turing Pi 2 | Turing Pi Docs"
lastUpdated: 2025-11-12
---

## BMC firmware upgrade to version 2.x

Firmware in version 2.x overhauls the flashing method and how the images are built. We drop the dependency on Phoenix Suit, but this also means we cannot use either Phoenix Suit or the original (contained in the firmware version 1.x) OTA updates to perform the upgrade from version 1.x to 2.x.

To perform an upgrade from version 1.x to version 2.x you’ll need an empty SD card, flash the image to the SD card, and boot the Turing Pi 2 board off of this SD card with the steps described in the [v1.x to v2.x](/docs/turing-pi2-bmc-v1x-to-v2x) page. The same flashing method can be used to recover the board if, for any reason, the BMC does not boot anymore.

If you have any version 2.x installed already, unlike in version 1.x, you can perform all subsequent updates using [the new OTA](/docs/turing-pi2-bmc-v2x-to-v2x) the feature in the BMC GUI.

If you cannot access the SD card slot, [there is also a way to perform the upgrade](/docs/turing-pi2-bmc-v1x-to-v2x#upgrading-the-firmware-without-sd-card-access).

You can also choose to [run the firmware off of an SD card](/docs/turing-pi2-bmc-run-from-sd), but the upgrades will be a little tricky currently.

While it's still possible to return to the firmware v1.x from v2.x, it is strongly recommended not to do so without a very good cause. This is because Phoenix Suit will probably not convert the erase-counter headers, and the wear information will be lost (which may shorten the Flash life).

 

## Firmware upgrade

Follow the links below that match your current state to perform the firmware upgrade:

* [Upgrade v2.x firmware to v2.x firmware](/docs/turing-pi2-bmc-v2x-to-v2x)
* [Upgrade v1.x firmware to v2.x firmware](/docs/turing-pi2-bmc-v1x-to-v2x) (OTA update, or recover from BMC not booting)
* [Upgrade v1.x firmware to v1.x firmware]() (obsolete)
* [Upgrade v1.x firmware to v2.x firmware without physical access to the SD card](/docs/turing-pi2-bmc-v1x-to-v2x#upgrading-the-firmware-without-sd-card-access)
* [Run firmware from the SD card (without flashing the BMC)](/docs/turing-pi2-bmc-run-from-sd)
* [Upgrade firmware that runs from the SD card](/docs/turing-pi2-bmc-run-from-sd#ota-update)
