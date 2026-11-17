---
title: "Sample app deployment"
description: "We suggest utilizing ArgoCD for GitOps-based deployments to keep track about what is running and where more easily."
head:
  - tag: title
    content: "Sample App Deployment To Turing Pi2 Kubernetes Cluster | Turing Pi Docs"
lastUpdated: 2025-11-12
---

We suggest utilizing ArgoCD for GitOps-based deployments to keep track about what is running and where more easily.

However, this sample deployment will covers the majority of the systems we have established, including MetalLB and Persistent Storage. We will create separate deployment YAML files and apply them sequentially without ArgoCD.

We plan to deploy a basic Redis server that will feature persistent storage, which will be linked to the pod as it moves throughout the cluster. The server will also have its own unique IP address (10.0.0.73) thanks to the use of MetalLB.

**Create a directory** to store your configuration files.

```
mkdir redis-deployment  
cd redis-deployment
```

We will organize all components related to Redis into its own namespace.

```
kubectl create namespace redis-server
```

### pvc.yaml

Create our first configuration file: **pvc.yaml.** We are going to define persistent storage for our deployment. In this example, we are using Longhorn storage class, but you can easily rename it to **nfs-client** if you have installed NFS StorageClass.

To list your StorageClasses run following command:

```
kubectl get storageclass
```

Inside pvc.yaml

```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: redis-pvc
  namespace: redis-server
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: longhorn
  resources:
    requests:
      storage: 5Gi
```

### deployment.yaml

Here we will define what container to run, what storage to mount to it and where.

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis-server
  namespace: redis-server
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis-server
  template:
    metadata:
      labels:
        app: redis-server
        name: redis-server
    spec:
      nodeSelector:
        node-type: worker
      containers:
      - name: redis-server
        image: redis
        args: ["--appendonly", "yes"]
        ports:
          - name: redis-server
            containerPort: 6379
        volumeMounts:
          - name: lv-storage
            mountPath: /data
        env:
          - name: ALLOW_EMPTY_PASSWORD
            value: "yes"
      volumes:
        - name: lv-storage
          persistentVolumeClaim:
            claimName: redis-pvc
```

**Note some details like:**

* **nodeSelector** - where near the start of this guide we have labeled our nodes, and this allows us to tell Kubernetes where this deployment can run.
* **volumeMounts** - Is mounting volume named lv-storage (defined from our PVC in the bottom of the config) in container to path /data

### service.yaml

In this file, we will define Kubernetes service, telling our cluster how to access the container from deployment.yaml

```
apiVersion: v1
kind: Service
metadata:
  name: redis-server
  namespace: redis-server
spec:
  selector:
    app: redis-server
  type: LoadBalancer
  ports:
    - name: redis-port
      protocol: TCP
      port: 6379
      targetPort: 6379
  loadBalancerIP: 10.0.0.73
```

Here is important to node **selector** which basically looks for container with app=redis-server, and we have defined that in deployment.yaml under **template.** Next important is the **loadBalancerIP,** here you can specify IP from MetalLB range.

## Deploy

You can deploy all the files at once by just providing a folder for kubect deploy command, but we will do it in logical order for educational purposes.

```
kubectl apply -f pvc.yaml
```

Check if PVC was created

```
root@cube01:~/redis-deployment# kubectl get pvc -n redis-server  
NAME      STATUS   VOLUME                                   CAPACITY ACCESS MODES STORAGECLASS AGE  
redis-pvc Bound    pvc-5cc8e80c-182a-4f50-b25a-d52904ec31d9 5Gi       RWO            longhorn    66s
```

You can also get more details with:

```
kubectl describe pvc redis-pvc -n redis-server
```

Deploy the deployment.yaml

```
kubectl apply -f deployment.yaml
```

Check and wait until container is "Running"

```
root@cube01:~/redis-deployment# kubectl get pods -n redis-server  
NAME                        READY  STATUS  RESTARTS AGE  
redis-server-8db957bc6-dpxtx 1/1   Running    0      74s
```

Lastly, create the service.

```
kubectl apply -f service.yaml
```

Check the service:

```
root@cube01:~/redis-deployment# kubectl get svc redis-server -n redis-server  
NAME            TYPE        CLUSTER-IP  EXTERNAL-IP   PORT(S)       AGE  
redis-server LoadBalancer 10.43.233.56    10.0.0.73 6379:31424/TCP 2m46s
```

**Now we have Redis server on port 10.0.0.73, with persistent storage and external IP.** 

## Cleanup

You can easily remove everything by using **kubectl delete** with the same files in reverse order.

```
kubectl delete -f service.yaml  
kubectl delete -f deployment.yaml   
kubectl delete -f pvc.yaml 
```
