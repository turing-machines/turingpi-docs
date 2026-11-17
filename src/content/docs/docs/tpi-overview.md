---
title: "Overview"
description: "The tpi is a tool designed to facilitate interaction with your Turing Pi 2 board. It comes bundled with the BMC firmware and can also be installed on your…"
head:
  - tag: title
    content: "Overview | TPI | Turing Pi 2 | Turing Pi Docs"
lastUpdated: 2025-11-12
---

The [`tpi`](https://github.com/turing-machines/tpi) is a tool designed to facilitate interaction with your Turing Pi 2 board. It comes bundled with the BMC firmware and can also be installed on your Windows/macOS/Linux PC.

The tool can be used from within the BMC (for example, via SSH):

```shell
$ ssh root@turingpi.local
# tpi power on --node 1
# tpi usb --mode host --node 1
```

Or directly from your personal computer. In this case, `tpi` will try to connect to the board at the address of `turingpi.local`, which is the default host name through which the Turing Pi 2 is accessible on the local network. If you need to change the address, use the `--host` option:

```shell
$ tpi power on                          # will try to connect to `turingpi.local`
$ tpi --host mycluster2.local power on  # custom hostname
$ tpi --host 192.168.1.42 power on      # explicit IP address
```
