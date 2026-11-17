---
title: "Usage"
description: "The syntax takes the form of tpi , see the relevant --help listing:"
head:
  - tag: title
    content: "Usage | TPI | Turing Pi 2 | Turing Pi Docs"
lastUpdated: 2025-11-12
---

The syntax takes the form of `tpi <command> <options>`, see the relevant `--help` listing:

```shell
$ tpi --help
CLI tool to control a Turing-Pi board

Usage: tpi [OPTIONS] [COMMAND]

Commands:
  power     Power on/off or reset specific nodes
  usb       Change the USB device/host configuration. The USB-bus can only be routed to one node
                simultaneously
  firmware  Upgrade the firmware of the BMC
  flash     Flash a given node
  eth       Configure the on-board Ethernet switch
  uart      Read or write over UART
  advanced  Advanced node modes
  info      Print turing-pi info
  reboot    Reboot the BMC chip. Nodes will lose power until booted!
  help      Print this message or the help of the given subcommand(s)

Options:
      --host <HOST>        Specify the Turing-pi host to connect to. Note: IPv6 addresses must be
                           wrapped in square brackets e.g. `[::1]` [default: turingpi.local]
      --port <PORT>        Specify a custom port to connect to
      --user <USER>        Specify a user name to log in as. If unused, an interactive prompt will
                           ask for credentials unless a cached token file is present
      --password <PASS>    Same as `--username`
      --json               Print results formatted as JSON
  -a <API_VERSION>         Force which version of the BMC API to use. Try lower the version if you
                           are running older BMC firmware [default: v1-1] [possible values: v1,
                           v1-1]
  -g <gen completion>      [possible values: bash, elvish, fish, powershell, zsh]
  -h, --help               Print help
  -V, --version            Print version
```

Each command has its own set of options and a usage listing:

```shell
$ tpi usb
Change the USB device/host configuration. The USB-bus can only be routed to one node simultaneously

Usage: tpi usb [OPTIONS] <MODE>

Arguments:
  <MODE>  specify which mode to set the given node in [possible values: device, host, status]

Options:
  -b, --bmc              instead of USB-A, route the USB-bus to the BMC chip
  -n, --node <NODE>      [possible values: 1-4]
      --host <HOST>      Specify the Turing-pi host to connect to. Note: IPv6 addresses must be
                         wrapped in square brackets e.g. `[::1]` [default: turingpi.local]
      --port <PORT>      Specify a custom port to connect to
      --user <USER>      Specify a user name to log in as. If unused, an interactive prompt will ask
                         for credentials unless a cached token file is present
      --password <PASS>  Same as `--username`
      --json             Print results formatted as JSON
  -a <API_VERSION>       Force which version of the BMC API to use. Try lower the version if you are
                         running older BMC firmware [default: v1-1] [possible values: v1, v1-1]
  -h, --help             Print help (see more with '--help')
  -V, --version          Print version
```

Note that a required argument `<MODE>` was not provided, hence a help text was printed. Same can also be accomplished by invoking `tpi <command> --help`.

Starting with version 2.0.0 of the firmware, only authenticated users can issue commands on the BMC. That means you can either provide one or both credentials on the command line, or none at all, in which case you will be asked to enter username and password interactively:

```shell
$ tpi power status                              # interactive prompt
User: root
Password:
node1: off
node2: off
node3: off
node4: off
$ tpi power status --user root                  # only password is entered at a prompt
Password:
node1: off
[..]
$ tpi power status --user root --password pass  # no credentials are requested interactively
node1: off
[..]
```

When you provide both credentials interactively, an authentication token is stored to a file so that you would not need to enter them again. This token is valid for a configurable amount of time, by default 3 hours. You can change this duration by editing bmcd's configuration file found in your BMC at `/etc/bmcd/config.yaml` in `authentication.token_expires` value.

The file with an authentication token called `tpi_token` is stored in these directories:

| Platform | Value                             | Example                          |
| :------- | :-------------------------------- | :------------------------------- |
| Linux    | $XDG\_CACHE\_HOME or $HOME/.cache | /home/alice/.cache               |
| macOS    | $HOME/Library/Caches              | /Users/Alice/Library/Caches      |
| Windows  | \{FOLDERID\_LocalAppData}         | C:\\Users\\Alice\\AppData\\Local |
