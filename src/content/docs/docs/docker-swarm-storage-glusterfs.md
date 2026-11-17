---
title: "Storage: GlusterFS"
description: "We will be using Node1 to Node3 that are equipped with SATA SSD storage (through the use of microPCIe to SATA converters). However, you can also opt for…"
head:
  - tag: title
    content: "Storage Setup Using GlusterSF On A Turing Pi2 Cluster | Turing Pi Docs"
lastUpdated: 2025-11-12
---

## Install

Install **on all nodes**:

```
apt-get -y install glusterfs-server
```

```
sudo systemctl start glusterd
sudo systemctl enable glusterd
```

## Prepare disks

We will be using Node1 to Node3 that are equipped with SATA SSD storage (through the use of microPCIe to SATA converters). However, you can also opt for using only Node3 that has built-in SATA connectors and a single disk, but it will be the sole point of failure in the system.

### Bricks

Bricks in GlusterFS are basic building blocks that represent individual disk storage. A GlusterFS storage volume is created by grouping multiple bricks together. These bricks can be located on different servers and combined to create a large and scalable distributed file system. Bricks are used to store actual data and make up the physical storage of the GlusterFS volume.

**On nodes with disks:**

Find your disk/s

```
root@cube03:~# fdisk -l  
  
Disk /dev/ram0: 4 MiB, 4194304 bytes, 8192 sectors  
Units: sectors of 1 * 512 = 512 bytes  
Sector size (logical/physical): 512 bytes / 4096 bytes  
I/O size (minimum/optimal): 4096 bytes / 4096 bytes  
.  
.  
.  
Disk /dev/sda: 465.76 GiB, 500107862016 bytes, 976773168 sectors  
Disk model: Samsung SSD 870  
Units: sectors of 1 * 512 = 512 bytes  
Sector size (logical/physical): 512 bytes / 512 bytes  
I/O size (minimum/optimal): 512 bytes / 512 bytes
```

So for us its **/dev/sda.**

```
# Format your disk (If you decided to use your internal storage, just ignore the mount and format steps)  
mkfs.xfs -f /dev/sda  
  
# Create brick folder location  
mkdir -p /data/glusterfs/myvol1/brick1  
  
# Add line to /etc/fstab to auto mount this disk to /data on boot  
echo "/dev/sda /data/glusterfs/myvol1/brick1 xfs defaults 0 0" | tee -a /etc/fstab  
  
# Create brick folder   
mkdir -p /data/glusterfs/myvol1/brick1/brick  
  
# Mount  
mount -a  
  
# Check   
df -h /data/glusterfs/myvol1/brick1  

```

## Cluster

On the designated master node, we can now inform GlusterFS of the presence of all nodes in the network.

```
root@cube01:~# gluster peer probe cube02  
peer probe: success  
root@cube01:~# gluster peer probe cube03  
peer probe: success  
root@cube01:~# gluster peer probe cube04  
peer probe: success  
# Check  
root@cube01:~# gluster pool list  
UUID Hostname State  
a67aa75b-a359-4064-844e-e32ebedda4a0 cube02 Connected   
475c599d-57dc-4c9d-a8d9-90da965cdddb cube03 Connected   
df807f9a-1e56-4dd7-a8be-4dc98de57192 cube04 Connected   
4cd1dc90-3f42-4bd7-9510-54ad9a3fcdb2 localhost Connected 
```

## Volume

In GlusterFS, a volume is a logical unit of storage created from one or more bricks (physical storage resources). The volume is the main entity through which data is stored, retrieved, and managed. It provides a single namespace for data and enables high availability, scalability, and data protection features. Simply put, a GlusterFS volume is a pool of storage space that can be accessed from multiple servers in a cluster.

### Option 1:

Creating volume on **single node** with disk (node3)

```
root@cube01:~# gluster volume create dockervol1 cube03:/data/glusterfs/myvol1/brick1/brick  
volume create: dockervol1: success: please start the volume to access data
```

