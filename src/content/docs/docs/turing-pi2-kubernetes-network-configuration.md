---
title: "Network Configuration"
description: "Networking within Kubernetes can be intricate, involving both internal and external communication. For simplicity and containment within the cluster, we'll…"
head:
  - tag: title
    content: "How to Configure Network For Turing Pi2 Kubernetes Cluster | Turing Pi Docs"
lastUpdated: 2025-11-12
---

Networking within Kubernetes can be intricate, involving both internal and external communication. For simplicity and containment within the cluster, we'll use an internal networking solution to assign IP addresses directly to services, bypassing the need for external DNS servers or load balancers.

**Please ensure that Helm has been installed before proceeding with this section.**

## MetalLB

MetalLB is a Kubernetes-based load balancer that assigns IP addresses to services, facilitating network requests to those IPs. This allows services to be externally exposed, improving accessibility and scalability. MetalLB is particularly beneficial when a Kubernetes cluster lacks an external load balancer or when the cluster administrator prefers to use a custom load balancing solution.

To understand more about MetalLB, refer [HERE](https://metallb.universe.tf/).

**MetalLB should be installed only on your main control node.**

```bash
# Add MetalLB repository to Helm
helm repo add metallb https://metallb.github.io/metallb

# Check the added repository
helm search repo metallb
```

Example of "helm search repo metallb"

```bash
root@cube01:~# helm search repo metallb  
NAME             CHART VERSION  APP VERSION  DESCRIPTION   
metallb/metallb  0.13.7         v0.13.7      A network load-balancer implementation for Kubernetes...
```

Install MetalLB

```bash
helm upgrade --install metallb metallb/metallb --create-namespace \
--namespace metallb-system --wait
```

The above command returns:

```bash
Release "metallb" does not exist. Installing it now.  
NAME: metallb  
LAST DEPLOYED: Tue Jan 31 14:28:54 2023  
NAMESPACE: metallb-system  
STATUS: deployed  
REVISION: 1  
TEST SUITE: None  
NOTES:  
MetalLB is now running in the cluster.
```

Now that MetalLB is installed, we need to assign an IP range for it. In this case, we allow MetalLB to use the range 10.0.0.70 to 10.0.0.80.

```bash
cat << 'EOF' | kubectl apply -f -
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: default-pool
  namespace: metallb-system
spec:
  addresses:
  - 10.0.0.70-10.0.0.80
---
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: default
  namespace: metallb-system
spec:
  ipAddressPools:
  - default-pool
EOF
```

The above command returns:

```bash
ipaddresspool.metallb.io/default-pool created
l2advertisement.metallb.io/default created
```

## Traefik

Traefik is an open-source reverse proxy and load balancer used extensively in Kubernetes environments. Traefik intelligently routes incoming requests to appropriate microservices based on factors such as domain name, path, and other attributes. It works closely with Kubernetes and other cloud-native tools to provide service discovery, automatic SSL certificate management, and request routing based on custom rules. Traefik is pre-installed with K3s.

However, to utilize Traefik, a working DNS server external to the Kubernetes cluster is required. For local testing, the /etc/hosts file can be modified to act as a faux DNS server.

The host file is located at:

* Mac: /private/etc/hosts
* Windows: c:\\windows\\system32\\drivers\\etc\\hosts
* Linux: /etc/

hosts

You can edit this file to add an entry like:

```bash
10.0.0.70 turing-cluster turing-cluster.local
```

Now, when you enter **[https://turing-cluster.local](https://turing-cluster.local)** in your browser, you should be redirected to a 404 page of Traefik.

:::caution
Remember this will work only on machines where the host file has been modified. For network-wide accessibility, a DNS server is required, and all PCs need to be aware of this DNS server.
:::
