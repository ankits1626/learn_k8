# Checkpoint 0: Foundation Setup ⚙️

**Status:** 🔄 In Progress
**Time Estimate:** 15-20 minutes
**Difficulty:** Beginner

---

## 🎯 Learning Objectives

By the end of this checkpoint, you will:
- ✅ Verify all required tools are installed
- ✅ Understand what each tool does and why we need it
- ✅ Start your first Kubernetes cluster with minikube
- ✅ Get comfortable with basic kubectl commands
- ✅ Experience k9s (the terminal UI for Kubernetes)

---

## 📚 Concepts: Understanding Your Toolkit

Before we dive in, let's understand what each tool does:

### **Docker** 🐳
- **What:** Platform for building and running containers
- **Why:** We need it to create the "shipping containers" for our applications
- **Analogy:** Think of it as a factory that packages your app with everything it needs to run

### **kubectl** ⚙️
- **What:** Command-line tool to talk to Kubernetes clusters
- **Why:** It's your remote control for Kubernetes - you'll use this A LOT
- **Pronunciation:** "kube-control" or "kube-C-T-L"

### **minikube** 🎮
- **What:** Creates a local Kubernetes cluster on your Mac
- **Why:** Practice on your laptop before touching production!
- **Analogy:** Like a flight simulator for pilots - safe practice environment

### **Helm** 📦
- **What:** Package manager for Kubernetes applications
- **Why:** Instead of writing 10 YAML files, write 1 Helm chart
- **Analogy:** Like npm for Node.js, but for Kubernetes apps

### **k9s** 🎨
- **What:** Beautiful terminal UI for managing Kubernetes
- **Why:** Easier to navigate than typing kubectl commands constantly
- **Analogy:** Like using a GUI file explorer vs. just command line

### **ArgoCD** 🔄
- **What:** GitOps tool for automated deployments
- **Why:** Git becomes your single source of truth - what's in Git is what runs
- **Analogy:** Like autopilot that keeps your cluster matching your Git repository

---

## 📖 Concept Deep Dive: What is a Kubernetes Cluster?

Before we verify tools, let's understand **what we're actually building**. A Kubernetes cluster is not just abstract - let's explore it visually!

### 🎯 Definition

A **Kubernetes cluster** is a set of machines (called **nodes**) working together to run your containerized applications.

**Components:**
1. **Control Plane (The Brain)** - Makes all decisions
2. **Worker Nodes (The Muscle)** - Runs your applications

### 🏗️ Visual Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   KUBERNETES CLUSTER                        │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │         CONTROL PLANE (The Brain)                   │    │
│  │                                                     │    │
│  │  [API Server] ← kubectl talks to this               │    │
│  │       ↓                                             │    │
│  │  [Scheduler] ← Decides which node runs which pod    │    │
│  │       ↓                                             │    │
│  │  [Controller Manager] ← Ensures desired state       │    │
│  │       ↓                                             │    │
│  │  [etcd] ← Database storing cluster state            │    │
│  └─────────────────────────────────────────────────────┘    │
│                         ↓ ↓ ↓                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Worker Node 1│  │ Worker Node 2│  │ Worker Node 3│       │
│  │              │  │              │  │              │       │
│  │ [Kubelet]    │  │ [Kubelet]    │  │ [Kubelet]    │       │
│  │ [Kube-proxy] │  │ [Kube-proxy] │  │ [Kube-proxy] │       │
│  │              │  │              │  │              │       │
│  │  🔵 Pod 1    │  │  🔵 Pod 3    │  │  🔵 Pod 5    │        │
│  │  🔵 Pod 2    │  │  🔵 Pod 4    │  │  🔵 Pod 6    │        │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

### 🎮 Your Minikube Cluster (Simplified for Learning)

```
┌─────────────────────────────────┐
│      Your Mac                   │
│                                 │
│  ┌───────────────────────────┐  │
│  │  Minikube Container       │  │
│  │                           │  │
│  │  Control Plane + Worker   │  │
│  │  (All-in-one!)            │  │
│  │                           │  │
│  │  Your apps run here       │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
```

**We'll explore this hands-on in Exercise 2!**

---

## 🔧 Exercise 1: Verify Your Tools

Let's make sure everything is installed correctly.