Check

```
root@cube01:~# gluster volume info  
  
Volume Name: dockervol1  
Type: Distribute  
Volume ID: a8b4fa7f-df8c-4788-be70-2acc0544afd6  
Status: Created  
Snapshot Count: 0  
Number of Bricks: 1  
Transport-type: tcp  
Bricks:  
Brick1: cube03:/data/glusterfs/myvol1/brick1/brick  
Options Reconfigured:  
storage.fips-mode-rchecksum: on  
transport.address-family: inet  
nfs.disable: on  
root@cube01:~# gluster volume start dockervol1  
volume start: dockervol1: success  
root@cube01:~# gluster volume info
```

Start the volume before we can mount it.

```
root@cube01:~# gluster volume start dockervol1  
volume start: dockervol1: success
```

### Option 2:

To create a GlusterFS volume using 3 nodes, make sure the disks have been mounted under **"/data/glusterfs/myvol1**" and that the folder "**/data/glusterfs/myvol1/brick2**" has been created on all 3 nodes. Note, if you are using the root file system, you will need to include the "force" option at the end of the command.

**On master node:**

```
gluster volume create dockervol2 disperse 3 redundancy 1 cube01:/data/glusterfs/myvol1/brick2 cube02:/data/glusterfs/myvol1/brick2 cube03:/data/glusterfs/myvol1/brick2
```

Interesting parts are:

* **disperse** - Read more [**HERE**](https://docs.gluster.org/en/main/Administrator-Guide/Setting-Up-Volumes/#volume-types)
* **redundancy** - Read more [**HERE**](https://docs.gluster.org/en/main/Administrator-Guide/Setting-Up-Volumes/#volume-types)

```
root@cube01:~# gluster volume info dockervol2  
  
Volume Name: dockervol2  
Type: Disperse  
Volume ID: 27c79497-848e-4fe4-80c5-18b7d5471001  
Status: Started  
Snapshot Count: 0  
Number of Bricks: 1 x (2 + 1) = 3  
Transport-type: tcp  
Bricks:  
Brick1: cube01:/data/glusterfs/myvol1/brick2  
Brick2: cube02:/data/glusterfs/myvol1/brick2  
Brick3: cube03:/data/glusterfs/myvol1/brick2  
Options Reconfigured:  
storage.fips-mode-rchecksum: on  
transport.address-family: inet  
nfs.disable: on
```

**Start the volume.**

```
root@cube01:~# gluster volume start dockervol2  
volume start: dockervol2: success
```

## Mounting GlusterFS

We have our volumes, now we can mount one of them to nodes.

**On all nodes**:

```
mkdir /mnt/docker-storage  
echo "localhost:/dockervol1 /mnt/docker-storage glusterfs defaults,_netdev 0 0" | tee -a /etc/fstab  
mount -a  
  

```

Our persistent shared storage will be "/mnt/docker-storage"

### Check:

```
root@cube02:~# df -h /mnt/docker-storage  
Filesystem Size Used Avail Use% Mounted on  
localhost:/dockervol1 466G 8.0G 458G 2% /mnt/docker-storage
```

### Test:

```
# Create file on node4  
touch /mnt/docker-storage/test_file  
# Check on node1 in same location and the file should be there.
```

Now that the GlusterFS volume has been created and mounted to "/mnt/docker-storage", you can utilize this directory in your Docker deployments to ensure that any persistent files will be accessible regardless of which node in the swarm the container is running on.

## Security

By default, GlusterFS server allows mounting volume to everybody, you can limit it to specific IPs. In our case, IPs of our nodes. On your master node (cube01):

```
gluster volume set dockervol1 auth.allow 127.0.0.1,10.0.0.60,10.0.0.61,10.0.0.62,10.0.0.63  
gluster volume set dockervol2 auth.allow 127.0.0.1,10.0.0.60,10.0.0.61,10.0.0.62,10.0.0.63
```
