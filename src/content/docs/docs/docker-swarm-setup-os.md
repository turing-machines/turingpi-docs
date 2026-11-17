---
title: "Setup OS"
description: "The process for setting up the operating system for Docker Swarm is similar to the process of setting up the operating system for a Kubernetes cluster, as…"
head:
  - tag: title
    content: "Setup OS For Docker Swarm Using Turing Pi2 | Turing Pi Docs"
lastUpdated: 2025-11-12
---

The process for setting up the operating system for Docker Swarm is similar to the process of setting up the operating system for a Kubernetes cluster, as outlined in our [Kubernetes](/docs/how-to-plan-kubernetes-installation). While following this guide, simply make **one exception** when editing the **dietpi.txt** file.

When configuring software to install **in the dietpi.txt** file, it is important to **include** the following line among the lines that begin with "AUTO\_SETUP\_INSTALL\_SOFTWARE\_ID".

Note, you can find the list of IDs available for automated installation [**HERE**](https://github.com/MichaIng/DietPi/wiki/DietPi-Software-list).

* ID 134 - Docker Compose
* ID 162 - Docker
* ID 17 - Git

```
AUTO_SETUP_INSTALL_SOFTWARE_ID=134  
AUTO_SETUP_INSTALL_SOFTWARE_ID=162  
AUTO_SETUP_INSTALL_SOFTWARE_ID=17
```

:::note
When you can SSH to each node, please return here to this guide and continue with Swarm Deploy.
:::
