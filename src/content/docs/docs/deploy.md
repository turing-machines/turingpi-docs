---
title: "Deploy"
description: "Simply log in as the root user and run the following commands to complete the process."
head:
  - tag: title
    content: "Deploy Docker Swarm To A Turing Pi2 Cluster | Turing Pi Docs"
lastUpdated: 2025-11-12
---

**On your master node**, which in this case is Node1 with IP address 10.0.0.60 and hostname cube01, the process for initializing the Docker Swarm is straightforward.

Simply log in as the root user and run the following commands to complete the process.

```
docker swarm init --advertise-addr 10.0.0.60
```

It should return us output similar to this:

```
Swarm initialized: current node (myjwx5z3m7kcrplih1yw0e2sy) is now a manager.  
  
To add a worker to this swarm, run the following command:  
  
docker swarm join --token SWMTKN-1-2gwqttpup0hllec6p6xkun8nmht4xu18g09vsxyjhlyqc9sgjw-729yfmz5rfg02eiw0537m49c1 10.0.0.60:2377  
  
To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.  
  

```

From the output, we have two important things:

* docker swarm join --token &lt;token&gt; 10.0.0.60:2377
* docker swarm join-token manager

The **first command** in this output is used to join additional **worker** nodes to your Docker Swarm cluster, while the second command will allow us to print a command to join more **managers. You can have just one manager node, but in our case it's recommended to have 3.** This is for the simple reason that when one manager fails, another manager will be elected as a leader and everything will continue working. Why would we not set 4 ? The number of managers should always be an odd number. More information can be found in official documentation [**HERE.**](https://docs.docker.com/engine/swarm/admin_guide/#operate-manager-nodes-in-a-swarm)

You can always use command:

```
docker swarm join-token worker
```

To get the original worker token command.

## Join managers

It is important to note that the role of Master and Worker nodes in Docker Swarm is distinct from their Kubernetes counterparts. In Docker Swarm, any node can be designated as a Master node, while all nodes are considered Worker nodes. This differs from the way these roles are assigned in Kubernetes, and highlights the flexibility and scalability of Docker Swarm.

We will make our Node2 and Node3 also managers:

```
# Get the join command from current manager node  
docker swarm join-token manager  
# On Node2 and 3 use that command to join, in our case:  
docker swarm join --token SWMTKN-1-2gwqttpup0hllec6p6xkun8nmht4xu18g09vsxyjhlyqc9sgjw-eba5cbn1o4zv449w441bndfv0 10.0.0.60:2377
```

## Join workers

On Node4 execute following join command (Take the token from the master node)

```
root@cube04:~# docker swarm join --token SWMTKN-1-2gwqttpup0hllec6p6xkun8nmht4xu18g09vsxyjhlyqc9sgjw-729yfmz5rfg02eiw0537m49c1 10.0.0.60:2377  
This node joined a swarm as a worker.
```

## Check

On **any of the manager node**, run "docker node ls":

```
  
root@cube02:~# docker node ls  
root@cube02:~# docker node ls  
ID                        HOSTNAME STATUS AVAILABILITY MANAGER STATUS ENGINE VERSION  
myjwx5z3m7kcrplih1yw0e2sy cube01   Ready  Active       Leader         23.0.0  
hox556neondt5kloil0norswb * cube02 Ready  Active       Reachable      23.0.0  
m9a7tbcksnjhm01bs8hyertik cube03   Ready  Active       Reachable      23.0.0  
ylkhufgruwpq2iafjwsw01h4r cube04   Ready  Active                      23.0.0
```

If you are on a worker node, this command will not work. You can easily **find which node is Leader** at the moment with:

```
root@cube02:~# docker info | grep -A1 'Manager Addresses'  
Manager Addresses:  
10.0.0.60:2377
```

**To promote a worker node to a leader node** in a Docker Swarm cluster, you can run the following command in the terminal:

```
docker node promote <node-name>
```

Replace &lt;node-name&gt; with the hostname of the node you want to promote. This command will change the node's role from worker to leader, granting it additional privileges and responsibilities within the swarm. Note that in a Docker Swarm cluster, there can only be one active leader node at a time, and promoting a node to leader will demote the current leader to a worker.

## Network

**During our testing, we had issue exporting ports. Seems like the overlay ingress network that is automatically created was in the same range as the nodes.**

**Our Nodes have IPs from 10.0.0.x and the network was set to:**

```
}  
"Subnet": "10.0.0.0/8",  
"Gateway": "10.0.0.1"  
}
```

You can check that with commands:

```
root@cube01:~# docker network ls  
NETWORK ID    NAME             DRIVER         SCOPE  
c7ba0aae930a  bridge           bridge         local  
48ce906c3544  docker_gwbridge  bridge         local  
5c6001c2110e  host             host           local  
kpiocqticjlx  ingress          overlay        swarm  
fb28177a7b9a  none             null           local  
k55h53e1e97d  portainer_agent_network overlay swarmls
```

```
# Using the ID: kpiocqticjlx of ingress network.  
docker network inspect --format='{{json .IPAM.Config}}' kpiocqticjlx
```

If the range is the same as your node IPs, you need to change it.

```
docker network rm ingress  
# Create in different range  
docker network create --driver overlay --ingress --subnet 172.16.0.0/16 --gateway 172.16.0.1 ingress
```

**Restart all your nodes.**

## Done?

With that, you have successfully set up a Docker Swarm cluster. However, there are still ways to optimize and improve it. To continue learning about these possibilities, read the other sections of the guide. If you have any interesting projects utilizing the Turing Pi V2 board and Docker Swarm, feel free to share in the comment section.
