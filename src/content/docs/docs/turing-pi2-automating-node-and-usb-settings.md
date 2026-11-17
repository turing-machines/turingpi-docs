---
title: "Automating Node and USB Settings"
description: "Automating operations such as powering on nodes or altering USB settings can be achieved by adding scripts to the /etc/init.d directory on the Baseboard…"
head:
  - tag: title
    content: "Automating Node And USB Settings | Turing Pi2 | Turing Pi Docs"
lastUpdated: 2025-11-12
---

Automating operations such as powering on nodes or altering USB settings can be achieved by adding scripts to the `/etc/init.d` directory on the Baseboard Management Controller (BMC). Below, we provide a detailed guide on how to accomplish this task.

## Powering On All Nodes at Startup

By default, the Turing Pi 2 doesn't power on any nodes at startup. While this can be beneficial in certain scenarios, it might not be ideal in situations like recovering from a power outage.

To alter this default behavior, a small startup script can be added. Create the file `S99zallnodeson.sh` in the `/etc/init.d` directory with the following content:

```
#!/bin/sh  

while ! netstat -tuln | grep LISTEN | grep ':80 '; do sleep 1; done

# Turn on all nodes  
tpi -p on
```

The name of the file must follow alphabetically the name `S99hello.sh` because the BMC server starts in the `S99hello.sh`. 

Make the script executable

```shell
chmod +x /etc/init.d/S99zallnodeson.sh
```

The while loop, ensure that the bmc is ready before executing the HTTP requests.

## Powering On a Specific Node at Startup

If you wish to power on a specific node at startup, utilize the script below. Create the file `S99znodeon.sh` in the `/etc/init.d `directory with the following content:

```
#!/bin/sh  
  
# Wait for the API to be ready to accept requests  
sleep 10  
  
# Power on NODE 1  
curl --location --request POST 'http://127.0.0.1/api/bmc?opt=set&type=power&node1=1'
```

Make the script executable

```shell
chmod +x /etc/init.d/S99znodeon.sh
```

Please note, we are not using `tpi` in this case. As of now, `tpi` can only power on and off all the nodes simultaneously, and not specific nodes. Instead, we are using `curl` to make a request to the `BMC API`.

## Altering Node USB Settings at Startup

The USB lanes of the Mini PCI-Express for both NODE 1 and NODE 2 are multiplexed with the USB-OTG port. **Therefore, when a USB setting is active** for either NODE 1 or NODE 2, **any USB devices connected via the Mini PCI-Express will be hidden.**

On a cold boot of the Turing Pi 2, the default setting is HOST MODE for NODE 1, which will render any Mini PCI-Express modules connected to NODE 1 that use USB unavailable.

A simple startup script can ensure that HOST MODE is automatically set for NODE 3 instead. Create the file `S92usb.sh` in the `/etc/init.d` directory with the following content:

```
#!/bin/sh  
  
# Change USB to HOST MODE for NODE 3  
tpi -u host -n 3
```

Make the script executable

```shell
chmod +x /etc/init.d/S92usb.sh
```

### Important Considerations

**Order of Execution**: If you create a script that changes the USB-OTG settings and powers on one or more nodes, ensure that you alter the USB settings before powering on the affected nodes. This sequence of operations is crucial for the proper functioning of your nodes.
