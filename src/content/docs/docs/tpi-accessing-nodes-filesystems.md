---
title: "Accessing nodes' filesystems"
description: "With tpi it's possible to access filesystems of nodes by booting them as a Mass Storage Device (MSD)."
head:
  - tag: title
    content: "Accessing nodes' filesystems | TPI | Turing Pi 2 | Turing Pi Docs"
lastUpdated: 2025-11-12
---

With `tpi` it's possible to access filesystems of nodes by booting them as a Mass Storage Device (MSD).

1. Execute a command with a desired node number:\
   `tpi advanced msd --node 1`
2. Wait for the device to reboot, which should take around 10 seconds.
3. Create a directory for mounting, if needed:\
   `mkdir /mnt/raspios`
4. Mount one or more desired partitions:\
   `mount /dev/sda1 /mnt/raspios`
5. Perform any applicable read or write operations:\
   `vi /mnt/raspios/config.txt`
6. Unmount the device and reboot:\
   `umount /dev/sda1`\
   `tpi power off -n 1`\
   `tpi power on -n 1`
