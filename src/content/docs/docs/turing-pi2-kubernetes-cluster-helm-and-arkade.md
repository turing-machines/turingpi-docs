---
title: "Helm and Arkade"
description: "Helm is a Kubernetes package manager that streamlines the management and distribution of applications, making the process simpler and more organized. It…"
head:
  - tag: title
    content: "Helm and Arkade | Kubernetes | Advanced Topics | Turing Pi Docs"
lastUpdated: 2025-11-12
---

## Helm

Helm is a Kubernetes package manager that streamlines the management and distribution of applications, making the process simpler and more organized. It provides a mechanism to package, configure, and deploy applications consistently and with version control. Helm simplifies the update and rollback procedures, and facilitates the sharing of your applications.

To install Helm, we will follow the official installation process detailed [**HERE**](https://helm.sh/docs/intro/install/).

For further details on Helm's functionality, refer to [**HERE**](https://helm.sh/).

**Execute the following commands on your Master node only:**

```bash
# Ensure GIT is installed
apt -y install git  

# Fix kubeconfig file to prevent Helm errors
export KUBECONFIG=~/.kube/config  
mkdir ~/.kube 2> /dev/null  
sudo k3s kubectl config view --raw > "$KUBECONFIG"  
chmod 600 "$KUBECONFIG"  
echo "KUBECONFIG=$KUBECONFIG" >> /etc/environment  

# Switch to home directory
cd

# Create a directory for Helm and navigate into it
mkdir helm  
cd helm  

# Download Helm installer
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3  

# Modify permissions for execution
chmod 700 get_helm.sh  

# Install Helm
./get_helm.sh  

# Verify Helm installation
helm version
```

## Arkade

Arkade is a one-liner tool that simplifies the installation of Kubernetes applications on any cluster. It automates the installation process, making it quicker and easier to run desired applications on a Kubernetes cluster. With Arkade, manual installation, configuration, and dependency management are things of the past.

To install Arkade, we will follow the official installation process detailed [**HERE**](https://github.com/alexellis/arkade#getting-arkade).

For more information on Arkade's features, refer to [**HERE**](https://github.com/alexellis/arkade#usage-overview).

**Execute the following commands on your Master node only:**

```bash
# Install Arkade
curl -sLS https://get.arkade.dev | sudo sh 

# Verify Arkade installation
arkade version
```
