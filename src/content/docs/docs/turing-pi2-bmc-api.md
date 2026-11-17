---
title: "BMC API"
description: "The system management daemon of the BMC (bmcd) exposes an API that any application can talk to,\\ including the provided Web UI and the tpi tool. This…"
head:
  - tag: title
    content: "BMC API | Turing Pi2 | Turing Pi Docs"
lastUpdated: 2025-11-12
---

## Introduction

The system management daemon of the BMC (bmcd) exposes an API that any application can talk to,\
including the provided Web UI and the `tpi` tool. This article documents the API in version 2.0.3\
of the firmware.

## Authentication

Starting with version 2.0.0, all requests must be authenticated with one of the two methods:

* Bearer token

  To use token-based authentication, first issue a POST to `/api/bmc/authenticate` with user credentials:

  `curl 'https://turingpi.local/api/bmc/authenticate' -X POST -d '{"username":"root", "password":"turing"}' -k`

  In a response you will receive a bearer token that is valid for a predetermined amount of time,\
  as specified in bmcd's configuration file (`/etc/bmcd/config.yaml`). Next, use the token to\
  authenticate your requests:

  `curl 'https://turingpi.local/api/bmc?opt=get&type=usb' --header "Authorization: Bearer longtokenhere" -k`

* Basic

  To use basic authentication, encode the credentials in base64:

  `echo -n 'root:turing' | base64`

  You can then use it to authenticate requests:

  `curl 'https://turingpi.local/api/bmc?opt=get&type=usb' --header 'Authorization: Basic base64digest' -k`

## Endpoints

The API accepts input in the form of '/api/bmc?opt=*opt*\&type=*type*&*args*' and returns JSON\
responses as `[{ "response": ... }]`. The format is constructed in this way to preserve backwards\
compatibility. All methods below are of type GET.

#### `usb_boot`

Enable USB boot mode for a specified node. For Raspberry Pi CM4s, this means pulling pin 93 (`nRPIBOOT`) low.

`/api/bmc?opt=set&type=usb_boot&node=0`

#### `clear_usb_boot`

Clear USB boot status of a specified node.

`/api/bmc?opt=set&type=clear_usb_boot&node=0`

#### `network`

Reset network switch.

`/api/bmc?opt=set&type=network`

#### `nodeinfo`

Deprecated: this functionality is removed in versions ≥2.0.0 of the firmware and replaced with empty\
output. Previous versions would listen to nodes' serial output (disabled by default in Raspberry Pi\
OS) and try to unreliably deduce a type of a node.

#### `node_to_msd`

Reboot a node into USB Mass Storage Device (MSD) mode.

`/api/bmc?opt=set&type=node_to_msd&node=0`

#### `other`

Get system & daemon information.

Returns:

* `api`: API version
* `version`: daemon version
* `buildtime`: UTC+0 timestamp of build date
* `ip`: IPv4 address of eth0
* `mac`: MAC address of eth0

`/api/bmc?opt=get&type=other`

#### `power`

* Opt = set

  Set power status of specified nodes.

  `/api/bmc?opt=power&type=set&node1=0&node3=1`

  This example turns node 1 off and node 3 on.

* Opt = get

  Get power status of nodes.

  `/api/bmc?opt=get&type=power`

  Returns powered-on status of nodes 1 to 4.

#### `reboot`

Reboot the BMC chip.

`/api/bmc?opt=set&type=reboot`

#### `reload`

Restart the system management daemon.

`/api/bmc?opt=set&type=reload`

#### `reset`

Reboot a specified node.

`/api/bmc?opt=set&type=reset`

#### `sdcard`

Get microSD card info.

`/api/bmc?opt=get&type=sdcard`

Returns:

* `total`: total storage space, in bytes
* `use`: used storage space
* `free`: free storage space

#### `uart`

* Opt = set

  Write data over UART.

  Parameter: `cmd`: data to write

  `/api/bmc?opt=set&type=uart&cmd=echo%20hi`

* Opt = get

  Read buffered UART data, clearing output buffer.

  Parameter: `encoding` (optional): convert from this encoding to UTF-8 for transmission.\
  Acceptable values: `utf8` (default), `utf16`, `utf16le`, `utf16be`, `utf32`, `utf32le`, `utf32be`.

  `/api/bmc?opt=get&type=uart`

#### `usb`

* Opt = set

  Set USB routing to/from a specified node.

  Parameters:

  * `node`: affected node
  * `mode`: integer describing mode and route

  | `mode` | Mode           | Route |
  | ------ | -------------- | ----- |
  | 0      | Host           | USB-A |
  | 1      | Device         | USB-A |
  | 2      | Flash (Host)   | USB-A |
  | 3      | Flash (Device) | USB-A |
  | 4      | Host           | BMC   |
  | 5      | Device         | BMC   |
  | 6      | Flash (Host)   | BMC   |
  | 7      | Flash (Device) | BMC   |

  `/api/bmc?opt=set&type=usb&mode=0&node=0`

* Opt = get

  Get USB mode.

  Returns:

  * `mode`: USB mode (Device/Host)
  * `node`: active node
  * `route`: where the USB is routed to: the BMC or the USB-2.0 connector on the board.

  `/api/bmc?opt=get&type=usb`

#### `info`

Get more detailed system information.

Returns:

* `ip`: get device names, IP and MAC addresses of all non-loopback and non-local interfaces
* `storage`: get total and free bytes of storage space of the BMC and microSD card

`/api/bmc?opt=get&type=info`

#### `about`

Get more detailed daemon information.

Returns:

* `api`: API version
* `version`: daemon version
* `buildtime`: UTC+0 timestamp of build date
* `buildroot`: buildroot version
* `build_version`: firmware version

`/api/bmc?opt=get&type=about`

#### `flash` / `firmware`

`flash`: Flash a specified node with an OS image.

`firmware`: Update firmware of the BMC.

Parameters:

* `length`: image length, in bytes
* `local`: if present, indicates that image file will be read directly from the locally-accessible\
  filesystem, with path given in `file`.

Returns: `handle`: handle that can be used to:

* upload data (`/api/bmc/upload/{handle}`)
* cancel operation (`/api/bmc/upload/{handle}/cancel`)
* retrieve current progress (`/api/bmc?opt=get&type=flash`)
