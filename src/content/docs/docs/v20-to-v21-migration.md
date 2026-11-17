---
title: "V2.1 network migration"
description: "how to deal with the breaking network change in v2.1"
head:
  - tag: title
    content: "V2.1 network migration | BMC | Turing Pi 2 | Turing Pi Docs"
lastUpdated: 2025-11-12
---

<p class="lead">how to deal with the breaking network change in v2.1</p>

This page is specifically targeted for users that are running v2.0, made changed to the `/etc/network/interfaces` file and want to install firmware version 2.1.x. 

If you never touched this file you can skip this section and follow the normal upgrade guide [here](/docs/turing-pi2-bmc-v2x-to-v2x).

There is no manual action required, this page is to warn users that network configuration will change and, depending on setup, could result in an network loss.

:::note[Test if you are affected]
to test if this applies to you, you can copy/paste the following snippet in a BMC shell:

```shell
if [ -f "/mnt/overlay/upper/etc/network/interfaces" ] && (grep -qE "^[^#]*eth0" "/mnt/overlay/upper/etc/network/interfaces" || ! grep -qE "node[1-4]|ge[01]" "/mnt/overlay/upper/etc/network/interfaces"); then echo "migration required!"; else echo "Not affected"; fi
```
:::

During the update to v2.1 an attempt is made to upgrade the `interfaces`file. It will update definitions and aliases from `eth0` to the appropriate new bridge interface. The original `interfaces` file will be renamed to `interfaces_bak` and can be put back in the event of errors.

## Disable migration script

Before installing the update, [login](/docs/turing-pi2-bmc-how-to-get-started) the BMC and create the file `/root/.disable_interface_migration` if you prefer to manually update the interfaces config.

```text
touch /root/.disable_interface_migration
```

This will opt out of the migration later on once you decide to install the update.

To make manual adjustments use the reference configuration, which can be found [here](https://github.com/turing-machines/BMC-Firmware/blob/master/tp2bmc/board/tp2bmc/overlay/etc/network/interfaces)