### Step 1.1: Check Docker

Run this command in your terminal:

```bash
docker --version
```

**Expected output:**
```
Docker version 28.5.1, build e180ab8
```

**❓ Concept Check:** What does this tell you?
<details>
<summary>Click to see answer</summary>
Docker is installed and ready to create containers. Version 28.5.1 is the latest version optimized for Apple Silicon.
</details>

---

### Step 1.2: Check kubectl

```bash
kubectl version --client
```

**Expected output:**
```
Client Version: v1.34.2
```

**❓ Why `--client` flag?**
<details>
<summary>Click to see answer</summary>
We only want the client version for now. Without this flag, kubectl tries to connect to a cluster (which we haven't started yet) and will show an error.
</details>

---

### Step 1.3: Check minikube

```bash
minikube version
```

**Expected output:**
```
minikube version: v1.37.0
```

---

### Step 1.4: Check Helm

```bash
helm version
```

**Expected output:**
```
version.BuildInfo{Version:"v4.0.1", GitCommit:"12500dd401faa7629f30ba5d5bff36287f3e94d3", GitTreeState:"clean", GoVersion:"go1.25.4", KubeClientVersion:"v1.34"}
```

**🔍 Let's decode what this means:**

| Field | Value | What It Means |
|-------|-------|---------------|
| **Version** | `v4.0.1` | The Helm version you're running - this is the important one! |
| **GitCommit** | `12500dd...` | The specific Git commit hash used to build this Helm binary |
| **GitTreeState** | `clean` | No uncommitted changes when built - it's an official release |
| **GoVersion** | `go1.25.4` | Helm is written in Go programming language, built with Go v1.25.4 |
| **KubeClientVersion** | `v1.34` | Helm can talk to Kubernetes API version 1.34 |

**💡 Why is this useful?**
- **Version** tells you which Helm you have (v4 has new features vs v3)
- **GitTreeState: clean** confirms it's an official build, not custom
- **KubeClientVersion** shows Helm is compatible with your kubectl version

**🔧 Quick Test - Let's verify Helm works:**

```bash
# List all Helm releases (should be empty for now)
helm list
```

**Possible outputs:**

**If you see this:**
```
Error: kubernetes cluster unreachable: the server could not find the requested resource
```

**✅ This is EXPECTED!** It means:
- Helm is installed correctly
- Helm is trying to connect to a Kubernetes cluster
- **But you haven't started your cluster yet!**
- We'll start the cluster in Exercise 2

**Or if you see this (empty table):**
```
NAME    NAMESPACE    REVISION    UPDATED    STATUS    CHART    APP VERSION
```

**✅ This is also correct!** It means:
- Helm is working
- It's connected to a cluster
- You haven't deployed anything with Helm yet

**💡 Key Insight:**

Helm **needs** a Kubernetes cluster to work because it:
1. Talks to the Kubernetes API (just like kubectl)
2. Deploys applications to the cluster
3. Stores release information in the cluster

**Think of it this way:**
- **kubectl** = talking to your cluster
- **Helm** = talking to your cluster + packaging apps nicely

Both need a cluster running! You'll start your cluster in the next exercise.

---

**🎯 What just happened?**

```
You (helm list) → Helm → Tries to find Kubernetes API → ❌ No cluster running yet
```

**After Exercise 2:**
```
You (helm list) → Helm → Finds Kubernetes API ✅ → Shows empty list (expected)
```

---

### Step 1.5: Check k9s

```bash
k9s version
```

**Expected output:**
```
Version: 0.50.16
```

---

### Step 1.6: Check ArgoCD CLI

```bash
argocd version --client
```

**Expected output:**
```
argocd: v3.2.0+...
```

---

## ✅ Checkpoint: Did all commands work?

- ✅ **All worked:** Perfect! Continue to Exercise 2
- ❌ **Some failed:** Let me know which tool failed and I'll help you install it

---

## 🔧 Exercise 2: Start Your First Kubernetes Cluster

This is the exciting part! We're going to create a complete Kubernetes cluster on your Mac.

### Step 2.1: Start minikube

Run this command:

```bash
minikube start --driver=docker --cpus=4 --memory=8192
```

**What's happening:**
- `--driver=docker`: Use Docker to run the cluster (not a VM)
- `--cpus=4`: Allocate 4 CPU cores to the cluster
- `--memory=8192`: Allocate 8GB of RAM (8192 MB)

**Expected output:**
```
😄  minikube v1.37.0 on Darwin 15.6.1 (arm64)
🆕  Kubernetes 1.34.0 is now available. If you would like to upgrade, specify: --kubernetes-version=v1.34.0
✨  Using the docker driver based on existing profile
❗  You cannot change the memory size for an existing minikube cluster. Please first delete the cluster.
❗  You cannot change the CPUs for an existing minikube cluster. Please first delete the cluster.
👍  Starting "minikube" primary control-plane node in "minikube" cluster
🚜  Pulling base image v0.0.48 ...
🤷  docker "minikube" container is missing, will recreate.
🔥  Creating docker container (CPUs=2, Memory=9200MB) ...
❗  Image was not built for the current minikube version. To resolve this you can delete and recreate your minikube cluster using the latest images. Expected minikube version: v1.34.0 -> Actual minikube version: v1.37.0
🐳  Preparing Kubernetes v1.31.0 on Docker 27.2.0 ...
🔗  Configuring bridge CNI (Container Networking Interface) ...
🔎  Verifying Kubernetes components...
    ▪ Using image gcr.io/k8s-minikube/storage-provisioner:v5
🌟  Enabled addons: storage-provisioner, default-storageclass
❗  /opt/homebrew/bin/kubectl is version 1.34.2, which may have incompatibilities with Kubernetes 1.31.0.
    ▪ Want kubectl v1.31.0? Try 'minikube kubectl -- get pods -A'
🏄  Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default
```

⏱️ **This takes 2-3 minutes** - minikube is downloading Kubernetes and setting up your cluster. Grab some water! 💧

---

### 🔍 Step 2.1a: Understanding What Just Happened

Let's decode each line of that output:

| Line | What It Means | Technical Detail |
|------|---------------|------------------|
| 😄 `minikube v1.37.0 on Darwin 15.6.1 (arm64)` | You're running minikube v1.37.0 on macOS with Apple Silicon | Darwin = macOS, arm64 = M1/M2/M3 chip |
| 🆕 `Kubernetes 1.34.0 is now available` | Newer K8s version available (optional upgrade) | You're using v1.31.0, v1.34.0 exists but not required |
| ✨ `Using the docker driver based on existing profile` | Minikube found a previous cluster configuration | You had a cluster before, reusing settings |
| ❗ `You cannot change the memory/CPUs` | Your old cluster had different resources | It's using the old settings (CPUs=2, Memory=9200MB) |
| 👍 `Starting "minikube" primary control-plane node` | Creating the cluster node | This node runs both control plane AND workloads |
| 🚜 `Pulling base image v0.0.48` | Downloading the minikube base container image | Like downloading an OS installer |
| 🤷 `container is missing, will recreate` | Old container was deleted, making a new one | Fresh start! |
| 🔥 `Creating docker container (CPUs=2, Memory=9200MB)` | **THE KEY STEP!** Creating a Docker container | This container IS your Kubernetes cluster |
| 🐳 `Preparing Kubernetes v1.31.0 on Docker 27.2.0` | Installing Kubernetes inside the container | K8s v1.31.0 running on Docker v27.2.0 |
| 🔗 `Configuring bridge CNI` | Setting up pod networking | CNI = Container Network Interface (how pods talk) |
| 🔎 `Verifying Kubernetes components` | Checking control plane is healthy | API server, scheduler, etc. starting up |
| 🌟 `Enabled addons: storage-provisioner` | Added storage capability | Allows pods to request persistent storage |
| ❗ `kubectl is version 1.34.2...` | Minor version mismatch warning | kubectl v1.34 vs K8s v1.31 - **safe to ignore** |
| 🏄 `Done! kubectl is now configured` | **SUCCESS!** Ready to use | kubectl now points to this cluster |

---

### 🐳 Step 2.1b: Verify in Docker Desktop

**Now let's SEE your cluster in Docker Desktop!**

**Method 1: Docker Desktop GUI**

1. **Open Docker Desktop** (click the Docker icon in your menu bar)
2. Click on **"Containers"** in the left sidebar
3. Look for a container named **`minikube`**

**You should see:**
```
Container Name: minikube
Image: gcr.io/k8s-minikube/kicbase:v0.0.48
Status: Running (green)
Ports: Multiple ports exposed
CPU/Memory: 2 CPUs, ~9200MB RAM
```

**Click on the `minikube` container** to see:
- **Logs** - Kubernetes startup logs
- **Inspect** - Full container configuration
- **Stats** - Real-time CPU/Memory usage
- **Terminal** - Shell access inside the container!

---

**Method 2: Command Line Verification**

```bash
# List all Docker containers
docker ps
```

**You should see:**
```
CONTAINER ID   IMAGE                                 STATUS         PORTS                                                                                                                                  NAMES
abc12345def    gcr.io/k8s-minikube/kicbase:v0.0.48   Up 2 minutes   127.0.0.1:xxxxx->22/tcp, 127.0.0.1:xxxxx->2376/tcp, 127.0.0.1:xxxxx->5000/tcp, 127.0.0.1:xxxxx->8443/tcp, 127.0.0.1:xxxxx->32443/tcp   minikube
```

**What this tells you:**
- **IMAGE**: `gcr.io/k8s-minikube/kicbase:v0.0.48` - The base image minikube uses
- **STATUS**: `Up 2 minutes` - Container is running
- **PORTS**: Multiple ports exposed - these are for Kubernetes API, SSH, etc.
- **NAMES**: `minikube` - This is your entire Kubernetes cluster!

---

**Method 3: Inspect the Container**

```bash
# Get detailed information about the minikube container
docker inspect minikube | grep -A 10 "Config"
```

**Or see it in Docker Desktop:**
1. Click on **`minikube`** container
2. Click **"Inspect"** tab
3. Scroll through the JSON - you'll see:
   - **Memory limit**: 9200MB
   - **CPU count**: 2
   - **Environment variables**: Kubernetes configuration
   - **Volumes**: Where cluster data is stored

---

### 🎯 The Big Picture: What Is Actually Running?

**Inside that single Docker container:**

```
┌─────────────────────────────────────────────────────┐
│  Docker Container: "minikube"                       │
│  Image: gcr.io/k8s-minikube/kicbase:v0.0.48        │
│                                                     │
│  ┌───────────────────────────────────────────────┐ │
│  │  KUBERNETES CONTROL PLANE                     │ │
│  │  ┌─────────────────────────────────────────┐ │ │
│  │  │ kube-apiserver (port 8443)              │ │ │
│  │  │ kube-scheduler                          │ │ │
│  │  │ kube-controller-manager                 │ │ │
│  │  │ etcd (database)                         │ │ │
│  │  └─────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────┘ │
│                                                     │
│  ┌───────────────────────────────────────────────┐ │
│  │  WORKER NODE                                  │ │
│  │  ┌─────────────────────────────────────────┐ │ │
│  │  │ kubelet (node agent)                    │ │ │
│  │  │ kube-proxy (networking)                 │ │ │
│  │  │ Container runtime (Docker-in-Docker)    │ │ │
│  │  │                                         │ │ │
│  │  │ Your pods will run here! →              │ │ │
│  │  └─────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

**Mind-blowing fact:** That one Docker container contains an ENTIRE Kubernetes cluster - control plane, worker node, networking, storage, everything!

---

### ✅ Quick Verification Checklist

Run these commands to confirm everything is working:

```bash
# 1. Check Docker has minikube container
docker ps --filter "name=minikube"

# 2. Check minikube status
minikube status

# 3. Check Kubernetes nodes
kubectl get nodes

# 4. Check system pods
kubectl get pods -n kube-system
```

**All should show successful output!**

---

### 🎓 Key Learnings

1. **Minikube = Docker Container**: Your entire cluster runs in one container
2. **Docker Desktop Shows It**: You can see/manage the minikube container like any other container
3. **Resource Allocation**: The container uses real RAM/CPU from your Mac (2 CPUs, 9200MB in your case)
4. **Self-Contained**: Everything Kubernetes needs is inside that container
5. **Easy to Delete**: `minikube delete` removes the container - clean slate!

---

### Step 2.2: Verify the cluster is running

```bash
minikube status
```

**Expected output:**
```
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured
```

**🎉 Congratulations!** You now have a real Kubernetes cluster running on your Mac!

---

### Step 2.3: View cluster information

```bash
kubectl cluster-info
```

**Expected output:**
```
Kubernetes control plane is running at https://127.0.0.1:xxxxx
CoreDNS is running at https://127.0.0.1:xxxxx/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
```

**❓ What is this showing?**
<details>
<summary>Click to see answer</summary>
- Your Kubernetes API server is running locally
- CoreDNS provides internal DNS for pods to find each other
- Everything is accessible via localhost (127.0.0.1)
</details>

---

### Step 2.4: View your cluster nodes

```bash
kubectl get nodes
```

**Expected output:**
```
NAME       STATUS   ROLES           AGE   VERSION
minikube   Ready    control-plane   2m    v1.32.0
```

**❓ What is a "node"?**
<details>
<summary>Click to see answer</summary>
A node is a worker machine (physical or virtual) that runs your applications. In production, you'd have many nodes. Minikube gives you one node that acts as both control plane and worker.
</details>

---

## 🔧 Exercise 3: Explore with kubectl

Let's practice some basic kubectl commands to explore your cluster.

### Step 3.1: View all namespaces

```bash
kubectl get namespaces
```

**Expected output:**
```
NAME              STATUS   AGE
default           Active   3m
kube-node-lease   Active   3m
kube-public       Active   3m
kube-system       Active   3m
```

**❓ What are namespaces?**
<details>
<summary>Click to see answer</summary>
Namespaces are like folders for organizing resources. Think of them as separate departments in a company:
- `default` - Where your apps go (if you don't specify)
- `kube-system` - Kubernetes internal components
- `kube-public` - Publicly accessible resources
- `kube-node-lease` - Node heartbeat information
</details>

---

### Step 3.2: View system pods

```bash
kubectl get pods -n kube-system
```

**Expected output:**
```
NAME                               READY   STATUS    RESTARTS   AGE
coredns-xxx                        1/1     Running   0          5m
etcd-minikube                      1/1     Running   0          5m
kube-apiserver-minikube            1/1     Running   0          5m
kube-controller-manager-minikube   1/1     Running   0          5m
kube-proxy-xxx                     1/1     Running   0          5m
kube-scheduler-minikube            1/1     Running   0          5m
storage-provisioner                1/1     Running   0          5m
```

**🤯 Mind-blowing fact:** Kubernetes manages itself! All these components (API server, scheduler, etc.) run as pods inside Kubernetes.

---

### Step 3.3: View everything at once

```bash
kubectl get all -A
```

**What does `-A` mean?**
<details>
<summary>Click to see answer</summary>
`-A` means "all namespaces". Without it, you only see resources in the `default` namespace.
</details>

You'll see lots of output - don't worry about understanding it all yet! We'll learn each component step by step.

---

## 🔧 Exercise 4: Experience k9s (The Fun Part!)

k9s is a terminal UI that makes Kubernetes much easier to navigate. Let's try it!

### Step 4.1: Launch k9s

```bash
k9s
```

**What you'll see:**
- A beautiful terminal interface showing your pods
- Top bar showing cluster name and context
- List of pods in the current namespace

### Step 4.2: Navigate k9s

**Try these keyboard shortcuts:**

| Key | Action |
|-----|--------|
| `0` | Show all namespaces |
| `:pods` | View pods |
| `:deploy` | View deployments |
| `:svc` | View services |
| `:ns` | View namespaces |
| `?` | Help menu |
| `q` | Quit |

**Exercise:**
1. Press `0` to see all namespaces
2. Type `:pods` and press Enter - you'll see all pods across all namespaces
3. Use arrow keys to navigate
4. Press `q` to quit k9s

**💡 Pro Tip:** k9s is amazing for quickly checking what's running in your cluster. You'll use this a lot!

---

## 🔧 Exercise 5: Quick Test - Deploy Something!

Let's deploy something simple to verify everything works.

### Step 5.1: Run a test pod

```bash
kubectl run hello-test --image=nginx:alpine --port=80
```

**What's happening:**
- `kubectl run` - Create a pod
- `hello-test` - Name of the pod
- `--image=nginx:alpine` - Use the nginx web server (Alpine Linux version)
- `--port=80` - Expose port 80

---

### Step 5.2: Check if it's running

```bash
kubectl get pods
```

**Expected output:**
```
NAME         READY   STATUS    RESTARTS   AGE
hello-test   1/1     Running   0          10s
```

**Status meanings:**
- `ContainerCreating` - Still downloading/starting
- `Running` - Pod is running ✅
- `Error` or `CrashLoopBackOff` - Something went wrong ❌

---

### Step 5.3: Access the nginx web server

```bash
kubectl port-forward pod/hello-test 8080:80
```

**What's happening:**
- Forward port 8080 on your Mac → port 80 in the pod
- Leave this terminal window open

**Now open a NEW terminal and run:**
```bash
curl http://localhost:8080
```

**Expected:** You'll see HTML output from nginx!

```html
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
...
```

**🎉 Success!** You just deployed your first application to Kubernetes and accessed it!

---

### Step 5.4: Clean up

Press `Ctrl+C` in the terminal running port-forward, then:

```bash
kubectl delete pod hello-test
```

**Verify it's gone:**
```bash
kubectl get pods
```

**Expected:**
```
No resources found in default namespace.
```

---

## ✅ Concept Check Quiz

Test your understanding:

1. **What is the difference between Docker and Kubernetes?**
   <details>
   <summary>Show answer</summary>
   Docker creates and runs individual containers. Kubernetes orchestrates (manages) many containers across many machines - handles scaling, healing, networking, etc.
   </details>

2. **What does kubectl do?**
   <details>
   <summary>Show answer</summary>
   kubectl is the command-line tool for interacting with Kubernetes clusters. It sends commands to the Kubernetes API server.
   </details>

3. **Why use minikube instead of a real cluster?**
   <details>
   <summary>Show answer</summary>
   Minikube is perfect for learning and testing locally. It's free, runs on your laptop, and you can't break production!
   </details>

4. **What is a namespace?**
   <details>
   <summary>Show answer</summary>
   A namespace is a way to divide cluster resources between multiple users or projects. Like folders for organizing your Kubernetes resources.
   </details>

5. **What does `kubectl get pods -n kube-system` do?**
   <details>
   <summary>Show answer</summary>
   Lists all pods in the `kube-system` namespace (where Kubernetes system components run).
   </details>

---

## 🎯 Summary: What You Learned

✅ **Tools verified** - Docker, kubectl, minikube, Helm, k9s, ArgoCD
✅ **First cluster created** - Real Kubernetes running on your Mac
✅ **Basic kubectl commands** - get, run, delete, port-forward
✅ **k9s navigation** - Beautiful UI for cluster exploration
✅ **First deployment** - Ran nginx pod and accessed it

---

## 🏢 Real-World Corollary: Local vs AWS Production

**This is CRITICAL to understand:** Everything you're learning locally maps directly to production AWS/EKS. The concepts are identical - only the infrastructure changes!

### 🔄 What Changes from Local to Production?

| Component | Your Local Setup (minikube) | Rewardz Production (AWS EKS) | Why Different? |
|-----------|------------------------------|------------------------------|----------------|
| **Cluster** | `minikube` - single Docker container | **AWS EKS** - Managed Kubernetes service | EKS handles control plane (API server, etcd, scheduler), you manage worker nodes |
| **Nodes** | 1 node (your Mac via Docker) | Multiple **EC2 instances** across **3 Availability Zones** | High availability - if one data center fails, others continue |
| **kubectl** | ✅ Same tool! | ✅ Same tool! Points to EKS cluster | **No difference!** Commands are identical |
| **Networking** | `127.0.0.1` (localhost) | **AWS VPC** with private subnets | Isolated network, pods get internal IPs |
| **DNS** | CoreDNS (local) | **Route53** + CoreDNS | Route53 handles external DNS, CoreDNS for internal |
| **Load Balancer** | `minikube service` or port-forward | **AWS ALB** (Application Load Balancer) | Real load balancer distributes traffic across nodes |
| **Storage** | Local Docker volumes | **EBS** (Elastic Block Storage) + **S3** | Persistent storage survives pod restarts |
| **Image Registry** | Local Docker cache | **AWS ECR** (Elastic Container Registry) | Private registry: `985539790887.dkr.ecr.ap-southeast-1.amazonaws.com` |
| **Secrets** | kubectl create secret | **AWS Secrets Manager** + **ExternalSecrets Operator** | Centralized secret management, auto-rotation |
| **Monitoring** | `kubectl logs` | **CloudWatch** + **Prometheus** + **Grafana** | Production-grade monitoring, alerts, dashboards |
| **Access** | Direct kubectl access | **IAM roles** + **kubeconfig** | Identity & Access Management for security |

---

### 🎯 Exercise 2.4 in Production

**What you just did locally:**
```bash
kubectl get nodes
# Output: 1 node (minikube)
```

**In Rewardz EKS production:**
```bash
# First, connect to EKS cluster
aws eks update-kubeconfig --name rewardz-cluster --region ap-southeast-1

# Same command, different output!
kubectl get nodes
```

**Production output would look like:**
```
NAME                                         STATUS   ROLES    AGE   VERSION
ip-10-0-1-123.ap-southeast-1.compute.internal   Ready    <none>   30d   v1.30.0
ip-10-0-2-234.ap-southeast-1.compute.internal   Ready    <none>   30d   v1.30.0
ip-10-0-3-345.ap-southeast-1.compute.internal   Ready    <none>   30d   v1.30.0
ip-10-0-4-456.ap-southeast-1.compute.internal   Ready    <none>   28d   v1.30.0
ip-10-0-5-567.ap-southeast-1.compute.internal   Ready    <none>   28d   v1.30.0
```

**What's different?**
- ✅ **5 nodes** instead of 1 (distributed across availability zones)
- ✅ **EC2 instance names** instead of "minikube"
- ✅ **Same kubectl command!** The tool doesn't change

---

### 🏗️ Architecture Comparison

**Your Local Setup:**
```
┌─────────────────────────────────────┐
│       Your Mac (darwin/arm64)       │
│                                     │
│  ┌───────────────────────────────┐ │
│  │   Minikube (Docker Container) │ │
│  │                               │ │
│  │  ┌──────────────────────┐    │ │
│  │  │  Control Plane       │    │ │
│  │  │  - API Server        │    │ │
│  │  │  - Scheduler         │    │ │
│  │  │  - Controller        │    │ │
│  │  │  - etcd              │    │ │
│  │  └──────────────────────┘    │ │
│  │                               │ │
│  │  ┌──────────────────────┐    │ │
│  │  │  Worker Node         │    │ │
│  │  │  - Your Pods         │    │ │
│  │  │  - CoreDNS           │    │ │
│  │  └──────────────────────┘    │ │
│  └───────────────────────────────┘ │
└─────────────────────────────────────┘
```

**Rewardz Production (AWS EKS):**
```
┌─────────────────────────────────────────────────────────────────────┐
│                        AWS Cloud (ap-southeast-1)                   │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │   EKS Control Plane (AWS Managed - You don't see this)      │ │
│  │   - API Server (High Availability across 3 AZs)             │ │
│  │   - Scheduler, Controller, etcd                             │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                              ↕ (API calls)                          │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │                    VPC (Private Network)                     │ │
│  │                                                              │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │ │
│  │  │   AZ-1       │  │   AZ-2       │  │   AZ-3       │     │ │
│  │  │              │  │              │  │              │     │ │
│  │  │ ┌──────────┐ │  │ ┌──────────┐ │  │ ┌──────────┐ │     │ │
│  │  │ │ EC2 Node │ │  │ │ EC2 Node │ │  │ │ EC2 Node │ │     │ │
│  │  │ │  Pods    │ │  │ │  Pods    │ │  │ │  Pods    │ │     │ │
│  │  │ └──────────┘ │  │ └──────────┘ │  │ └──────────┘ │     │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘     │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                              ↕                                      │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │   AWS Services                                               │ │
│  │   - ALB (Load Balancer)                                      │ │
│  │   - ECR (Container Registry)                                 │ │
│  │   - RDS (PostgreSQL Database)                                │ │
│  │   - S3 (File Storage)                                        │ │
│  │   - Secrets Manager                                          │ │
│  └──────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

### 📋 Real-World Example: Deploying nginx

**What you just did (Exercise 5):**
```bash
# Local
kubectl run hello-test --image=nginx:alpine --port=80
```

**In production, the same concept but with production image:**
```bash
# Connect to EKS first
aws eks update-kubeconfig --name rewardz-cluster --region ap-southeast-1

# Deploy auto-approver (conceptually same as your nginx!)
kubectl run auto-approver-test \
  --image=985539790887.dkr.ecr.ap-southeast-1.amazonaws.com/auto_approver:v1.2.3 \
  --port=8000
```

**Key differences:**
1. **Image source:**
   - Local: `nginx:alpine` from Docker Hub (public)
   - Production: `985539790887.dkr.ecr...` from AWS ECR (private)

2. **Cluster connection:**
   - Local: Automatic (minikube configures kubectl)
   - Production: `aws eks update-kubeconfig` to authenticate

3. **Port:**
   - Local: nginx uses port 80
   - Production: auto-approver uses port 8000

4. **Everything else is THE SAME!** ✅

---

### 🔑 Key Takeaway

**The Kubernetes concepts and kubectl commands you're learning are IDENTICAL in production!**

What changes:
- ❌ **Infrastructure layer** (minikube → EKS, localhost → AWS)
- ❌ **Scale** (1 node → 5+ nodes)
- ❌ **Services** (local files → AWS S3, RDS, Secrets Manager)

What stays the same:
- ✅ **kubectl commands** - `get`, `describe`, `logs`, `delete`, etc.
- ✅ **YAML manifests** - Pods, Deployments, Services all work identically
- ✅ **Kubernetes concepts** - Namespaces, labels, selectors, volumes
- ✅ **Helm charts** - Same templating, same values.yaml structure
- ✅ **ArgoCD GitOps** - Same workflow, same sync mechanism

**This is why minikube is perfect for learning!** You master the concepts locally, then apply them to production with just a different cluster configuration.

---

### 💼 Your Future Self in Production

**3 months from now:**

```bash
# Morning: Check your local dev environment
kubectl get pods -n dev
# Shows your local minikube pods

# Afternoon: Check production
aws eks update-kubeconfig --name rewardz-cluster --region ap-southeast-1
kubectl get pods -n prod
# Shows Rewardz EKS production pods

# Same command, different cluster! 🎉
```

You'll be comfortable switching between local and production because **the skills are transferable!**

---

## 🚀 Challenge (Optional)

Want to go further? Try this:

1. Start k9s (`k9s`)
2. Deploy another nginx pod with a different name
3. Use k9s to find and delete it (hint: select with arrow keys, press `Ctrl+d`)

---

## 📝 Common Commands Reference

Save these - you'll use them constantly:

```bash
# Cluster management
minikube start                 # Start cluster
minikube stop                  # Stop cluster
minikube status                # Check status
minikube delete                # Delete cluster

# View resources
kubectl get pods               # List pods
kubectl get pods -A            # List pods in all namespaces
kubectl get nodes              # List nodes
kubectl get all -A             # List everything

# Create/delete resources
kubectl run NAME --image=IMAGE # Create a pod
kubectl delete pod NAME        # Delete a pod

# Inspect resources
kubectl describe pod NAME      # Detailed info about pod
kubectl logs NAME              # View pod logs
kubectl port-forward pod/NAME 8080:80  # Access pod locally

# k9s
k9s                           # Launch k9s
# Then use: 0, :pods, :deploy, :svc, q
```

---

## ➡️ Next Steps

**Ready for Checkpoint 1?**

You've laid the foundation! Next, we'll learn about **containers in depth** by building a custom application and containerizing it with Docker.

Tell me when you're ready, and I'll create **Checkpoint 1: Containers Before Kubernetes**! 🚀

---

## 🆘 Troubleshooting

### Minikube won't start?

```bash
# Delete and recreate
minikube delete
minikube start --driver=docker --cpus=4 --memory=8192
```

### kubectl command not found?

Verify installation:
```bash
which kubectl
```

If not found, install:
```bash
brew install kubectl
```

### Port-forward not working?

Make sure the pod is running:
```bash
kubectl get pods
# Status should be "Running"
```

---

**Questions?** Ask your coach (me!) anytime. No question is too basic! 💪
