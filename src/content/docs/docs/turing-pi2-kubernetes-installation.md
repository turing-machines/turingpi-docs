---
title: "Kubernetes Installation"
description: "We have opted for K3s, a lightweight Kubernetes distribution, for our setup. This decision is driven by K3s' ability to deliver a full-fledged Kubernetes…"
head:
  - tag: title
    content: "Kubernetes Installation For Turing Pi2 Cluster | Turing Pi Docs"
lastUpdated: 2025-11-12
---

We have opted for K3s, a lightweight Kubernetes distribution, for our setup. This decision is driven by K3s' ability to deliver a full-fledged Kubernetes experience while demanding lesser resources in terms of CPU and RAM compared to other distributions.

Here is our nodes' reference for this section:

* **Node1** - 10.0.0.60 - Serves as both a **Kubernetes controller** and worker node
* **Node2** - 10.0.0.61 - Serves as a Kubernetes worker node
* **Node3** - 10.0.0.62 - Functions as a Kubernetes worker node and an **NFS server**
* **Node4** - 10.0.0.63 - Acts as a Kubernetes worker node

## Master Node Initialization

Using your preferred SSH client, **log into Node1**. Execute the following command:

```bash
curl -sfL https://get.k3s.io | sh -s - --write-kubeconfig-mode 644 --disable servicelb --token myrandompassword --node-ip 10.0.0.60 --disable-cloud-controller --disable local-storage
```

Let's dissect this command:

* **--write-kubeconfig-mode 644** - Specifies the permissions for the kubeconfig file. While optional, it's needed if you plan to later connect to the Rancher manager.
* **--disable servicelb** - Disables the service load balancer. We will use Metallb instead.
* **--token** - Defines the token used to connect to the K3s master node. Choose a strong random password and keep it safe.
* **--node-ip** - Binds the K3s master node to a specific IP address.
* **--disable-cloud-controller** - Turns off the K3s cloud controller, which we don't need for this setup.
* **--disable local-storage** - Deactivates the K3s local storage as we'll set up Longhorn and NFS as storage providers instead.

Post-installation, verify the installation success with `kubectl get nodes`, which should return an output similar to:

```bash
root@cube01:~# kubectl get nodes  
NAME   STATUS ROLES                AGE    VERSION  
cube01 Ready control-plane,master 6m22s v1.25.6+k3s1
```

## Worker Nodes Addition

Next, add the worker nodes. SSH into Node2 to Node4 and run the following command:

```bash
curl -sfL https://get.k3s.io | K3S_URL=https://10.0.0.60:6443 K3S_TOKEN=myrandompassword sh -
```

You can run this command simultaneously on all nodes. After the script completes, execute `kubectl get nodes` **on Node1**. This should yield:

```bash
root@cube01:~# kubectl get nodes  
NAME   STATUS ROLES  AGE  VERSION  
cube01 Ready control-plane,master 43m v1.25.6+k3s1  
cube04 Ready &lt;none&gt; 38s v1.25.6+k3s1  
cube02 Ready &lt;none&gt; 35s v1.25.6+k3s1  
cube03 Ready &lt;none&gt; 34s v1.25.6+k3s1
```

## Node Labeling

Although optional, labeling nodes is recommended to represent the "worker" role instead of "&lt;none&gt;". Labels are more than cosmetic; they help specify a node for running certain workloads. For example, a specialized hardware node, like a Jetson Nano, can be labeled, and applications that require

such hardware can be directed to run exclusively on that node.

Label your nodes with the key:value pair kubernetes.io/role=worker to get cleaner output from `kubectl get nodes`.

```bash
kubectl label nodes cube01 kubernetes.io/role=worker  
kubectl label nodes cube02 kubernetes.io/role=worker  
kubectl label nodes cube03 kubernetes.io/role=worker  
kubectl label nodes cube04 kubernetes.io/role=worker
```

Another useful label is to denote the node-type as "worker" for deploying applications. "node-type" is an arbitrary key name and can be changed as needed.

```bash
kubectl label nodes cube01 node-type=worker  
kubectl label nodes cube02 node-type=worker  
kubectl label nodes cube03 node-type=worker  
kubectl label nodes cube04 node-type=worker
```

If your Node4 is a Nvidia Jetson, you might label it as node-type=jetson, allowing specific workloads (like ML containers) to run exclusively on that node.

After labeling, your nodes should resemble:

```bash
root@cube01:~# kubectl get nodes  
NAME   STATUS ROLES AGE VERSION  
cube01 Ready control-plane,master,worker 52m v1.25.6+k3s1  
cube02 Ready worker 10m v1.25.6+k3s1  
cube03 Ready worker 10m v1.25.6+k3s1  
cube04 Ready worker 10m v1.25.6+k3s1
```

To list all labels per node, use:

```bash
kubectl get nodes --show-labels
```

:::tip
Well done! You've successfully set up a Kubernetes cluster. However, there are additional steps to improve the cluster's functionality. Continue reading our guide for these next steps.
:::
