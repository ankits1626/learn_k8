# Checkpoint 00: Docker Fundamentals - From Zero to Hero

**Goal**: Master Docker basics by building a simple 3-service Python system (Orchestrator, Worker, Redis) from scratch. Then migrate it to Kubernetes in later checkpoints.

**Time**: 2-3 hours

**Prerequisites**:
- Docker Desktop installed (you already have this!)
- Python 3.11+ installed
- Basic Python knowledge

---

## Table of Contents

1. [Part 1: Docker Basics - Single Container](#part-1-docker-basics---single-container)
2. [Part 2: Dockerfile - Build Your Own Image](#part-2-dockerfile---build-your-own-image)
3. [Part 3: Docker Networks - Connect Containers](#part-3-docker-networks---connect-containers)
4. [Part 4: Docker Compose - Multi-Container Apps](#part-4-docker-compose---multi-container-apps)
5. [Part 5: Build the Complete System](#part-5-build-the-complete-system)
6. [Part 6: Docker Best Practices](#part-6-docker-best-practices)

---

## Learning Path Overview

```
Part 1: Single Container (15 min)
  └─> Run Redis, understand containers

Part 2: Build Images (30 min)
  └─> Write Dockerfile, build Python app

Part 3: Networks (20 min)
  └─> Connect containers, DNS resolution

Part 4: Docker Compose (30 min)
  └─> Multi-container orchestration

Part 5: Complete System (45 min)
  └─> Build Orchestrator + Worker + Redis

Part 6: Best Practices (15 min)
  └─> Production patterns
```

---

## Part 1: Docker Basics - Single Container

### What is Docker?

**Docker** packages your application and all its dependencies into a **container** - a lightweight, standalone executable package.

**Key Concepts:**
- **Image**: Blueprint (like a class in OOP)
- **Container**: Running instance (like an object)
- **Registry**: Image storage (like npm registry, but for Docker images)

### Step 1.1: Run Your First Container

```bash
# Pull and run Redis (a database)
docker run -d --name my-redis redis:7-alpine

# Explanation:
# -d              = Run in background (detached)
# --name my-redis = Give it a friendly name
# redis:7-alpine  = Image name:tag
```

**Expected output:**
```
Unable to find image 'redis:7-alpine' locally
7-alpine: Pulling from library/redis
...
Status: Downloaded newer image for redis:7-alpine
a1b2c3d4e5f6...  (container ID)
```

### Step 1.2: Inspect the Container

```bash
# List running containers
docker ps

# Expected output:
# CONTAINER ID   IMAGE           COMMAND                  STATUS         PORTS      NAMES
# a1b2c3d4e5f6   redis:7-alpine  "docker-entrypoint.s…"   Up 10 seconds  6379/tcp   my-redis
```

**What you see:**
- **CONTAINER ID**: Unique identifier
- **IMAGE**: What image it's running
- **STATUS**: How long it's been running
- **PORTS**: What network ports it exposes
- **NAMES**: Friendly name you gave it

### Step 1.3: Interact with the Container

```bash
# Execute a command inside the running container
docker exec -it my-redis redis-cli

# You're now inside Redis!
# Try some commands:
127.0.0.1:6379> PING
PONG
127.0.0.1:6379> SET mykey "Hello from Docker"
OK
127.0.0.1:6379> GET mykey
"Hello from Docker"
127.0.0.1:6379> exit
```

**What just happened?**
- `docker exec` = Execute command in running container
- `-it` = Interactive terminal
- `redis-cli` = Redis command-line interface

### Step 1.4: View Container Logs

```bash
# See what's happening inside
docker logs my-redis

# Follow logs in real-time (like tail -f)
docker logs -f my-redis

# Press Ctrl+C to stop following
```

### Step 1.5: Stop and Remove

```bash
# Stop the container
docker stop my-redis

# Remove the container
docker rm my-redis

# Verify it's gone
docker ps -a
```

### 🎯 Checkpoint 1 Quiz

**Q1**: What's the difference between an image and a container?
<details>
<summary>Answer</summary>
Image = blueprint (recipe), Container = running instance (actual meal)
</details>

**Q2**: What does `-d` flag do?
<details>
<summary>Answer</summary>
Runs container in detached mode (background), so you get your terminal back
</details>

---

## Part 2: Dockerfile - Build Your Own Image

### What is a Dockerfile?

A **Dockerfile** is a recipe for building your own Docker image. It contains instructions like:
- What base image to use
- What files to copy
- What commands to run
- What to execute when container starts

### Step 2.1: Create a Simple Python App

```bash
# Create project directory
mkdir -p ~/learn-docker/simple-app
cd ~/learn-docker/simple-app
```

**Create `app.py`:**
```python
# app.py
import time
from datetime import datetime

print("🚀 Python app started!")

count = 0
while True:
    count += 1
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] Running... count={count}")
    time.sleep(5)
```

This simple app just prints a counter every 5 seconds.

### Step 2.2: Create Your First Dockerfile

**Create `Dockerfile`:**
```dockerfile
# Dockerfile
# Start from Python base image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy your code into the container
COPY app.py .

# What to run when container starts
CMD ["python", "app.py"]
```

**Line-by-line explanation:**
- `FROM python:3.11-slim` - Start with a Python image (already has Python installed)
- `WORKDIR /app` - Create and navigate to /app directory
- `COPY app.py .` - Copy app.py from your computer into container's /app
- `CMD ["python", "app.py"]` - Run this command when container starts

### Step 2.3: Build Your Image

```bash
# Build the image
docker build -t my-python-app .

# Explanation:
# build          = Build an image
# -t my-python-app = Tag (name) the image
# .              = Use Dockerfile in current directory
```

**Expected output:**
```
[+] Building 8.2s (8/8) FINISHED
 => [internal] load build definition from Dockerfile
 => [internal] load metadata for docker.io/library/python:3.11-slim
 => [1/2] FROM docker.io/library/python:3.11-slim
 => [2/2] COPY app.py .
 => exporting to image
 => => naming to docker.io/library/my-python-app
```

### Step 2.4: Run Your Custom Image

```bash
# Run your app
docker run --name my-app my-python-app

# You'll see:
# 🚀 Python app started!
# [15:30:45] Running... count=1
# [15:30:50] Running... count=2
# ...

# Press Ctrl+C to stop
```

### Step 2.5: Run in Background

```bash
# Remove old container
docker rm my-app

# Run in background
docker run -d --name my-app my-python-app

# Check logs
docker logs -f my-app

# Stop it
docker stop my-app
docker rm my-app
```

### 🎯 Checkpoint 2 Quiz

**Q1**: What does `FROM` instruction do?
<details>
<summary>Answer</summary>
Specifies the base image to start from (like inheriting from a parent class)
</details>

**Q2**: What's the difference between `COPY` and `CMD`?
<details>
<summary>Answer</summary>
`COPY` runs during BUILD (creates image), `CMD` runs when STARTING container
</details>

---

## Part 3: Docker Networks - Connect Containers

### The Problem

Containers are isolated by default. If you have:
- Container A (Python app)
- Container B (Redis database)

**Container A cannot talk to Container B** without a network!

### Step 3.1: Create a Network

```bash
# Create a custom network
docker network create my-network

# List networks
docker network ls

# You'll see:
# NETWORK ID     NAME         DRIVER    SCOPE
# ...
# abc123def456   my-network   bridge    local
```

### Step 3.2: Run Containers on the Same Network

```bash
# Start Redis on the network
docker run -d \
  --name my-redis \
  --network my-network \
  redis:7-alpine

# Start another Redis CLI container to test connection
docker run -it \
  --network my-network \
  --rm \
  redis:7-alpine redis-cli -h my-redis

# You're now connected! Try:
# my-redis:6379> PING
# PONG
# my-redis:6379> exit
```

**What happened?**
- Both containers are on `my-network`
- Docker provides **DNS resolution**
- `my-redis` hostname resolves to Redis container's IP
- Magic! Just like `localhost` but for containers

### Step 3.3: Create a Python App that Connects to Redis

**Update `app.py`:**
```python
# app.py
import redis
import time
from datetime import datetime

print("🚀 Connecting to Redis...")

# Connect to Redis by hostname
r = redis.Redis(host='my-redis', port=6379, decode_responses=True)

print("✅ Connected to Redis!")

count = 0
while True:
    count += 1
    now = datetime.now().strftime("%H:%M:%S")

    # Store in Redis
    r.set('count', count)
    r.set('last_update', now)

    # Read from Redis
    stored_count = r.get('count')
    stored_time = r.get('last_update')

    print(f"[{now}] Count={stored_count} (stored at {stored_time})")
    time.sleep(5)
```

**Create `requirements.txt`:**
```
redis==5.0.1
```

**Update `Dockerfile`:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app.py .

CMD ["python", "app.py"]
```

### Step 3.4: Build and Run

```bash
# Rebuild image (it now includes redis library)
docker build -t my-python-app .

# Run on the same network as Redis
docker run -d \
  --name my-app \
  --network my-network \
  my-python-app

# Check logs
docker logs -f my-app

# You'll see:
# 🚀 Connecting to Redis...
# ✅ Connected to Redis!
# [15:45:30] Count=1 (stored at 15:45:30)
# [15:45:35] Count=2 (stored at 15:45:35)
```

### Step 3.5: Verify Data in Redis

```bash
# Connect to Redis
docker exec -it my-redis redis-cli

# Check the data
127.0.0.1:6379> GET count
"5"
127.0.0.1:6379> GET last_update
"15:46:00"
127.0.0.1:6379> exit
```

**Your Python app is talking to Redis! 🎉**

### Step 3.6: Clean Up

```bash
docker stop my-app my-redis
docker rm my-app my-redis
docker network rm my-network
```

### 🎯 Checkpoint 3 Quiz

**Q1**: Why do we need Docker networks?
<details>
<summary>Answer</summary>
To allow containers to communicate with each other. By default, containers are isolated.
</details>

**Q2**: How does `my-redis` hostname work?
<details>
<summary>Answer</summary>
Docker provides built-in DNS for containers on the same network. Container names become hostnames.
</details>

---

## Part 4: Docker Compose - Multi-Container Apps

### The Problem

Running multiple `docker run` commands is tedious:
```bash
docker network create my-network
docker run -d --name my-redis --network my-network redis:7-alpine
docker run -d --name my-app --network my-network my-python-app
```

**Solution**: Docker Compose!

### What is Docker Compose?

A tool to define and run **multi-container applications** using a YAML file.

### Step 4.1: Create docker-compose.yml

```yaml
# docker-compose.yml
services:
  # Redis service
  redis:
    image: redis:7-alpine
    container_name: my-redis
    networks:
      - my-network

  # Python app service
  app:
    build: .  # Build from Dockerfile in current dir
    container_name: my-app
    depends_on:
      - redis  # Start redis first
    networks:
      - my-network

networks:
  my-network:
    driver: bridge
```

### Step 4.2: Start Everything with One Command

```bash
# Start all services
docker compose up -d

# Expected output:
# [+] Running 3/3
#  ✔ Network simple-app_my-network  Created
#  ✔ Container my-redis             Started
#  ✔ Container my-app               Started
```

### Step 4.3: View Status and Logs

```bash
# See all services
docker compose ps

# View logs
docker compose logs -f

# View logs for specific service
docker compose logs -f app
```

### Step 4.4: Stop Everything

```bash
# Stop all services
docker compose down

# Stop and remove volumes (data)
docker compose down -v
```

### 🎯 Checkpoint 4 Quiz

**Q1**: What's the advantage of Docker Compose?
<details>
<summary>Answer</summary>
One command to start/stop multiple containers. No manual network creation. Easier to manage.
</details>

**Q2**: What does `depends_on` do?
<details>
<summary>Answer</summary>
Ensures Redis starts before the app. Controls startup order.
</details>

---

## Part 5: Build the Complete System

Now let's build a real system: **Orchestrator + Worker + Redis**

### System Architecture

```
┌──────────────┐         ┌──────────┐
│ Orchestrator │────────>│  Redis   │
│  (Flask API) │         │ (Queue)  │
└──────────────┘         └─────┬────┘
                               │
                         ┌─────▼────┐
                         │  Worker  │
                         │ (Python) │
                         └──────────┘
```

**Flow:**
1. Orchestrator receives tasks via HTTP
2. Pushes tasks to Redis queue
3. Worker pulls tasks from Redis
4. Worker processes and stores results

### Step 5.1: Project Structure

```bash
mkdir -p ~/learn-docker/task-system
cd ~/learn-docker/task-system
```

Create this structure:
```
task-system/
├── docker-compose.yml
├── orchestrator/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app.py
└── worker/
    ├── Dockerfile
    ├── requirements.txt
    └── worker.py
```

### Step 5.2: Build the Orchestrator

**File: `orchestrator/requirements.txt`**
```
flask==3.0.0
redis==5.0.1
```

**File: `orchestrator/app.py`**
```python
from flask import Flask, request, jsonify
import redis
import json
import uuid
from datetime import datetime

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379, decode_responses=True)

@app.route('/health')
def health():
    return {"status": "healthy", "service": "orchestrator"}

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    task_id = str(uuid.uuid4())

    task = {
        "task_id": task_id,
        "description": data.get("description"),
        "status": "queued",
        "created_at": datetime.now().isoformat()
    }

    # Store task metadata
    r.hset(f"task:{task_id}", mapping=task)

    # Queue for worker
    r.lpush("work_queue", json.dumps(task))

    print(f"✅ Created task: {task_id}")
    return jsonify(task), 201

@app.route('/tasks/<task_id>')
def get_task(task_id):
    task = r.hgetall(f"task:{task_id}")
    if not task:
        return {"error": "Task not found"}, 404
    return jsonify(task)

if __name__ == '__main__':
    print("🚀 Orchestrator starting...")
    app.run(host='0.0.0.0', port=5000)
```

**File: `orchestrator/Dockerfile`**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

CMD ["python", "app.py"]
```

### Step 5.3: Build the Worker

**File: `worker/requirements.txt`**
```
redis==5.0.1
```

**File: `worker/worker.py`**
```python
import redis
import json
import time

print("🚀 Worker starting...")
r = redis.Redis(host='redis', port=6379, decode_responses=True)
print("✅ Connected to Redis")

while True:
    # Blocking pop from queue (waits for tasks)
    result = r.brpop("work_queue", timeout=1)

    if result:
        queue_name, task_json = result
        task = json.loads(task_json)
        task_id = task['task_id']

        print(f"📋 Processing task: {task_id}")
        print(f"   Description: {task['description']}")

        # Simulate work
        time.sleep(3)

        # Update status
        r.hset(f"task:{task_id}", "status", "completed")

        print(f"✅ Completed task: {task_id}")
```

**File: `worker/Dockerfile`**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY worker.py .

CMD ["python", "worker.py"]
```

### Step 5.4: Create docker-compose.yml

**File: `docker-compose.yml`**
```yaml
services:
  # Redis - message queue
  redis:
    image: redis:7-alpine
    container_name: task-redis
    networks:
      - task-network

  # Orchestrator - API service
  orchestrator:
    build: ./orchestrator
    container_name: task-orchestrator
    ports:
      - "5000:5000"
    depends_on:
      - redis
    networks:
      - task-network

  # Worker - job processor
  worker:
    build: ./worker
    container_name: task-worker
    depends_on:
      - redis
    networks:
      - task-network

networks:
  task-network:
    driver: bridge
```

### Step 5.5: Start the System

```bash
# Build and start all services
docker compose up -d

# Watch logs
docker compose logs -f
```

### Step 5.6: Test the System

**Terminal 1: Watch logs**
```bash
docker compose logs -f
```

**Terminal 2: Create tasks**
```bash
# Create a task
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"description": "Process user data"}'

# Response:
# {
#   "task_id": "abc-123-def",
#   "description": "Process user data",
#   "status": "queued",
#   "created_at": "2024-01-15T10:30:00"
# }

# Check task status
curl http://localhost:5000/tasks/abc-123-def
```

**What you'll see in logs:**
```
orchestrator | ✅ Created task: abc-123-def
worker       | 📋 Processing task: abc-123-def
worker       |    Description: Process user data
worker       | ✅ Completed task: abc-123-def
```

### 🎉 Congratulations!

You've built a complete distributed system with Docker!

---

## Part 6: Docker Best Practices

### 1. Use .dockerignore

Create `.dockerignore` to exclude unnecessary files:
```
# .dockerignore
__pycache__
*.pyc
.git
.env
node_modules
```

### 2. Multi-stage Builds (for smaller images)

```dockerfile
# Build stage
FROM python:3.11 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Runtime stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY app.py .
CMD ["python", "app.py"]
```

### 3. Layer Caching

**Bad** (rebuilds everything on code change):
```dockerfile
COPY . .
RUN pip install -r requirements.txt
```

**Good** (only rebuilds if requirements change):
```dockerfile
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

### 4. Health Checks

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:5000/health || exit 1
```

### 5. Use Specific Tags (not `latest`)

**Bad:**
```dockerfile
FROM python:latest
```

**Good:**
```dockerfile
FROM python:3.11-slim
```

---

## Summary & Next Steps

### What You Learned

✅ **Docker Basics**: Images, containers, lifecycle
✅ **Dockerfiles**: Build custom images
✅ **Networks**: Connect containers
✅ **Docker Compose**: Multi-container orchestration
✅ **Real System**: Built Orchestrator + Worker + Redis

### Your System

```
                    HTTP
                     │
                     ▼
              ┌──────────────┐
              │ Orchestrator │ :5000
              │   (Flask)    │
              └──────┬───────┘
                     │
                ┌────▼────┐
                │  Redis  │ :6379
                │ (Queue) │
                └────┬────┘
                     │
              ┌──────▼───────┐
              │    Worker    │
              │   (Python)   │
              └──────────────┘
```

### Docker Commands Cheat Sheet

```bash
# Images
docker build -t myapp .          # Build image
docker images                    # List images
docker rmi myapp                 # Remove image

# Containers
docker run -d --name app myapp   # Run container
docker ps                        # List running
docker ps -a                     # List all
docker stop app                  # Stop container
docker rm app                    # Remove container
docker logs -f app               # View logs
docker exec -it app bash         # Enter container

# Networks
docker network create mynet      # Create network
docker network ls                # List networks

# Docker Compose
docker compose up -d             # Start services
docker compose down              # Stop services
docker compose logs -f           # View logs
docker compose ps                # List services
docker compose restart worker    # Restart service
```

---

## Next: Kubernetes Migration

In the next checkpoint, you'll take this **exact same system** and migrate it to Kubernetes!

**What you'll learn:**
- Pods (like containers)
- Deployments (manage replicas)
- Services (like Docker networks)
- ConfigMaps & Secrets
- Scaling & rolling updates

**The transition will be smooth** because you understand Docker networking and multi-container apps!

---

## 🎯 Final Quiz

**Q1**: What's the Docker equivalent of Kubernetes?
<details>
<summary>Answer</summary>
- Docker Container ≈ Kubernetes Pod
- Docker Compose ≈ Kubernetes Deployment
- Docker Network ≈ Kubernetes Service
</details>

**Q2**: Why is our architecture good for Kubernetes?
<details>
<summary>Answer</summary>
3 independent services that communicate via network = perfect for K8s microservices
</details>

**Q3**: What would you change to scale workers to 5 instances?
<details>
<summary>Answer</summary>
Docker Compose: `docker compose up -d --scale worker=5`
Kubernetes: `kubectl scale deployment worker --replicas=5`
</details>

---

**Ready for Kubernetes?** Continue to **Checkpoint 01: Kubernetes Basics** where you'll deploy this same system to a K8s cluster!
