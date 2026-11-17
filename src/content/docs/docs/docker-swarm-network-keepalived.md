---
title: "Network: keepalived"
description: "We previously discussed Keepalived in our planning section, but to summarise, it enables us to use a single, shared virtual IP to access our service on…"
head:
  - tag: title
    content: "Network: keepalived | Turing Pi Docs"
lastUpdated: 2025-11-12
---

We previously discussed `Keepalived` in our planning section, but to summarise, it enables us to use a single, shared virtual IP to access our service on Docker Swarm. This eliminates the need to target individual nodes and instead allows us to target one virtual IP that is self-healing and highly available. By doing so, we no longer require an external load balancer.

## Our layout:

* **Node1** - 10.0.0.60
* **Node2** - 10.0.0.61
* **Node3** - 10.0.0.62
* **Node4** - 10.0.0.63
* **Ingress** (virtual IP - **Keepalived**) - 10.0.0.70

## Install Keepalived

**On every node:**

```
apt-get -y install keepalived
```

**On master node** (cube01) create file "/etc/keepalived/keepalived.conf"

```
global_defs {  
  router_id DOCKER_INGRESS  
}  
  
vrrp_instance VI_1 {  
  state MASTER  
  interface eth0  
  virtual_router_id 51  
  priority 100  
  advert_int 1  
  authentication {  
    auth_type PASS  
    auth_pass mypassword  
  }  
  virtual_ipaddress {  
  10.0.0.70  
  }  
}  
  

```

Keepalived configuration file consists of various parameters that define how the virtual IP address should be managed and maintained in a high availability environment. Some of the common parameters in Keepalived's configuration file include:

* **router\_id**: is a unique identifier for the keepalived instance. The identifier is used by keepalived to differentiate between multiple instances of the service running on the same system. The value of the router\_id can be any string that is unique to the keepalived instance.
* **vrrp\_instance**: defines the virtual router instance that will manage the virtual IP address.
* **interface**: specifies the network interface that will be used to manage the virtual IP address.
* **state**: defines the initial state of the virtual IP address, which can be either MASTER or BACKUP.
* **virtual\_router\_id**: a unique identifier for the virtual router instance.
* **priority**: defines the priority of the node to take over the virtual IP address. A higher value indicates a higher priority.
* **virtual\_ipaddress**: lists the virtual IP addresses that should be assigned to the node with the highest priority.
* **advert\_in**: refers to the advertisement interval. It specifies the frequency in seconds at which a keepalived instance sends gratuitous ARP announcements to update its local ARP cache table on the network.
* **auth\_pass:** is the authentication password used between the keepalived instances running on different nodes. It is used to prevent unauthorized access to the keepalived service, and to ensure that only authorized keepalived instances can modify the virtual IP configuration.

**On Node2 same file "/etc/keepalived/keepalived.conf"**

```
global_defs {  
  router_id DOCKER_INGRESS  
}  
  
vrrp_instance VI_1 {  
  state BACKUP  
  interface eth0  
  virtual_router_id 51  
  priority 90  
  advert_int 1  
  authentication {  
    auth_type PASS  
    auth_pass mypassword  
  }  
  virtual_ipaddress {  
    10.0.0.70  
  }  
}
```

We only changed two things:

* **state** to BACKUP
* **priority** to 90 from 100

**To configure nodes 3 and 4**, you'll need to make a similar configuration as the node 2. But **decrease the priority of each node** by 10. For example, node 3 would have a priority of 80, and node 4 would have a priority of 70.

**Start and enabled the service** to start at boot **on every node** (start from Node 1)

```
systemctl start keepalived  
systemctl enable keepalived
```

## Check

To check if keepalived successfully negotiated the virtual IP, you can use the `ip a` command to list the IP addresses assigned to the network interfaces. The virtual IP should be listed under the interface specified in the `interface` directive in keepalived.conf and the state should be "MASTER" on the node with the highest priority, and "BACKUP" on the other nodes. You can also check the logs in the `/var/log/syslog` or `/var/log/messages` for any error messages related to keepalived.

```
root@cube01:~# ip a show eth0  
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000  
    link/ether e4:5f:01:b7:4d:9e brd ff:ff:ff:ff:ff:ff  
    inet 10.0.0.60/24 brd 10.0.0.255 scope global eth0  
       valid_lft forever preferred_lft forever  
    inet 10.0.0.70/32 scope global eth0  
       valid_lft forever preferred_lft forever
```

You can also try to ping the virtual IP from other nodes.

```
root@cube04:~# ping -c 3 10.0.0.70  
PING 10.0.0.70 (10.0.0.70) 56(84) bytes of data.  
64 bytes from 10.0.0.70: icmp_seq=1 ttl=64 time=0.271 ms  
64 bytes from 10.0.0.70: icmp_seq=2 ttl=64 time=0.225 ms  
64 bytes from 10.0.0.70: icmp_seq=3 ttl=64 time=0.199 ms  
  
--- 10.0.0.70 ping statistics ---  
3 packets transmitted, 3 received, 0% packet loss, time 2038ms  
rtt min/avg/max/mdev = 0.199/0.231/0.271/0.029 ms
```
