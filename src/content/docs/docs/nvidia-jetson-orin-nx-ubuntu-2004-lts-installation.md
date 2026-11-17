---
title: "Ubuntu 20.04 LTS"
description: "To install Ubuntu 20.04 LTS, first, download the installation ISO file."
head:
  - tag: title
    content: "Ubuntu 20.04 LTS How To Install Onto Nvidia Jetson Orin / Nano NX | Turing Pi Docs"
lastUpdated: 2025-11-12
---

## ISO Image

To install Ubuntu 20.04 LTS, first, download the [installation ISO file](https://releases.ubuntu.com/focal/ubuntu-20.04.6-desktop-amd64.iso).

## Bare-metal installation

If you are installing it on the PC/laptop directly, you can use these guides to prepare a bootable Pendrive:

* Windows: [https://ubuntu.com/tutorials/create-a-usb-stick-on-windows#1-overview](https://ubuntu.com/tutorials/create-a-usb-stick-on-windows#1-overview)
* Ubuntu: [https://ubuntu.com/tutorials/create-a-usb-stick-on-ubuntu#1-overview](https://ubuntu.com/tutorials/create-a-usb-stick-on-ubuntu#1-overview)
* MacOS: [https://ubuntu.com/tutorials/create-a-usb-stick-on-macos#1-overview](https://ubuntu.com/tutorials/create-a-usb-stick-on-macos#1-overview)

Boot your PC/laptop from the pen drive.

## Virtual Machine using VMWare Player

If you are using VMWare Player to install Ubuntu 20.04 LTS and you haven't already set the ISO image, run the VMWare Player, right-click on your Ubuntu virtual machine, and click "Settings". Click on the CD/DVD device, check it's connected, and browse for the downloaded Ubuntu ISO image:

![](../../../assets/img/2ecb15e-11526637119133.png)

Click on "Close" and power on the virtual machine and wait for it to load the Ubuntu installation.

## Installing Ubuntu 20.04 LTS

Installing Ubuntu 20.04 is pretty straightforward. On most of the screens, the default settings would be enough. Start with clicking on "Install ubuntu":

![](../../../assets/img/3f605eb-11526632744861.png)

Choose your keyboard layout

![](../../../assets/img/558192a-11526632746269.png)

We only need the minimal installation:

![](../../../assets/img/f6485be-11526637126301.png)

Choose to erase the disk - it won;t erase any of your disks, just a virtual disk created for this virtual machine:

![](../../../assets/img/3aa406b-11526637128093.png)

![](../../../assets/img/4632587-11526632754461.png)

Choose your timezone:

![](../../../assets/img/341a852-11526637132061.png)

Set your name, the computer name (not important), and set the password. Setting the OS to log in automatically is handy and recommended, but not necessary:

![](../../../assets/img/e2596b0-11526637133725.png)

Ubuntu will now get installed what's going to take a few minutes:

![](../../../assets/img/94425e7-11526632758941.png)

After the installation is finished - restart the virtual machine:

![](../../../assets/img/345b435-11526632762269.png)

When asked to remove the installation media either disconnect the pendrive if you are using bare-metal installation or disconnect CD/DVD device in case of using a virtual machine:

![](../../../assets/img/6224082-11526632764829.png)

You can skip this step if you do not want to connect any of your accounts:

![](../../../assets/img/2499e0a-11526632767133.png)

Click on "Next":

![](../../../assets/img/adfc8eb-11526632769437.png)

If you do not want the usage data to be sent to Canonical, check the option to not do so. Click on "Next":

![](../../../assets/img/3978821-11526637145757.png)

And click on "Next" again:

![](../../../assets/img/d500815-11526632774173.png)

Click on "Done":

![](../../../assets/img/eb9a599-11526632776221.png)

If there's an upgrade available, you can skip it for now:

![](../../../assets/img/0ddc3d3-11526632779677.png)
