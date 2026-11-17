---
title: "Failsafe boot"
description: "Using Safe mode, users can recover their boards in case its not booting anymore. Safe mode temporarily disables all user modifications to the filesystem…"
head:
  - tag: title
    content: "Failsafe boot | BMC | Turing Pi 2 | Turing Pi Docs"
lastUpdated: 2025-11-12
---

## Safe mode

Using Safe mode, users can recover their boards in case its not booting anymore. Safe mode temporarily disables all user modifications to the filesystem, effectively booting the board with "factory settings." After a successive reboot, the board boots again with all the files present as before the safe boot. 

:::tip[user files are perserved]
Failsafe will never remove or permanently change any files that the user created.
:::

If failsafe is activated and your board is still not booting, we recommend you ask for help on Discord or our Question section.

### Entering safe mode

* restart your board
* Press the `KEY_1` button for 5 seconds
* if you have a serial cable connected to the BMC UART3 port, you see the following logline passing by:

```shell
PREINIT: Starting  
PREINIT: Entering safemode
```

* Logged in to the BMC, verify that you are in safe mode by checking the environment variable "IS\_SAFEMODE":

```shell
$IS_SAFEMODE && echo "we are in safemode!"
```

### About read-only filesystems

The BMC uses a read-only filesystem, EROFS. This filesystem can layer multiple partitions on top of each other. This enables us to upgrade the bottom layer, our base firmware, without wiping any files residing on the user layer. We will not go into much detail on how this works, but its important to understand that these layers are opaque to the user and that in safe mode, the user partition is mounted to an arbitrary directory rather than layered on top of the root filesystem. 

### How to mount the user layer

If there is a problem with something in the user layer, for example a misconfiguration in `/etc/ssh/sshd_config` file that prevents the SSH service from operating, you will need to mount the user layer in order to address the problem. To do this run the following command:

```shell
mount_overlay && cd /mnt/overlay/upper
```

You will now find yourself within the user layer. In our example, to fix the `sshd_config` file you would edit the file under `etc/ssh/ssh/sshd_config`.  When you are satisfied, call.`reboot` to reboot the system. Your board will start up again in normal mode.

## Recovery mode

When `KEY1` is pressed for 15 seconds during boot, or if no valid OS is found, "recovery mode" is entered. Depending on if you are running Linux from your SD card or, more conventionally, from Flash the following will happen:

* Flash

an attempt is made to do a netboot over DHCP. If failed, it falls back to providing the U-Boot console over netconsole.

* (micro)SD card

exposes the microSD card over the USB interface as a mass storage device
