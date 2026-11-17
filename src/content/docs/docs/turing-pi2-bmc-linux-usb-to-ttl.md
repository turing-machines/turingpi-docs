---
title: "Linux USB to TTL"
head:
  - tag: title
    content: "Linux to TTL Linux | Turing Pi2 | Turing Pi Docs"
lastUpdated: 2025-11-12
---

**Step 1: Connect USB to TTL Converter Cable** [(see Windows USB to TTL)](/docs/windows-usb-to-ttl)\
Connect the USB to TTL converter cable to your computer's USB port and to the serial port on the BMC (Baseboard Management Controller). This will allow you to establish a direct communication link with the BMC.

**Step 2: Identify the Serial Port**\
Open a terminal window on your computer. Use the `dmesg` command to identify the name of the serial port that the USB to TTL converter cable is connected to. It should appear as something like `/dev/ttyUSB0` or `/dev/ttyACM0`. Alternatively, find the symlink in `/dev/serial/by-id/`.

**Step 3: Open a Screen Session**\
Using the terminal, employ the `screen` or `picocom` commands to initiate a session to the identified serial port. Both programs should be easily installable from the system's package manager and require root privileges. Assuming the serial device is `/dev/ttyUSB0` (substitute as necessary), the command would look something like this:

* screen: `sudo screen /dev/ttyUSB0 115200`\
  If you are prompted, press the "Enter" key to confirm agreement with the device's baud rate, which should be set at 115200. This sets the communication speed between your computer and the BMC.
* picocom: `sudo picocom /dev/ttyUSB0 -b 115200`\
  To remap the escape sequence, e.g. to avoid conflicts when nesting in a tmux session, provide an additional argument `--escape <char>`, such as `-e b`. Exiting the program thus becomes a key combination `Ctrl-b` `Ctrl-x`.

**Step 4: Monitor System Messages**\
After connecting, you should be able to view the system's boot process, kernel messages, and other debug information directly in the terminal window.

**Step 5: Access BMC's Command Line Interface (CLI)**\
To reach the BMC's command line interface, you will be asked to enter the appropriate login credentials when prompted. This could be a username and password specific to your device or system.

**Step 6: Execute Commands and Make Configuration Changes**\
Once logged into the BMC's CLI, you are now able to run commands and make configuration changes as necessary, based on your specific requirements or tasks at hand.
