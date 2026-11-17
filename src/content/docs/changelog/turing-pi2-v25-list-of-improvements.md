---
title: "Turing PI V2.5 Changelog"
head:
  - tag: title
    content: "Turing PI V2.5 Changelog | Changelog | Turing Pi Docs"
lastUpdated: 2026-09-03
---

**The list of improvements compared to the Turing Pi2 v2.4:**

* Improved internal USB connections:
  * The Mini PCIe USB interface (used, for example, by some WiFi cards and modems) is now connected to the USB1 interface - this change allows Turing RK1 and Nvidia Jetson modules to utilize the USB interface in the Mini PCIe slot and was required to improve the node flashing experience in Node 1 and Node 2 (occasional inability to flash the modules in Node 1 and rarely in Node 2); This change affects Raspberry Pi CM4 which only contains a single USB interface (USB0) - RPi CM4 will no longer be able to use Mini PCIe modules that communicate using USB
  * Added internal USB hub connected to USB0 interfaces of all nodes - this change will expose all the modules set into flashing mode to the BMC or the USB\_OTG port, which means an ability to flash multiple modules at once and improves USB signal integrity
  * Replaced USB-A connector for the USB\_OTG function (node module flashing) with USB-C connector - will let flash the modules using USB A-to-C  or USB C-to-C cables - USB A-to-A cable is no longer needed
  * Added USB-A connector connected to the USB2 interface (USB0 interface for Raspberry Pi CM4 module while in USB host mode) of Node 1 - lets you connect USB keyboard and mouse (and other peripherals) to Node 1, useful, for example, while using Node 1 in a desktop mode with an HDMI screen connected
* Added onboard USB-UART converter for the BMC - lets you connect to the BMC's UART using a USB-C cable (you no longer need an external USB-UART converter); Applies only to the BMC UART, node UARTs remain accessible via UART headers
* Added new 8-pin connector exposing I²C and 4 GPIO pins as well as 3V3 and GND - the main purpose for this header is to connect an I²C screen and 4 buttons (a relevant product will be released later), but it can also be used for other purposes
* Added an ability for the nodes to stay powered on when the BMC restarts
* Replaced soldered Mini PCIe and M.2 studs with removable counterparts - improves compatibility with full-size Mini PCIe modules as well as 2260 and double-sided M.2 drives (6x M2 screws will also be included with the board - one for each M.2 and Mini PCIe slot)
* Improved HDMI screen compatibility - adds higher-resolution screen support (especially noticeable for 4K screens connected to the Nvidia Jetson modules)
* Improved SATA compatibility in Node 3 - helps with operating systems that could not previously boot on the modules placed in Node 3 due to unconnected #clkreq signal (mostly a case with Talos running on Raspberry Pi CM4)
* Added case PWM header controlled by the BMC
* Doubled the BMC flash capacity from 128 MB to 256 MB - to be used to extend the user space (can also be used to store more firmware versions)
* Added FEL Mode button - makes it easier to recover from unsuccessful firmware upgrade
* Added switch for toggling the embedded network switch mode between managed and unmanaged
* Improved node power delivery for better efficiency - slightly reduces power consumption and generated heat, the changes will also prevent the whispering noise that could be heard on some of the boards with modules powered on
* Improved the GPIO header compatibility - changed pin 17 function from GND to 3.3V to match other implementations
* The RTC battery fix is integrated with the board and the RTC Battery Adapter Board is no longer needed
