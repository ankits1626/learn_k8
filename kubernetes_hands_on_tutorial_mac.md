# Kubernetes Hands-On Tutorial for Mac

## Learn by Doing - From Zero to Production Concepts

This tutorial teaches you Kubernetes concepts used in the Rewardz organization by building everything from scratch on your Mac. By the end, you'll understand how the auto-approver application deploys to EKS.

**🎯 Your Setup:**
- ✅ Docker 28.5.1
- ✅ kubectl v1.34.2
- ✅ minikube v1.37.0
- ✅ Helm v4.0.1
- ✅ k9s v0.50.16
- ✅ ArgoCD v3.2.0
- ✅ Apple Silicon (M1/M2/M3)

**⏱️ Time to Complete:** 4-6 hours (can be done in multiple sessions)

**📚 What You'll Learn:**
All Kubernetes concepts used in the Rewardz EKS deployment - from basic containers to GitOps workflows!

---

## Quick Start (Impatient? Start Here!)

```bash
# 1. Start minikube (takes ~2 minutes)
minikube start --driver=docker --cpus=4 --memory=8192

# 2. Verify it's running
kubectl get nodes

# 3. Open k9s to see your cluster
k9s

# 4. You're ready! Jump to Lab 1
```

**If this worked, skip to [Lab 1](#lab-1-running-your-first-container)!**

---

## Table of Contents

**📖 [Glossary of Terms](#glossary-of-terms)** ← Start here if you're new to Kubernetes!

1. [Prerequisites and Setup](#prerequisites-and-setup)
2. [Lab 1: Running Your First Container](#lab-1-running-your-first-container)
3. [Lab 2: Local Kubernetes Cluster](#lab-2-local-kubernetes-cluster)
4. [Lab 3: Pods - The Smallest Unit](#lab-3-pods---the-smallest-unit)
5. [Lab 4: Deployments - Managing Multiple Pods](#lab-4-deployments---managing-multiple-pods)
6. [Lab 5: Services - Networking Between Pods](#lab-5-services---networking-between-pods)
7. [Lab 6: ConfigMaps and Secrets](#lab-6-configmaps-and-secrets)
8. [Lab 7: Ingress - External Access](#lab-7-ingress---external-access)
9. [Lab 8: Namespaces - Environment Isolation](#lab-8-namespaces---environment-isolation)
10. [Lab 9: Auto-Scaling with HPA](#lab-9-auto-scaling-with-hpa)
11. [Lab 10: Helm Charts](#lab-10-helm-charts)
12. [Lab 11: GitOps with ArgoCD](#lab-11-gitops-with-argocd)
13. [Lab 12: Deploying Auto-Approver Locally](#lab-12-deploying-auto-approver-locally)

---

## Glossary of Terms

**This section explains technical terms used throughout the tutorial. Reference this anytime you encounter an unfamiliar term!**

### Core Kubernetes Terms

| Term | What It Means | Real-World Analogy |
|------|---------------|-------------------|
| **Container** | A lightweight, standalone package that includes your application code + all dependencies (libraries, runtime, system tools) | Like a shipping container - everything your app needs is packaged together and can run anywhere |
| **Docker** | A platform for building and running containers | The factory that creates and manages shipping containers |
| **Image** | A blueprint/template for creating containers. Built from a Dockerfile | Like a cookie cutter - you use it to create many identical cookies (containers) |
| **Pod** | The smallest deployable unit in Kubernetes. One or more containers running together | Like a shipping box - can hold one or more items (containers) |
| **Node** | A physical or virtual machine in the cluster that runs pods | Like a warehouse worker - does the actual work of running your applications |
| **Cluster** | A set of nodes managed by Kubernetes | Like a warehouse - multiple workers (nodes) working together |
| **Namespace** | A virtual cluster for isolating resources (like folders) | Like departments in a company - HR, Engineering, Finance - each isolated |
| **Deployment** | Manages multiple copies (replicas) of your application, handles rolling updates | Like a factory manager - ensures right number of workers, handles shift changes |
| **Service** | Provides a stable network address for accessing pods | Like a company phone number - even if employees change, the number stays the same |
| **Ingress** | Routes external HTTP/HTTPS traffic to services based on URLs | Like a receptionist - directs visitors to the right department based on who they're looking for |
| **ConfigMap** | Stores non-sensitive configuration data (like .env files) | Like a settings file - stores preferences and configuration |
| **Secret** | Stores sensitive data (passwords, API keys) in encrypted form | Like a safe - stores valuable items securely |

### Helm Terms

| Term | What It Means | Real-World Analogy |
|------|---------------|-------------------|
| **Helm** | Package manager for Kubernetes applications | Like npm for Node.js or apt for Ubuntu - installs/manages software packages |
| **Chart** | A Helm package containing Kubernetes resource templates | Like a recipe - tells Helm what ingredients (resources) and steps (configuration) needed |
| **Values** | Configuration parameters for customizing a chart | Like recipe substitutions - "use almond milk instead of regular milk" |
| **Release** | A specific instance of a chart deployed to a cluster | Like a meal made from a recipe - the actual result of using the chart |
| **Repository** | A collection of charts stored together | Like a cookbook - multiple recipes (charts) in one place |

### Container Registry Terms

| Term | What It Means | Why It Matters |
|------|---------------|----------------|
| **Container Registry** | A storage and distribution system for Docker images | Like GitHub but for Docker images instead of source code |
| **ECR (Elastic Container Registry)** | AWS's private container registry service | Where Rewardz stores all Docker images (like 985539790887.dkr.ecr.ap-southeast-1.amazonaws.com/auto_approver) |
| **OCI Registry** | Open Container Initiative registry - a standard way to store container images and Helm charts | Modern standard that works with both Docker images AND Helm charts. Think of it like a universal storage format that everyone agrees on. Docker Hub, ECR, and GitHub Container Registry all support OCI. |
| **Docker Hub** | Public container registry (like docker.io/nginx) | Like npm registry - free public images, but slower than private registries |
| **Image Tag** | A version label for an image (like :v1, :latest, :abc123) | Like version numbers - helps identify which version you're using |

### AWS Terms (Used in Rewardz)

| Term | What It Means | Purpose in Rewardz |
|------|---------------|-------------------|
| **EKS (Elastic Kubernetes Service)** | AWS's managed Kubernetes cluster | Where the auto-approver runs in production. AWS manages the control plane, we manage the applications |
| **EC2** | Virtual machines (servers) in AWS | The actual computers (nodes) running your Kubernetes pods |
| **S3 (Simple Storage Service)** | Object storage service for files | Stores receipt PDFs, processed documents, backups |
| **RDS (Relational Database Service)** | Managed PostgreSQL/MySQL databases | Where auto-approver stores audit tasks, results, receipts data |
| **Secrets Manager** | Secure storage for passwords, API keys | Stores DATABASE_PASSWORD, OPENAI_API_KEY, etc. |
| **Textract** | AWS OCR (Optical Character Recognition) service | Extracts text from receipt images |
| **IAM (Identity and Access Management)** | AWS permissions system | Controls who/what can access which AWS resources |
| **VPC (Virtual Private Cloud)** | Isolated network in AWS | Private network where your Kubernetes cluster runs |
| **ALB (Application Load Balancer)** | AWS load balancer for HTTP/HTTPS traffic | Distributes incoming web traffic across multiple pods |

### GitOps Terms

| Term | What It Means | Real-World Analogy |
|------|---------------|-------------------|
| **GitOps** | Using Git as the single source of truth for infrastructure | Like using blueprints - whatever is in Git is what should be running |
| **ArgoCD** | A GitOps tool that automatically syncs Git to Kubernetes | Like an architect's supervisor - ensures the building matches the blueprints |
| **Sync** | Applying changes from Git to the Kubernetes cluster | Like updating a building to match new blueprints |
| **ApplicationSet** | ArgoCD feature for managing multiple applications | Like a template for creating multiple similar projects |
| **Out of Sync** | When cluster state doesn't match Git | Like when construction diverges from blueprints - needs correction |

### Networking Terms

| Term | What It Means | Example |
|------|---------------|---------|
| **DNS (Domain Name System)** | Translates names to IP addresses | `api-private.skordev.com` → `52.220.123.45` |
| **FQDN (Fully Qualified Domain Name)** | Complete domain name including subdomain | `hello-service.default.svc.cluster.local` |
| **Port** | A numbered endpoint for network connections | `8000` in `localhost:8000` |
| **Load Balancing** | Distributing traffic across multiple servers/pods | Like a traffic cop directing cars to different lanes |
| **Reverse Proxy** | A server that routes requests to backend servers | Like a hotel concierge directing guests to rooms |

### Auto-Scaling Terms

| Term | What It Means | When It Happens |
|------|---------------|----------------|
| **HPA (Horizontal Pod Autoscaler)** | Kubernetes feature that scales pods based on CPU/memory | When your app's CPU usage exceeds 70%, add more pods |
| **KEDA** | Advanced autoscaler that supports custom metrics | More powerful than HPA - can scale based on queue length, HTTP requests, etc. |
| **Replica** | A copy of your pod | If you have 3 replicas, you have 3 identical pods running |
| **Scale Up** | Adding more pods to handle increased load | Lunch rush at restaurant - hire more servers |
| **Scale Down** | Removing pods when load decreases | Night time - fewer servers needed |

### CI/CD Terms

| Term | What It Means | In Rewardz |
|------|---------------|-----------|
| **CI (Continuous Integration)** | Automatically building/testing code when pushed to Git | Jenkins builds Docker image when you push code |
| **CD (Continuous Deployment)** | Automatically deploying tested code to production | ArgoCD deploys to EKS after image is built |
| **Jenkins** | Automation server for CI/CD pipelines | Builds Docker images, runs tests, pushes to ECR |
| **Pipeline** | A series of automated steps (build → test → deploy) | Like an assembly line for software |
| **Webhook** | An HTTP callback when something happens | GitHub tells Jenkins "code was pushed" |

### Architecture Terms

| Term | What It Means | In Auto-Approver |
|------|---------------|-----------------|
| **Microservice** | Small, independent service doing one thing well | Auto-approver is one microservice; frontend-app is another |
| **Monolith** | One large application doing everything | Old way - everything in one codebase |
| **Control Plane** | Brain of Kubernetes that makes decisions | Manages scheduling, monitors health, handles requests |
| **Worker Node** | Node that runs your actual application pods | Does the real work |
| **Multi-AZ (Availability Zone)** | Spread across multiple data centers for reliability | If one data center fails, others continue working |

### Storage Terms

| Term | What It Means | Example |
|------|---------------|---------|
| **Volume** | Storage attached to a pod | Like an external hard drive for a pod |
| **Persistent Volume** | Storage that survives pod restarts | Data remains even if pod is deleted |
| **Mount** | Attaching storage to a specific path | Mount S3 bucket at `/data` |
| **Object Storage** | Store files as objects (S3) | Like Google Drive - store any file type |
| **Block Storage** | Raw storage volume (EBS) | Like a hard drive - needs formatting |

### Development Terms

| Term | What It Means | When You Use It |
|------|---------------|----------------|
| **Environment** | Isolated deployment (dev, staging, prod) | Test in dev, validate in staging, release in prod |
| **Rollback** | Reverting to a previous version | Oops! The new version has bugs - go back to old version |
| **Rolling Update** | Gradually replacing old pods with new ones | Update 1 pod at a time - ensures zero downtime |
| **Health Check** | Regular test to see if application is working | Like a pulse check - is the app alive? |
| **Readiness Probe** | Check if pod is ready to receive traffic | Don't send requests until database connection is ready |
| **Liveness Probe** | Check if pod is still alive | If app crashes, restart the pod |

### Quick Reference: Common Acronyms

- **K8s** = Kubernetes (K + 8 letters + s)
- **API** = Application Programming Interface
- **YAML** = YAML Ain't Markup Language (config file format)
- **JSON** = JavaScript Object Notation (data format)
- **HTTP/HTTPS** = HyperText Transfer Protocol (Secure)
- **SSH** = Secure Shell (remote access)
- **CLI** = Command Line Interface
- **GUI** = Graphical User Interface
- **OCR** = Optical Character Recognition (reading text from images)
- **LLM** = Large Language Model (AI like GPT)

**💡 Pro Tip:** Bookmark this section! You can always come back here when you encounter an unfamiliar term in the labs.

---

## Prerequisites and Setup

### Verify Your Current Setup

**You already have these tools installed! Let's verify:**

```bash
# Check Docker version (yours: 28.5.1)
docker --version
# Expected: Docker version 28.5.1, build e180ab8

# Check kubectl version (yours: v1.34.2)
kubectl version --client
# Expected: Client Version: v1.34.2

# Check minikube version (yours: v1.37.0)
minikube version
# Expected: minikube version: v1.37.0

# Check Helm version (yours: v4.0.1)
helm version
# Expected: version.BuildInfo{Version:"v4.0.1", ...}
```

**✅ All tools are already installed and up to date!**

### Optional Tools (Highly Recommended)

**You also have these installed:**

```bash
# Check k9s version (yours: v0.50.16)
k9s version
# Expected: Version: 0.50.16

# Check ArgoCD CLI version (yours: v3.2.0)
argocd version --client
# Expected: argocd: v3.2.0+66b2f30
```

**If not installed yet:**

```bash
# Install k9s (terminal UI for Kubernetes - highly recommended)
brew install k9s

# Install ArgoCD CLI (for GitOps - Lab 11)
brew install argocd
```

**What these tools do:**

- **k9s v0.50.16**: Interactive terminal UI to manage Kubernetes - makes it easy to view/edit resources
- **ArgoCD v3.2.0**: GitOps continuous delivery tool - automates deployments from Git

### System Architecture Note

**You're running on Apple Silicon (darwin/arm64)** - all tools are optimized for M1/M2/M3 Macs.

**What this means:**
- ✅ Native ARM64 support for all Kubernetes tools
- ✅ Better performance and battery life
- ✅ Docker Desktop runs containers natively (no emulation)
- ⚠️ Some older Docker images may need `--platform linux/amd64` flag
- ⚠️ In this tutorial, we build our own images, so no issues!

### For Fresh Installation (Skip if Already Installed)

If you need to install these tools on another machine:

```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install all tools
brew install --cask docker      # Docker Desktop
brew install kubectl            # Kubernetes CLI
brew install minikube          # Local K8s cluster
brew install helm              # Package manager
brew install k9s               # Terminal UI (optional)
brew install argocd            # GitOps CLI (optional)
```

### Understanding What You Installed

- **Docker Desktop 28.5.1**: Runs containers on your Mac
- **kubectl v1.34.2**: Command-line tool to interact with Kubernetes clusters
- **minikube v1.37.0**: Creates a local Kubernetes cluster on your Mac
- **Helm v4.0.1**: Package manager for Kubernetes (like npm for Node.js)
- **k9s**: Beautiful terminal UI for navigating Kubernetes (optional)
- **argocd**: CLI for GitOps deployments

### Important Notes About Helm v4 and Rewardz Compatibility

**You're using Helm v4.0.1**, while **Rewardz production uses Helm v3**.

**Good News - Full Compatibility! ✅**

The Rewardz infrastructure uses:
- **Chart API version: v2** (in all Chart.yaml files)
- **Chart API v2** is compatible with both Helm v3 AND Helm v4
- All commands in this tutorial work identically in both versions

**Verified from Rewardz repositories:**
```yaml
# From: rewardz-microservices/apps/auto-approver/dev/Chart.yaml
apiVersion: v2  # ← Compatible with Helm v3 and v4
name: auto-approver
dependencies:
  - name: microservice
    repository: https://rewardz.github.io/kubernetes-charts/
    version: 0.1.0
```

**What's different in Helm v4 (but doesn't affect you):**
- ✅ Better **OCI registry** support (see glossary below)
- ✅ Improved dependency management
- ✅ Built-in chart signing and verification
- ⚠️ `--create-namespace` behavior changed slightly
- ⚠️ Some deprecated v2 features removed (none used in Rewardz)

**For this tutorial:**
- ✅ All commands work with your Helm v4.0.1
- ✅ All commands work in production Helm v3
- ✅ You can practice locally and apply knowledge to production
- ✅ No compatibility issues to worry about!

---

## Lab 1: Running Your First Container

**Goal**: Understand what containers are before diving into Kubernetes.

### Step 1: Create a Simple Python Web App

```bash
# Create a project directory
mkdir -p ~/k8s-tutorial/lab1
cd ~/k8s-tutorial/lab1

# Create a simple Flask app
cat > app.py << 'EOF'
from flask import Flask
import os
import socket

app = Flask(__name__)

@app.route('/')
def hello():
    hostname = socket.gethostname()
    version = os.getenv('APP_VERSION', 'v1.0')
    return f"""
    <h1>Hello from Kubernetes Tutorial!</h1>
    <p>Hostname: {hostname}</p>
    <p>Version: {version}</p>
    """

@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
EOF

# Create requirements.txt
cat > requirements.txt << 'EOF'
Flask==3.0.0
EOF

# Create Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

ENV APP_VERSION=v1.0

EXPOSE 8000

CMD ["python", "app.py"]
EOF
```

### Step 2: Build and Run Docker Container

```bash
# Build the Docker image
docker build -t hello-k8s:v1 .

# See the image
docker images | grep hello-k8s

# Run the container
docker run -d -p 8000:8000 --name hello-v1 hello-k8s:v1

# Test it
curl http://localhost:8000
curl http://localhost:8000/health

# View logs
docker logs hello-v1

# Stop and remove
docker stop hello-v1
docker rm hello-v1
```

### Step 3: Run Multiple Versions

```bash
# Build v2 with different environment variable
docker build -t hello-k8s:v2 --build-arg APP_VERSION=v2.0 .

# Run both versions on different ports
docker run -d -p 8001:8000 -e APP_VERSION=v1.0 --name hello-v1 hello-k8s:v1
docker run -d -p 8002:8000 -e APP_VERSION=v2.0 --name hello-v2 hello-k8s:v2

# Test both
curl http://localhost:8001  # Should show v1.0
curl http://localhost:8002  # Should show v2.0

# List running containers
docker ps

# Clean up
docker stop hello-v1 hello-v2
docker rm hello-v1 hello-v2
```

**Key Concepts Learned:**
- ✅ Containers package app + dependencies
- ✅ Same image can run multiple times with different configs
- ✅ Containers are isolated from each other
- ✅ Manual management doesn't scale (imagine 100 containers!)

---

## Lab 2: Local Kubernetes Cluster

**Goal**: Set up a local Kubernetes cluster using minikube.

### Step 1: Start Minikube

```bash
# Start minikube with Docker driver
minikube start --driver=docker --cpus=4 --memory=8192

# Check cluster status
minikube status

# View cluster information
kubectl cluster-info

# View nodes (your Mac is the "node")
kubectl get nodes

# Open Kubernetes dashboard (optional)
minikube dashboard
```

**What just happened?**
- Minikube created a Docker container that acts as a Kubernetes node
- Inside that container, all Kubernetes components are running
- Your kubectl is now configured to talk to this cluster

### Step 2: Explore the Cluster

```bash
# View all namespaces
kubectl get namespaces

# View system pods (Kubernetes control plane components)
kubectl get pods -n kube-system

# View all resources
kubectl get all -A

# Use k9s for better visualization (optional)
k9s
# Press 0 to see all namespaces
# Press :pods to see pods
# Press :deployments to see deployments
# Press :q to quit
```

**Key Concepts Learned:**
- ✅ Kubernetes cluster = Control plane + Worker nodes
- ✅ Control plane components run as pods
- ✅ Namespaces provide isolation
- ✅ kubectl is your primary tool for interaction

---

## Lab 3: Pods - The Smallest Unit

**Goal**: Deploy your app as a Kubernetes Pod.

### Step 1: Load Your Docker Image into Minikube

```bash
cd ~/k8s-tutorial/lab1

# Point Docker CLI to minikube's Docker daemon
eval $(minikube docker-env)

# Build image again (now it's inside minikube)
docker build -t hello-k8s:v1 .

# Verify image is in minikube
docker images | grep hello-k8s

# To go back to your normal Docker:
# eval $(minikube docker-env -u)
```

### Step 2: Create a Pod Manifest

```bash
cd ~/k8s-tutorial
mkdir -p lab3
cd lab3

# Create pod.yaml
cat > pod.yaml << 'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: hello-pod
  labels:
    app: hello
    version: v1
spec:
  containers:
  - name: hello-container
    image: hello-k8s:v1
    imagePullPolicy: Never  # Use local image
    ports:
    - containerPort: 8000
    env:
    - name: APP_VERSION
      value: "v1.0"
EOF
```

### Step 3: Deploy the Pod

```bash
# Apply the manifest
kubectl apply -f pod.yaml

# Watch pod being created
kubectl get pods -w
# Press Ctrl+C to stop watching

# View detailed pod information
kubectl describe pod hello-pod

# View logs
kubectl logs hello-pod

# Get pod IP address
kubectl get pod hello-pod -o wide
```

### Step 4: Access the Pod

```bash
# Port forward to access pod from your Mac
kubectl port-forward pod/hello-pod 8080:8000

# In another terminal, test it
curl http://localhost:8080
curl http://localhost:8080/health

# Stop port-forward with Ctrl+C
```

### Step 5: Execute Commands Inside Pod

```bash
# Get a shell inside the pod
kubectl exec -it hello-pod -- /bin/bash

# Inside the pod:
ps aux                    # See running processes
cat /etc/hostname         # Pod hostname
env | grep APP_VERSION    # Environment variables
curl localhost:8000       # Test app internally
exit

# Run single command
kubectl exec hello-pod -- ls -la /app
```

### Step 6: Pod Lifecycle

```bash
# Delete the pod
kubectl delete pod hello-pod

# Watch it terminate
kubectl get pods -w

# Try to access it
kubectl get pod hello-pod
# Error: pod "hello-pod" not found

# Recreate it
kubectl apply -f pod.yaml
```

**Key Concepts Learned:**
- ✅ Pod = one or more containers running together
- ✅ Pods have IPs but they're ephemeral (change when recreated)
- ✅ Pods don't self-heal (if deleted, they're gone)
- ✅ Labels help identify and group pods

---

## Lab 4: Deployments - Managing Multiple Pods

**Goal**: Use Deployments for replica management and rolling updates.

### Step 1: Create a Deployment

```bash
cd ~/k8s-tutorial
mkdir -p lab4
cd lab4

cat > deployment.yaml << 'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-deployment
  labels:
    app: hello
spec:
  replicas: 3  # Run 3 pods
  selector:
    matchLabels:
      app: hello
  template:
    metadata:
      labels:
        app: hello
    spec:
      containers:
      - name: hello-container
        image: hello-k8s:v1
        imagePullPolicy: Never
        ports:
        - containerPort: 8000
        env:
        - name: APP_VERSION
          value: "v1.0"
EOF
```

### Step 2: Deploy and Observe

```bash
# Clean up previous pod
kubectl delete pod hello-pod --ignore-not-found

# Apply deployment
kubectl apply -f deployment.yaml

# Watch pods being created
kubectl get pods -w

# View deployment
kubectl get deployment hello-deployment

# View replica set (created by deployment)
kubectl get replicaset
```

### Step 3: Self-Healing in Action

```bash
# Get pod names
kubectl get pods

# Delete one pod
kubectl delete pod <pod-name>

# Watch Kubernetes automatically recreate it
kubectl get pods -w

# The deployment ensures 3 pods are always running!
```

### Step 4: Scaling

```bash
# Scale up to 5 replicas
kubectl scale deployment hello-deployment --replicas=5

# Watch new pods starting
kubectl get pods -w

# Scale down to 2
kubectl scale deployment hello-deployment --replicas=2

# Watch pods terminating
kubectl get pods -w
```

### Step 5: Rolling Update (Zero Downtime)

```bash
# Build v2 of the image
cd ~/k8s-tutorial/lab1
eval $(minikube docker-env)
cat > app.py << 'EOF'
from flask import Flask
import os
import socket

app = Flask(__name__)

@app.route('/')
def hello():
    hostname = socket.gethostname()
    version = os.getenv('APP_VERSION', 'v2.0')
    return f"""
    <h1>Hello from Kubernetes Tutorial - VERSION 2!</h1>
    <p>Hostname: {hostname}</p>
    <p>Version: {version}</p>
    <p style="color: green;">New feature added!</p>
    """

@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
EOF

docker build -t hello-k8s:v2 .

# Update deployment to use v2
cd ~/k8s-tutorial/lab4
kubectl set image deployment/hello-deployment hello-container=hello-k8s:v2

# Watch rolling update happen
kubectl rollout status deployment/hello-deployment

# View rollout history
kubectl rollout history deployment/hello-deployment

# Check pods (notice the names changed)
kubectl get pods
```

### Step 6: Access Updated Application

```bash
# Port forward to any pod
POD_NAME=$(kubectl get pods -l app=hello -o jsonpath='{.items[0].metadata.name}')
kubectl port-forward pod/$POD_NAME 8080:8000

# Test (in another terminal)
curl http://localhost:8080
# Should show "VERSION 2" and "New feature added!"
```

### Step 7: Rollback

```bash
# Rollback to previous version
kubectl rollout undo deployment/hello-deployment

# Watch rollback
kubectl rollout status deployment/hello-deployment

# Test again
POD_NAME=$(kubectl get pods -l app=hello -o jsonpath='{.items[0].metadata.name}')
kubectl port-forward pod/$POD_NAME 8080:8000

curl http://localhost:8080
# Should show v1.0 again
```

**Key Concepts Learned:**
- ✅ Deployments manage ReplicaSets
- ✅ ReplicaSets ensure desired number of pods
- ✅ Self-healing: pods automatically recreated
- ✅ Scaling: change replica count
- ✅ Rolling updates: zero downtime deployments
- ✅ Rollback: revert to previous version

---

## Lab 5: Services - Networking Between Pods

**Goal**: Create stable networking for pods.

### Step 1: Create a Service

```bash
cd ~/k8s-tutorial
mkdir -p lab5
cd lab5

cat > service.yaml << 'EOF'
apiVersion: v1
kind: Service
metadata:
  name: hello-service
spec:
  selector:
    app: hello
  ports:
  - protocol: TCP
    port: 80        # Service port
    targetPort: 8000  # Container port
  type: ClusterIP   # Internal only
EOF
```

### Step 2: Deploy Service

```bash
# Apply service
kubectl apply -f service.yaml

# View service
kubectl get service hello-service

# Get service details
kubectl describe service hello-service

# Notice the CLUSTER-IP and ENDPOINTS
```

### Step 3: Test Service from Another Pod

```bash
# Create a test pod
kubectl run test-pod --image=curlimages/curl:latest --rm -it -- sh

# Inside the test pod:
curl http://hello-service
curl http://hello-service
curl http://hello-service
# Notice different hostnames - load balancing across pods!

# DNS works too:
curl http://hello-service.default.svc.cluster.local

exit
```

### Step 4: Service Types

```bash
# Change to NodePort (accessible from your Mac)
cat > service-nodeport.yaml << 'EOF'
apiVersion: v1
kind: Service
metadata:
  name: hello-service-nodeport
spec:
  selector:
    app: hello
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
    nodePort: 30080  # External port on node
  type: NodePort
EOF

kubectl apply -f service-nodeport.yaml

# Get minikube IP
minikube ip

# Access service
curl http://$(minikube ip):30080

# Or use minikube service command
minikube service hello-service-nodeport
```

### Step 5: Service Discovery

```bash
# Services create DNS entries automatically
kubectl run dns-test --image=busybox:latest --rm -it -- sh

# Inside pod:
nslookup hello-service
nslookup hello-service.default
nslookup hello-service.default.svc.cluster.local

exit
```

**Key Concepts Learned:**
- ✅ Services provide stable IPs for pods
- ✅ ClusterIP: internal access only
- ✅ NodePort: external access via node IP
- ✅ Load balancing: traffic distributed across pods
- ✅ DNS: services automatically get DNS names

---

## Lab 6: ConfigMaps and Secrets

**Goal**: Separate configuration from application code.

### Step 1: Create ConfigMap

```bash
cd ~/k8s-tutorial
mkdir -p lab6
cd lab6

# Create ConfigMap from literal values
kubectl create configmap hello-config \
  --from-literal=APP_ENV=development \
  --from-literal=LOG_LEVEL=DEBUG \
  --from-literal=FEATURE_FLAG=enabled

# View ConfigMap
kubectl get configmap hello-config
kubectl describe configmap hello-config

# Create from YAML
cat > configmap.yaml << 'EOF'
apiVersion: v1
kind: ConfigMap
metadata:
  name: hello-config-yaml
data:
  APP_ENV: "production"
  LOG_LEVEL: "INFO"
  FEATURE_FLAG: "enabled"
  config.json: |
    {
      "database": "postgres",
      "cache": "redis"
    }
EOF

kubectl apply -f configmap.yaml
```

### Step 2: Create Secret

```bash
# Create secret for sensitive data
kubectl create secret generic hello-secret \
  --from-literal=DATABASE_PASSWORD=supersecret123 \
  --from-literal=API_KEY=sk-abc123xyz

# View secret (values are base64 encoded)
kubectl get secret hello-secret
kubectl describe secret hello-secret

# Decode secret
kubectl get secret hello-secret -o jsonpath='{.data.DATABASE_PASSWORD}' | base64 --decode
```

### Step 3: Use ConfigMap and Secret in Deployment

```bash
cat > deployment-with-config.yaml << 'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-with-config
spec:
  replicas: 2
  selector:
    matchLabels:
      app: hello-config
  template:
    metadata:
      labels:
        app: hello-config
    spec:
      containers:
      - name: hello-container
        image: hello-k8s:v1
        imagePullPolicy: Never
        ports:
        - containerPort: 8000
        env:
        # Environment variables from ConfigMap
        - name: APP_ENV
          valueFrom:
            configMapKeyRef:
              name: hello-config-yaml
              key: APP_ENV
        - name: LOG_LEVEL
          valueFrom:
            configMapKeyRef:
              name: hello-config-yaml
              key: LOG_LEVEL
        # Environment variables from Secret
        - name: DATABASE_PASSWORD
          valueFrom:
            secretKeyRef:
              name: hello-secret
              key: DATABASE_PASSWORD
        - name: API_KEY
          valueFrom:
            secretKeyRef:
              name: hello-secret
              key: API_KEY
        # Mount ConfigMap as file
        volumeMounts:
        - name: config-volume
          mountPath: /app/config
      volumes:
      - name: config-volume
        configMap:
          name: hello-config-yaml
EOF

kubectl apply -f deployment-with-config.yaml
```

### Step 4: Verify Configuration

```bash
# Get a pod name
POD_NAME=$(kubectl get pods -l app=hello-config -o jsonpath='{.items[0].metadata.name}')

# Check environment variables
kubectl exec $POD_NAME -- env | grep -E 'APP_ENV|LOG_LEVEL|DATABASE_PASSWORD|API_KEY'

# Check mounted file
kubectl exec $POD_NAME -- cat /app/config/config.json
```

**Key Concepts Learned:**
- ✅ ConfigMaps store non-sensitive configuration
- ✅ Secrets store sensitive data (base64 encoded)
- ✅ Configuration injected as environment variables
- ✅ Configuration can be mounted as files
- ✅ Updating ConfigMap/Secret doesn't auto-restart pods

---

## Lab 7: Ingress - External Access

**Goal**: Set up HTTP routing to services.

### Step 1: Enable Ingress on Minikube

```bash
# Enable ingress addon
minikube addons enable ingress

# Wait for ingress controller to start
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=120s

# View ingress controller
kubectl get pods -n ingress-nginx
```

### Step 2: Create Ingress

```bash
cd ~/k8s-tutorial
mkdir -p lab7
cd lab7

cat > ingress.yaml << 'EOF'
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: hello-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$1
spec:
  rules:
  - host: hello.local
    http:
      paths:
      - path: /(.*)
        pathType: Prefix
        backend:
          service:
            name: hello-service
            port:
              number: 80
  - host: hello-v2.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: hello-service
            port:
              number: 80
EOF

kubectl apply -f ingress.yaml
```

### Step 3: Configure Local DNS

```bash
# Get minikube IP
MINIKUBE_IP=$(minikube ip)
echo $MINIKUBE_IP

# Add to /etc/hosts
echo "$MINIKUBE_IP hello.local hello-v2.local" | sudo tee -a /etc/hosts

# Verify ingress
kubectl get ingress hello-ingress
kubectl describe ingress hello-ingress
```

### Step 4: Test Ingress

```bash
# Test with curl
curl http://hello.local
curl http://hello-v2.local

# Test with browser
open http://hello.local
open http://hello-v2.local
```

### Step 5: Path-Based Routing

```bash
# Create second deployment and service
cat > deployment-v2.yaml << 'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-v2
spec:
  replicas: 2
  selector:
    matchLabels:
      app: hello
      version: v2
  template:
    metadata:
      labels:
        app: hello
        version: v2
    spec:
      containers:
      - name: hello-container
        image: hello-k8s:v2
        imagePullPolicy: Never
        ports:
        - containerPort: 8000
---
apiVersion: v1
kind: Service
metadata:
  name: hello-service-v2
spec:
  selector:
    app: hello
    version: v2
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
EOF

kubectl apply -f deployment-v2.yaml

# Update ingress for path routing
cat > ingress-paths.yaml << 'EOF'
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: hello-ingress-paths
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$2
spec:
  rules:
  - host: hello.local
    http:
      paths:
      - path: /v1(/|$)(.*)
        pathType: Prefix
        backend:
          service:
            name: hello-service
            port:
              number: 80
      - path: /v2(/|$)(.*)
        pathType: Prefix
        backend:
          service:
            name: hello-service-v2
            port:
              number: 80
EOF

kubectl apply -f ingress-paths.yaml

# Test path routing
curl http://hello.local/v1/
curl http://hello.local/v2/
```

**Key Concepts Learned:**
- ✅ Ingress provides HTTP/HTTPS routing
- ✅ Host-based routing (different domains)
- ✅ Path-based routing (different URLs)
- ✅ Ingress controller (nginx) handles traffic
- ✅ Similar to auto-approver's routing in Rewardz

---

## Lab 8: Namespaces - Environment Isolation

**Goal**: Use namespaces to separate environments.

### Step 1: Create Namespaces

```bash
cd ~/k8s-tutorial
mkdir -p lab8
cd lab8

# Create dev namespace
kubectl create namespace dev

# Create prod namespace
kubectl create namespace prod

# List namespaces
kubectl get namespaces
```

### Step 2: Deploy to Different Namespaces

```bash
# Deploy to dev
kubectl apply -f ~/k8s-tutorial/lab4/deployment.yaml -n dev
kubectl apply -f ~/k8s-tutorial/lab5/service.yaml -n dev

# Deploy to prod
kubectl apply -f ~/k8s-tutorial/lab4/deployment.yaml -n prod
kubectl apply -f ~/k8s-tutorial/lab5/service.yaml -n prod

# View resources by namespace
kubectl get pods -n dev
kubectl get pods -n prod
kubectl get all -n dev
kubectl get all -n prod
```

### Step 3: Set Default Namespace

```bash
# View current context
kubectl config get-contexts

# Set dev as default namespace
kubectl config set-context --current --namespace=dev

# Now commands default to dev namespace
kubectl get pods
# Same as: kubectl get pods -n dev

# Switch to prod
kubectl config set-context --current --namespace=prod
kubectl get pods

# Switch back to default
kubectl config set-context --current --namespace=default
```

### Step 4: Cross-Namespace Communication

```bash
# Create a pod in dev
kubectl run test-pod -n dev --image=curlimages/curl:latest --rm -it -- sh

# Inside pod, access service in same namespace
curl http://hello-service

# Access service in different namespace
curl http://hello-service.prod
curl http://hello-service.prod.svc.cluster.local

exit
```

### Step 5: Namespace Resource Quotas

```bash
cat > quota.yaml << 'EOF'
apiVersion: v1
kind: ResourceQuota
metadata:
  name: dev-quota
  namespace: dev
spec:
  hard:
    requests.cpu: "4"
    requests.memory: 4Gi
    limits.cpu: "8"
    limits.memory: 8Gi
    pods: "10"
EOF

kubectl apply -f quota.yaml

# View quota
kubectl get resourcequota -n dev
kubectl describe resourcequota dev-quota -n dev
```

**Key Concepts Learned:**
- ✅ Namespaces provide logical isolation
- ✅ Resources scoped to namespaces (pods, services, etc.)
- ✅ DNS works across namespaces
- ✅ Resource quotas limit namespace consumption
- ✅ Similar to dev/staging/prod in Rewardz EKS

---

## Lab 9: Auto-Scaling with HPA

**Goal**: Automatically scale based on CPU/memory.

### Step 1: Enable Metrics Server

```bash
# Enable metrics-server addon
minikube addons enable metrics-server

# Wait for metrics to be available
kubectl top nodes
kubectl top pods -n dev
```

### Step 2: Create Deployment with Resource Limits

```bash
cd ~/k8s-tutorial
mkdir -p lab9
cd lab9

cat > deployment-with-resources.yaml << 'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-hpa
  namespace: dev
spec:
  replicas: 1
  selector:
    matchLabels:
      app: hello-hpa
  template:
    metadata:
      labels:
        app: hello-hpa
    spec:
      containers:
      - name: hello-container
        image: hello-k8s:v1
        imagePullPolicy: Never
        ports:
        - containerPort: 8000
        resources:
          requests:
            cpu: 100m      # 0.1 CPU
            memory: 128Mi
          limits:
            cpu: 200m      # 0.2 CPU
            memory: 256Mi
EOF

kubectl apply -f deployment-with-resources.yaml
```

### Step 3: Create HPA (Horizontal Pod Autoscaler)

```bash
cat > hpa.yaml << 'EOF'
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: hello-hpa
  namespace: dev
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: hello-hpa
  minReplicas: 1
  maxReplicas: 5
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50  # Scale up if CPU > 50%
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 70  # Scale up if memory > 70%
EOF

kubectl apply -f hpa.yaml

# View HPA
kubectl get hpa -n dev
kubectl describe hpa hello-hpa -n dev
```

### Step 4: Generate Load

```bash
# Create service
cat > service-hpa.yaml << 'EOF'
apiVersion: v1
kind: Service
metadata:
  name: hello-hpa-service
  namespace: dev
spec:
  selector:
    app: hello-hpa
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: NodePort
EOF

kubectl apply -f service-hpa.yaml

# In one terminal, watch HPA and pods
watch -n 1 'kubectl get hpa,pods -n dev | grep hello-hpa'

# In another terminal, generate load
kubectl run load-generator -n dev --image=busybox:latest --rm -it -- sh

# Inside the pod:
while true; do wget -q -O- http://hello-hpa-service; done
```

### Step 5: Observe Scaling

```bash
# Watch HPA in action (in first terminal)
kubectl get hpa -n dev -w

# You'll see:
# - CPU usage increases
# - Replicas scale from 1 → 2 → 3 → etc.
# - After load stops, cooldown period, then scale down
```

**Key Concepts Learned:**
- ✅ HPA automatically scales based on metrics
- ✅ Requires resource requests/limits
- ✅ Metrics server provides CPU/memory data
- ✅ Similar to KEDA in Rewardz (more advanced)
- ✅ Cooldown prevents flapping

---

## Lab 10: Helm Charts

**Goal**: Package Kubernetes applications with Helm.

### Step 1: Create a Helm Chart

```bash
cd ~/k8s-tutorial
mkdir -p lab10
cd lab10

# Create chart structure
helm create hello-chart

# View structure
tree hello-chart
```

### Step 2: Customize the Chart

```bash
# Edit values.yaml
cat > hello-chart/values.yaml << 'EOF'
replicaCount: 2

image:
  repository: hello-k8s
  tag: v1
  pullPolicy: Never

service:
  type: ClusterIP
  port: 80
  targetPort: 8000

ingress:
  enabled: true
  className: nginx
  hosts:
    - host: hello-helm.local
      paths:
        - path: /
          pathType: Prefix

resources:
  limits:
    cpu: 200m
    memory: 256Mi
  requests:
    cpu: 100m
    memory: 128Mi

env:
  - name: APP_VERSION
    value: "helm-v1.0"
  - name: APP_ENV
    value: "production"
EOF

# Simplify deployment template
cat > hello-chart/templates/deployment.yaml << 'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "hello-chart.fullname" . }}
  labels:
    {{- include "hello-chart.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "hello-chart.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "hello-chart.selectorLabels" . | nindent 8 }}
    spec:
      containers:
      - name: {{ .Chart.Name }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
        imagePullPolicy: {{ .Values.image.pullPolicy }}
        ports:
        - name: http
          containerPort: {{ .Values.service.targetPort }}
          protocol: TCP
        env:
        {{- toYaml .Values.env | nindent 10 }}
        resources:
          {{- toYaml .Values.resources | nindent 12 }}
EOF
```

### Step 3: Install Chart

```bash
# Dry run to see generated manifests
helm install hello-release hello-chart --dry-run --debug

# Install the chart
helm install hello-release hello-chart -n dev

# List releases
helm list -n dev

# View resources
kubectl get all -n dev -l app.kubernetes.io/instance=hello-release
```

### Step 4: Upgrade Release

```bash
# Create dev-values.yaml for environment-specific config
cat > dev-values.yaml << 'EOF'
replicaCount: 3

env:
  - name: APP_VERSION
    value: "dev-v1.0"
  - name: APP_ENV
    value: "development"
  - name: LOG_LEVEL
    value: "DEBUG"
EOF

# Upgrade release
helm upgrade hello-release hello-chart -n dev -f dev-values.yaml

# View revision history
helm history hello-release -n dev
```

### Step 5: Rollback

```bash
# Rollback to previous revision
helm rollback hello-release 1 -n dev

# Verify
helm history hello-release -n dev
```

### Step 6: Template Multiple Environments

```bash
# Create prod-values.yaml
cat > prod-values.yaml << 'EOF'
replicaCount: 5

image:
  tag: v2

env:
  - name: APP_VERSION
    value: "prod-v2.0"
  - name: APP_ENV
    value: "production"
  - name: LOG_LEVEL
    value: "INFO"

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi
EOF

# Install to prod namespace
helm install hello-release-prod hello-chart -n prod -f prod-values.yaml

# Compare
kubectl get deployment -n dev
kubectl get deployment -n prod
```

### Step 7: Package and Share

```bash
# Package chart
helm package hello-chart

# Inspect package
ls -lh hello-chart-*.tgz

# Install from package
helm install hello-from-package hello-chart-0.1.0.tgz -n dev --create-namespace
```

**Key Concepts Learned:**
- ✅ Helm charts = templates + values
- ✅ Values files customize deployments
- ✅ Same chart for multiple environments
- ✅ Revision history and rollbacks
- ✅ Similar to "microservice" chart in Rewardz

---

## Lab 11: GitOps with ArgoCD

**Goal**: Implement GitOps workflow like Rewardz infrastructure.

### Step 1: Install ArgoCD

```bash
# Create namespace
kubectl create namespace argocd

# Install ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Wait for pods to be ready
kubectl wait --for=condition=ready pod --all -n argocd --timeout=300s

# Get initial admin password
ARGOCD_PASSWORD=$(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 --decode)
echo "ArgoCD Password: $ARGOCD_PASSWORD"

# Port forward ArgoCD UI
kubectl port-forward svc/argocd-server -n argocd 8080:443 &

# Open in browser
open https://localhost:8080
# Username: admin
# Password: (from above)
```

### Step 2: Create Git Repository

```bash
# Create a local git repo to simulate GitHub
cd ~/k8s-tutorial
mkdir -p lab11/gitops-repo
cd lab11/gitops-repo

git init
git config user.email "you@example.com"
git config user.name "Your Name"

# Create application structure (like rewardz-microservices)
mkdir -p apps/hello-app/dev
mkdir -p apps/hello-app/prod

# Create dev environment config
cat > apps/hello-app/dev/values.yaml << 'EOF'
replicaCount: 2

image:
  repository: hello-k8s
  tag: v1
  pullPolicy: Never

service:
  type: ClusterIP
  port: 80

env:
  - name: APP_ENV
    value: "dev"
  - name: LOG_LEVEL
    value: "DEBUG"
EOF

# Create prod environment config
cat > apps/hello-app/prod/values.yaml << 'EOF'
replicaCount: 5

image:
  repository: hello-k8s
  tag: v2
  pullPolicy: Never

service:
  type: ClusterIP
  port: 80

env:
  - name: APP_ENV
    value: "prod"
  - name: LOG_LEVEL
    value: "INFO"
EOF

# Commit
git add .
git commit -m "Initial commit: hello-app configurations"
```

### Step 3: Create ArgoCD Application

```bash
# Create application YAML
cat > apps/hello-app/dev/application.yaml << 'EOF'
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: hello-app-dev
  namespace: argocd
spec:
  project: default
  source:
    repoURL: file:///Users/ankit/k8s-tutorial/lab11/gitops-repo
    targetRevision: HEAD
    path: apps/hello-app/dev
  destination:
    server: https://kubernetes.default.svc
    namespace: dev
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
EOF

# Apply application (but won't sync yet because we need the chart)
# kubectl apply -f apps/hello-app/dev/application.yaml
```

### Step 4: Copy Helm Chart to Repo

```bash
# Copy helm chart from lab10
cp -r ~/k8s-tutorial/lab10/hello-chart apps/hello-app/

# Update dev to use chart
cat > apps/hello-app/dev/Chart.yaml << 'EOF'
apiVersion: v2
name: hello-app-dev
description: Hello app for dev environment
type: application
version: 0.1.0
dependencies:
  - name: hello-chart
    version: 0.1.0
    repository: file://../hello-chart
EOF

# Commit
git add .
git commit -m "Add Helm chart and ArgoCD application"
```

### Step 5: Create Application via ArgoCD CLI

```bash
# Login to ArgoCD
argocd login localhost:8080 --username admin --password $ARGOCD_PASSWORD --insecure

# Create application
argocd app create hello-app-dev \
  --repo file:///Users/ankit/k8s-tutorial/lab11/gitops-repo \
  --path apps/hello-app/dev \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace dev \
  --sync-policy automated \
  --self-heal \
  --auto-prune

# View application
argocd app get hello-app-dev

# Sync application
argocd app sync hello-app-dev

# Watch sync progress
argocd app wait hello-app-dev
```

### Step 6: GitOps Workflow - Make Changes

```bash
cd ~/k8s-tutorial/lab11/gitops-repo

# Update dev environment to use 3 replicas
cat > apps/hello-app/dev/values.yaml << 'EOF'
replicaCount: 3  # Changed from 2 to 3

image:
  repository: hello-k8s
  tag: v1
  pullPolicy: Never

service:
  type: ClusterIP
  port: 80

env:
  - name: APP_ENV
    value: "dev"
  - name: LOG_LEVEL
    value: "DEBUG"
  - name: FEATURE_NEW
    value: "enabled"  # New feature!
EOF

# Commit change
git add .
git commit -m "Scale dev to 3 replicas and enable new feature"

# ArgoCD will detect change and auto-sync
# Watch in UI or CLI
argocd app get hello-app-dev --watch
```

### Step 7: Observe GitOps in Action

```bash
# View pods - should see 3 replicas now
kubectl get pods -n dev

# Check environment variable
POD_NAME=$(kubectl get pods -n dev -l app.kubernetes.io/instance=hello-app-dev -o jsonpath='{.items[0].metadata.name}')
kubectl exec -n dev $POD_NAME -- env | grep FEATURE_NEW
```

**Key Concepts Learned:**
- ✅ GitOps: Git as single source of truth
- ✅ ArgoCD continuously monitors Git repo
- ✅ Automated sync and self-healing
- ✅ Audit trail via Git commits
- ✅ Similar to rewardz-microservices workflow

---

## Lab 12: Deploying Auto-Approver Locally

**Goal**: Simulate the full auto-approver deployment.

### Step 1: Prepare Auto-Approver Image

```bash
cd ~/code/microservices/ai

# Build Docker image
eval $(minikube docker-env)
docker build -t auto-approver:local .

# Verify
docker images | grep auto-approver
```

### Step 2: Create Local Helm Values

```bash
cd ~/k8s-tutorial
mkdir -p lab12
cd lab12

cat > auto-approver-local-values.yaml << 'EOF'
replicaCount: 2

image:
  repository: auto-approver
  tag: local
  pullPolicy: Never

service:
  type: ClusterIP
  port: 80
  targetPort: 8000

ingress:
  enabled: true
  className: nginx
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$1
  hosts:
    - host: auto-approver.local
      paths:
        - path: /(.*)
          pathType: Prefix

resources:
  limits:
    cpu: 2048m
    memory: 2048Mi
  requests:
    cpu: 512m
    memory: 512Mi

env:
  - name: APP_ENV
    value: "local"
  - name: ROOT_PATH
    value: "/"
  - name: LOG_LEVEL
    value: "DEBUG"
  - name: DATABASE_URL
    value: "sqlite:///./local.db"
  # Add other required environment variables

initContainers:
  - name: migrations
    image: auto-approver:local
    imagePullPolicy: Never
    command: ["poetry", "run", "alembic", "upgrade", "head"]
    env:
      - name: DATABASE_URL
        value: "sqlite:///./local.db"
EOF
```

### Step 3: Deploy with Helm

```bash
# Use the chart from lab10
helm upgrade --install auto-approver-local \
  ~/k8s-tutorial/lab10/hello-chart \
  -f auto-approver-local-values.yaml \
  -n dev \
  --create-namespace

# Watch deployment
kubectl get pods -n dev -w
```

### Step 4: Set Up Local DNS

```bash
# Add to /etc/hosts
MINIKUBE_IP=$(minikube ip)
echo "$MINIKUBE_IP auto-approver.local" | sudo tee -a /etc/hosts

# Test
curl http://auto-approver.local/health
curl http://auto-approver.local/docs
```

### Step 5: Simulate Full Stack

```bash
# Create ConfigMap for app-config
kubectl create configmap auto-approver-config -n dev \
  --from-file=~/code/microservices/ai/app-config/dev.yaml

# Create Secret (simulate AWS Secrets Manager)
kubectl create secret generic auto-approver-secret -n dev \
  --from-literal=DATABASE_PASSWORD=local123 \
  --from-literal=OPENAI_API_KEY=sk-test \
  --from-literal=AWS_ACCESS_KEY_ID=test \
  --from-literal=AWS_SECRET_ACCESS_KEY=test

# Update deployment to use them
# (Similar to values.yaml in rewardz-microservices)
```

### Step 6: Test Complete Flow

```bash
# Port forward to access application
kubectl port-forward -n dev svc/auto-approver-local 8000:80

# Test API
curl http://localhost:8000/health
curl http://localhost:8000/v1/audit-tasks/

# View logs
kubectl logs -n dev -l app.kubernetes.io/instance=auto-approver-local -f

# Scale replicas
kubectl scale deployment auto-approver-local -n dev --replicas=3

# Watch rolling update
kubectl rollout status deployment auto-approver-local -n dev
```

### Step 7: Compare to Production

```bash
# Your local setup mirrors production:
# ✅ Docker image
# ✅ Kubernetes deployment
# ✅ ConfigMap/Secret management
# ✅ Ingress routing
# ✅ Resource limits
# ✅ Multiple replicas
# ✅ Health checks

# The only differences:
# - Local: minikube cluster
# - Prod: EKS cluster
# - Local: NodePort/port-forward access
# - Prod: AWS Load Balancer
# - Local: SQLite database
# - Prod: RDS PostgreSQL
# - Local: No AWS services (S3, Textract)
# - Prod: Full AWS integration
```

---

## Complete Kubernetes Concepts Map

### What You Learned vs. What's in Rewardz EKS

| Concept | Lab | Rewardz Usage |
|---------|-----|---------------|
| **Containers** | Lab 1 | Docker images in ECR |
| **Pods** | Lab 3 | Auto-approver pods |
| **Deployments** | Lab 4 | `auto-approver-dev-deployment` |
| **Services** | Lab 5 | `auto-approver-dev-service` |
| **Ingress** | Lab 7 | nginx-private ingress controller |
| **ConfigMaps** | Lab 6 | `configData` in values.yaml |
| **Secrets** | Lab 6 | AWS Secrets Manager + ExternalSecrets |
| **Namespaces** | Lab 8 | `dev`, `prod` namespaces |
| **HPA** | Lab 9 | KEDA `scalingPolicy` |
| **Helm** | Lab 10 | `microservice` chart |
| **GitOps** | Lab 11 | ArgoCD + rewardz-microservices |

---

## Advanced Topics (Beyond This Tutorial)

### KEDA (Kubernetes Event-Driven Autoscaling)
- More advanced than HPA
- Scales based on custom metrics (queue length, etc.)
- Used in auto-approver for Celery worker scaling

### ExternalSecrets Operator
- Syncs AWS Secrets Manager → Kubernetes Secrets
- Auto-updates when AWS secrets change
- Used for all sensitive configuration

### StatefulSets
- For stateful applications (databases, etc.)
- Stable network identities
- Ordered deployment/scaling

### DaemonSets
- One pod per node
- Useful for logging, monitoring agents

### Jobs and CronJobs
- Run tasks to completion
- Scheduled tasks (like cron)

### Service Mesh (Istio)
- Advanced traffic management
- Observability
- Security (mTLS)

---

## Troubleshooting Common Issues

### Pods Not Starting

```bash
# Check pod status
kubectl get pods -n dev

# Describe pod for events
kubectl describe pod <pod-name> -n dev

# View logs
kubectl logs <pod-name> -n dev

# Common issues:
# - ImagePullBackOff: Image not found
#   Solution: Check image name, use `imagePullPolicy: Never` for local
# - CrashLoopBackOff: App crashes on startup
#   Solution: Check logs, fix application
# - Pending: Insufficient resources
#   Solution: Scale down other apps or add nodes
```

### Service Not Accessible

```bash
# Check service endpoints
kubectl get endpoints -n dev

# If no endpoints, check selector matches pods
kubectl get pods -n dev --show-labels
kubectl describe service <service-name> -n dev

# Test from inside cluster
kubectl run test --image=curlimages/curl --rm -it -- curl http://<service-name>
```

### Ingress Not Working

```bash
# Check ingress status
kubectl get ingress -n dev
kubectl describe ingress <ingress-name> -n dev

# Check ingress controller logs
kubectl logs -n ingress-nginx -l app.kubernetes.io/component=controller

# Verify /etc/hosts
cat /etc/hosts | grep local

# Test with curl verbose
curl -v http://<host>
```

### Minikube Issues

```bash
# Restart minikube
minikube stop
minikube start

# Delete and recreate
minikube delete
minikube start --driver=docker --cpus=4 --memory=8192

# Check status
minikube status
kubectl get nodes
```

---

## Clean Up

```bash
# Delete all labs
kubectl delete namespace dev prod

# Delete ArgoCD
kubectl delete namespace argocd

# Stop minikube
minikube stop

# Delete minikube cluster
minikube delete

# Remove from /etc/hosts
sudo sed -i '' '/\.local/d' /etc/hosts
```

---

## Next Steps

### Practice Exercises

1. **Exercise 1: Blue-Green Deployment**
   - Deploy v1 with blue label
   - Deploy v2 with green label
   - Switch service selector to change versions instantly

2. **Exercise 2: Canary Deployment**
   - Deploy v1 with 90% traffic
   - Deploy v2 with 10% traffic
   - Gradually shift traffic to v2

3. **Exercise 3: Multi-Service Application**
   - Deploy frontend + backend + database
   - Configure networking between them
   - Expose only frontend via ingress

4. **Exercise 4: CI/CD Pipeline**
   - Create GitHub repo
   - Set up GitHub Actions to build Docker image
   - Auto-update Helm values on successful build
   - ArgoCD auto-deploys

### Real-World Projects

1. **Migrate auto-approver completely to local Kubernetes**
   - Use PostgreSQL instead of SQLite
   - Deploy Redis for Celery
   - Deploy Celery worker pods
   - Set up monitoring (Prometheus/Grafana)

2. **Create shared microservice chart**
   - Build reusable Helm chart
   - Deploy multiple microservices using it
   - Implement best practices from Rewardz

### Resources

- **Kubernetes Docs**: https://kubernetes.io/docs/
- **Kubernetes By Example**: https://kubernetesbyexample.com/
- **Helm Docs**: https://helm.sh/docs/
- **ArgoCD Docs**: https://argo-cd.readthedocs.io/
- **CNCF Landscape**: https://landscape.cncf.io/

---

## Summary

You've now learned:

✅ **Containers and Docker** - Building and running containerized applications
✅ **Kubernetes Fundamentals** - Pods, Deployments, Services, Ingress
✅ **Configuration Management** - ConfigMaps and Secrets
✅ **Environment Isolation** - Namespaces
✅ **Auto-Scaling** - HPA for automatic resource management
✅ **Package Management** - Helm charts and values
✅ **GitOps** - ArgoCD for declarative deployments
✅ **Production Simulation** - Deploying auto-approver locally

**These are the exact same concepts used in the Rewardz EKS cluster!**

The main difference between your local setup and production:
- **Infrastructure**: Minikube vs. AWS EKS
- **Scale**: Few pods vs. dozens/hundreds
- **Services**: Local files vs. AWS S3, RDS, Secrets Manager
- **Networking**: Local ingress vs. AWS Load Balancer

But the **Kubernetes concepts are identical**!

---

**Congratulations!** You now have hands-on experience with all Kubernetes concepts used in the Rewardz organization! 🎉

Continue practicing, experiment with different configurations, and you'll be a Kubernetes expert in no time!

---

## Appendix: Mapping Tutorial to Rewardz Production

### Local vs. Production Architecture

| Component | Your Tutorial | Rewardz Production |
|-----------|--------------|-------------------|
| **Cluster** | minikube (single node) | AWS EKS (multi-node, multi-AZ) |
| **Nodes** | 1 Docker container | Multiple EC2 instances |
| **Image Registry** | Local Docker cache | AWS ECR (985539790887.dkr.ecr...) |
| **Ingress** | minikube nginx | AWS ALB + nginx-private |
| **DNS** | /etc/hosts hacks | Route53 + real domains |
| **Secrets** | kubectl secrets | AWS Secrets Manager + ExternalSecrets |
| **Database** | SQLite in pod | AWS RDS PostgreSQL |
| **Storage** | Pod filesystem | AWS S3 |
| **Monitoring** | kubectl logs | CloudWatch + Prometheus + Grafana |
| **GitOps** | Local ArgoCD | Production ArgoCD cluster |
| **CI/CD** | Manual builds | Jenkins + GitHub webhooks |

### Your Auto-Approver Values.yaml Explained

Now that you understand Helm, let's revisit the production values.yaml:

```yaml
# From: apps/auto-approver/dev/values.yaml
microservice:
  # Lab 3-4: Container image (built by Jenkins, stored in ECR)
  image: 985539790887.dkr.ecr.ap-southeast-1.amazonaws.com/auto_approver:feature-056acf

  # Lab 7: Ingress routing
  ingress:
    ingressHost: api-private.skordev.com
    path: "/dev/auto-approver/(.*)"
    className: nginx-private

  # Lab 12: Database migrations (init container pattern)
  migration:
    enabled: true
    command: ["poetry", "run", "alembic", "-x", "env=prod", "upgrade", "head"]

  # Lab 6: Secrets from AWS Secrets Manager
  secretPaths:
    - /dev/auto-approver/SECRET

  # Lab 4: Resource limits (prevents pod from consuming too much)
  resources:
    memory: "2048Mi"
    cpu: "2048m"

  # Lab 6: ConfigMap (non-sensitive config)
  configData:
    APP_ENV: "prod"
    ROOT_PATH: "/dev/auto-approver"
    LOG_LEVEL: "INFO"
    OCR_PROVIDER: "aws_textract"

  # Lab 3: Container port
  containerPort: 8000

  # Lab 9: Auto-scaling (KEDA is more advanced than HPA)
  scalingPolicy:
    enabled: true
    minReplicaCount: 1
    maxReplicaCount: 10
    triggers:
      cpu:
        targetUtilization: "70"

  # Lab 4: Additional components (like sidecar containers)
  additionalComponents:
    - name: worker
      enabled: true
      command: ["poetry", "run", "celery", "-A", "cerra_ai.infrastructure.celery", "worker"]
```

### Commands You Can Run in Production

**View your application in EKS:**

```bash
# Set kubeconfig to EKS (you need AWS credentials)
aws eks update-kubeconfig --name <cluster-name> --region ap-southeast-1

# View pods (just like Lab 3!)
kubectl get pods -n dev | grep auto-approver

# View logs (just like Lab 3!)
kubectl logs -n dev <pod-name>

# View deployment (just like Lab 4!)
kubectl get deployment -n dev auto-approver-dev-deployment

# Describe ingress (just like Lab 7!)
kubectl describe ingress -n dev auto-approver-dev-ingress

# View ConfigMap (just like Lab 6!)
kubectl get configmap -n dev auto-approver-dev-configmap -o yaml

# View HPA/KEDA (just like Lab 9!)
kubectl get scaledobject -n dev auto-approver-dev-scaledobject
```

**The commands are identical!** You learned on minikube, but the concepts apply to production EKS!

### Understanding the Full Deployment Flow

**When you push code to GitHub:**

1. **Jenkins CI** (automated):
   ```bash
   # What Jenkins does (you learned this in Lab 1):
   docker build -t auto_approver:abc123 .
   docker push 985539790887.dkr.ecr...com/auto_approver:abc123
   ```

2. **Update Infrastructure Repo** (manual or automated):
   ```bash
   # Someone updates (you learned Helm values in Lab 10):
   # File: apps/auto-approver/dev/values.yaml
   # Change: image: ...auto_approver:feature-056acf → abc123
   git commit -m "Deploy auto-approver abc123 to dev"
   git push
   ```

3. **ArgoCD GitOps** (automated - Lab 11):
   ```bash
   # ArgoCD detects change and syncs (you learned this in Lab 11!)
   argocd app sync auto-approver-dev
   ```

4. **Kubernetes Rolling Update** (automated - Lab 4):
   ```
   # EKS performs rolling update (you learned this in Lab 4!)
   Old pods: 3 → 2 → 1 → 0
   New pods: 0 → 1 → 2 → 3
   Zero downtime!
   ```

### What You Should Do Next

**1. Practice on Minikube (This Week):**
- Complete all 12 labs
- Experiment with breaking things and fixing them
- Try the practice exercises
- Build confidence with kubectl commands

**2. Access EKS Cluster (Next Week):**
- Get AWS credentials for EKS access
- Configure kubectl for EKS
- Read-only exploration: view pods, logs, deployments
- Compare with your local setup

**3. Make Your First Deployment (When Ready):**
- Create a feature branch
- Make a small code change
- Test locally with minikube
- Push to GitHub → Jenkins builds → Update values.yaml → ArgoCD deploys!

**4. Deepen Your Knowledge:**
- Read the Rewardz microservices README
- Study the shared microservice Helm chart
- Learn about KEDA (more advanced than HPA)
- Understand ExternalSecrets operator

### Troubleshooting Production Issues

**Now you know how to debug!**

```bash
# Pod not starting? (Lab 3-4)
kubectl describe pod <pod-name> -n dev
kubectl logs <pod-name> -n dev

# Service not reachable? (Lab 5)
kubectl get endpoints -n dev
kubectl describe service <service-name> -n dev

# Ingress routing broken? (Lab 7)
kubectl describe ingress <ingress-name> -n dev
kubectl logs -n ingress-nginx <controller-pod>

# Scaling issues? (Lab 9)
kubectl get hpa -n dev
kubectl describe scaledobject <name> -n dev

# Config problems? (Lab 6)
kubectl get configmap <name> -n dev -o yaml
kubectl get secret <name> -n dev -o yaml
```

**The debugging commands you learned apply directly to production!**

### Final Tips

**✅ Do:**
- Use `k9s` for interactive exploration (faster than kubectl)
- Always check logs first when debugging
- Test changes in dev namespace before prod
- Use `kubectl describe` to understand resource state
- Read the events section in describe output

**❌ Don't:**
- Delete production resources without confirmation
- Edit resources directly (use GitOps workflow)
- Scale down production deployments to 0
- Change secrets without coordinating with team
- Force-delete stuck resources (understand why first)

### Reference: Quick Command Cheatsheet

```bash
# Context and namespace
kubectl config get-contexts
kubectl config set-context --current --namespace=dev

# Resources
kubectl get pods,svc,deploy,ingress -n dev
kubectl get all -n dev

# Details
kubectl describe pod <name> -n dev
kubectl logs <name> -n dev -f
kubectl logs <name> -n dev --previous  # Previous crashed container

# Debugging
kubectl exec -it <pod-name> -n dev -- bash
kubectl port-forward pod/<name> 8000:8000 -n dev
kubectl top pods -n dev

# ArgoCD
argocd app list
argocd app get auto-approver-dev
argocd app sync auto-approver-dev
argocd app logs auto-approver-dev

# Helm
helm list -n dev
helm history <release> -n dev
helm get values <release> -n dev
```

---

**You're now ready to work with Kubernetes in the Rewardz organization!** 🚀

The tutorial gave you hands-on experience with every concept used in production. The only difference is scale - but the fundamentals are identical.

**Welcome to the world of Kubernetes!** 🎉
