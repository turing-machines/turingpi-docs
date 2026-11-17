---
title: "MacOS USB to TTL"
head:
  - tag: title
    content: "MacOS USB to TTL | BMC | Turing Pi 2 | Turing Pi Docs"
lastUpdated: 2025-11-12
---

1. Connect the USB to TTL converter cable to your computer's USB port and to the serial port on the BMC.
2. Open the terminal window and use the `ls /dev/cu.*` command to determine the name of the serial port that the USB to TTL converter cable is connected to. It should be something like `/dev/cu.usbserial` or `/dev/cu.usbmodem`
3. Use the `screen` command to open a session on the serial port. For example: `screen /dev/cu.usbserial 115200` or `screen /dev/cu.usbmodem 115200`
4. If prompted, press enter to agree to the device's baud rate, which is 115200.
5. You should now be able to view the system's boot process, kernel messages, and other debug information in the terminal window.
6. To access BMC's command line interface, you will need to enter the appropriate login credentials when prompted.
7. Once you are logged in, you can run commands and make configuration changes as necessary.

:::note
On macOS, you may also use serial terminal software such as CoolTerm, Serial, or ZTerm.
:::
