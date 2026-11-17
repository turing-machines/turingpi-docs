---
title: "The Plan"
description: "Having a well-defined plan and clear objectives is crucial, regardless of whether you are setting up a Kubernetes cluster or a simpler solution like Docker…"
head:
  - tag: title
    content: "How To Plan Docker Swarm Deployment | Turing Pi Docs"
lastUpdated: 2025-11-12
---

Having a well-defined plan and clear objectives is crucial, regardless of whether you are setting up a Kubernetes cluster or a simpler solution like Docker Swarm. Both systems have specific requirements that need to be met, and choosing the right hardware solution can greatly ease this process. In particular, the Turing Pi V2 board may offer a convenient and effective solution for fulfilling some of these requirements.

## Docker Swarm

Docker Swarm is a native orchestration system for Docker containers. It allows users to manage and deploy multiple containers as a single system. Swarm uses the same API as Docker, making it familiar and easy to use for those already familiar with Docker.

On the other hand, Kubernetes is a more feature-rich and complex container orchestration system that was originally developed by Google. While Kubernetes provides a lot of features and is considered to be the industry standard, it has a steeper learning curve and may be overkill for smaller, simpler deployments.

Therefore, someone might prefer **Docker Swarm** over Kubernetes for its simplicity, ease of use, and **lower overhead** for smaller scale deployments. On the other hand, if you need advanced features and are running a large-scale deployment, Kubernetes might be the better choice.

### OS

Once more, we will utilize [**DietPi**](https://dietpi.com/) for its ease of setup. With DietPi, we can have our system up and running with minimal effort and without the need for extensive manual configuration.

### Network

Swarm offers several network drivers that determine how the network is created and how containers are connected to it. The most common network driver is the "bridge" driver, which creates a virtual network inside the Docker host and connects containers to it.

When you export your docker service in Docker Swarm, any Node in swarm can pick up the connection and relay it to the correct container. This is fine in general, however for our convenience we can use **[Keepalived](https://www.keepalived.org/).**

#### Keepalived

Keepalived is a high availability solution that monitors the health of servers in a network and automatically redirects traffic to healthy servers in case of failure. This ensures that the services provided by the servers are always available and minimizes downtime.

In simple terms, Keepalived is a tool that helps keep a service or application running by detecting when a server is not working and redirecting traffic to another server that is working. This helps ensure that the service or application is always available to users.

In our case, we will create one virtual IP that will serve as our single point of entry. This IP will always point to one of the Nodes and if one Node fails, the IP will renegotiate its routing automatically and always point to the other swarm node.

#### Layout

* **Node1** - 10.0.0.60
* **Node2** - 10.0.0.61
* **Node3** - 10.0.0.62
* **Node4** - 10.0.0.63
* **Ingress** (virtual IP) - 10.0.0.70

### Storage

While Docker Swarm does not have a built-in persistent storage feature that can handle the migration of containers between nodes, there is a third-party solution available. This solution is called **[GlusterFS](https://www.gluster.org/)**, and it provides a robust and flexible option for persistent storage in a Docker Swarm environment.

#### GlusterFS

GlusterFS is a scalable, distributed file system that allows you to store and access files across multiple servers as if they were on a single server. It provides features such as automatic data replication and data distribution across multiple nodes, allowing you to store large amounts of data and ensure high availability and data redundancy.

Compared to NFS (Network File System), GlusterFS has several advantages. GlusterFS offers better scalability, as it can easily grow and accommodate increasing storage needs by adding more nodes to the cluster. GlusterFS also provides a higher level of data protection, as it automatically replicates data across multiple nodes, reducing the risk of data loss. Additionally, GlusterFS can distribute data across nodes for improved performance, making it well-suited for high-performance storage requirements.

In summary, GlusterFS provides better scalability, data protection, and performance compared to NFS, making it a more suitable solution for enterprise-level storage needs.

While it is possible to configure GlusterFS with just one replica, which would result in data being stored on a single node, this approach is not recommended. To ensure high availability and data protection, it is advisable to have at least two replicas in a GlusterFS cluster.

In terms of storage hardware, using mini PCIe SATA cards and connecting SSD disks to three nodes is a recommended option. This provides a robust and reliable storage solution for GlusterFS. However, it's important to note that SD cards are not suitable for heavy writing and reading environments, and should not be used as the primary storage backend for GlusterFS or a Kubernetes cluster.
