---
title: "VMWare Player"
description: "To be able to flash the Orin modules, you need Ubuntu 20.04 LTS operating system. If you do not have a PC or laptop running this exact version of Ubuntu…"
head:
  - tag: title
    content: "VMWare Player For Nvidia Jetson Orin / Nano NX | Turing Pi Docs"
lastUpdated: 2025-11-12
---

## Installation

To be able to flash the Orin modules, you need Ubuntu 20.04 LTS operating system. If you do not have a PC or laptop running this exact version of Ubuntu, you can use a virtual machine. We tested VMWare Player that runs both on Windows and Linux, but other virtualization software that lets you pass the USB device into the VM should work too.

Download the [VMWare Player](https://www.vmware.com/go/getplayer-win) for your operating system and install it with the default options.

## USB settings

While not necessary, it is recommended to set the USB to connect to the virtual machine by default (otherwise you'll have to react to the dialog boxes popping in asking you what to do with a new USB device, and the flashing process will cause the USB device to disconnect and connect again multiple times and even change the USB device at some point):

![](../../../assets/img/1320efa-11525700970653.png)

![](../../../assets/img/c9ee40a-11525730576285.png)

## Virtual Machine Creation

Now you can create a virtual machine that we'll use to install the required operating system. Start with creating a virtual machine:

![](../../../assets/img/3539580-11526170974365.png)

Check that you'll install the operating system later:

![](../../../assets/img/e780fb2-11526197964573.png)

Choose Ubuntu as the operating system:

![](../../../assets/img/bb10c97-11526197967005.png)

Name your virtual machine and set where you are going to store its files (up to about 60 GB):

![](../../../assets/img/030cebc-11526197969309.png)

Choose the disk size. 120 GB ensures the will be enough space:

![](../../../assets/img/ad8ea4b-11526170985757.png)

We need to set some hardware customization:

![](../../../assets/img/21d600c-11526170988829.png)

Set the network type from NAT to Bridged and click on the "Configure Adapters":

![](../../../assets/img/90ecba3-11526170990493.png)

Make sure only your main network card (either LAN or WiFi) is checked here and click "OK":

![](../../../assets/img/4338448-11526197980189.png)

This step can be performed later, but if you have an operating system ISO image already downloaded, you can set it here already:

![](../../../assets/img/2ed1394-11526170995869.png)

And that's all:

![](../../../assets/img/0aa5cd8-11526170998813.png)

Now you should see your new virtual machine created. You can run it by double-clicking on its name or by clicking the name and clicking on the "Play virtual machine" on the right:

![](../../../assets/img/cd0bb48-11526170999709.png)
