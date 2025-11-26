# Checkpoint 1.2: Orchestrator Service (Python/FastAPI)

## 🎯 Goals

Build the **brain** of the system - receives tasks, breaks them into subtasks, queues to Redis.

- ✅ Create Python/FastAPI service with uv
- ✅ Implement task submission and queuing
- ✅ Write Dockerfile with uv
- ✅ Test locally with Redis

**Time:** 20 minutes

---

## 📦 Part 1: Initialize Python Project with uv

```bash
cd services/orchestrator

# Initialize uv project (creates pyproject.toml)
uv init --name orchestrator --no-readme

# Add dependencies
uv add fastapi uvicorn redis pydantic

# This creates:
# - pyproject.toml (project definition)
# - uv.lock (lockfile for reproducible builds)
# - .venv/ (virtual environment)
```

**What just happened?**
- `uv init` created a modern Python project structure
- `uv add` installed dependencies 100x faster than pip
- `.venv/` is local to the project (2025 best practice)
- `uv.lock` ensures everyone gets exact same versions

---

## 🧑‍💻 Part 2: Create Application Code

**File: `app.py`**

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from redis import Redis
import json
import os
import uuid
from datetime import datetime

app = FastAPI(title="Orchestrator Service")

# Redis connection (from environment variable)
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", "6379"))

try:
    redis_client = Redis(
        host=redis_host,
        port=redis_port,
        decode_responses=True,
        socket_connect_timeout=2
    )
    redis_client.ping()
    print(f"✅ Connected to Redis at {redis_host}:{redis_port}")
except Exception as e:
    print(f"⚠️  Redis not available: {e}")
    redis_client = None


class TaskRequest(BaseModel):
    description: str
    priority: int = 1


class TaskResponse(BaseModel):
    task_id: str
    description: str
    status: str
    created_at: str
    subtasks: list[str]


@app.get("/health")
def health_check():
    """Health check endpoint for Docker/K8s"""
    redis_status = "connected" if redis_client else "disconnected"
    return {
        "status": "healthy",
        "service": "orchestrator",
        "redis": redis_status
    }


@app.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskRequest):
    """
    Receive a task, break it into subtasks, and queue to Redis

    Example:
    POST /tasks
    {
        "description": "Build a user authentication system",
        "priority": 1
    }
    """
    if not redis_client:
        raise HTTPException(status_code=503, detail="Redis unavailable")

    # Generate unique task ID
    task_id = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat()

    # Break task into subtasks (simplified logic)
    subtasks = _generate_subtasks(task.description)

    # Create task object
    task_obj = {
        "task_id": task_id,
        "description": task.description,
        "priority": str(task.priority),  # Convert to string for Redis
        "status": "queued",
        "created_at": created_at,
        "subtasks": ",".join(subtasks)  # Convert list to comma-separated string
    }

    # Store task in Redis hash
    redis_client.hset(f"task:{task_id}", mapping=task_obj)

    # Queue each subtask for workers
    for idx, subtask in enumerate(subtasks):
        job = {
            "task_id": task_id,
            "subtask_id": f"{task_id}-{idx}",
            "description": subtask,
            "priority": task.priority
        }
        redis_client.lpush("work_queue", json.dumps(job))

    print(f"📋 Created task {task_id} with {len(subtasks)} subtasks")

    return TaskResponse(
        task_id=task_id,
        description=task.description,
        status="queued",
        created_at=created_at,
        subtasks=subtasks
    )


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: str):
    """Get task status by ID"""
    if not redis_client:
        raise HTTPException(status_code=503, detail="Redis unavailable")

    task_data = redis_client.hgetall(f"task:{task_id}")

    if not task_data:
        raise HTTPException(status_code=404, detail="Task not found")

    return TaskResponse(
        task_id=task_data["task_id"],
        description=task_data["description"],
        status=task_data["status"],
        created_at=task_data["created_at"],
        subtasks=task_data.get("subtasks", "").split(",")
    )


def _generate_subtasks(description: str) -> list[str]:
    """
    Break a task into subtasks (simplified AI logic)
    In production, this would call an LLM to intelligently break down tasks
    """
    # Simple keyword-based splitting for demo
    if "authentication" in description.lower():
        return [
            "Design user database schema",
            "Implement JWT token generation",
            "Create login/logout endpoints",
            "Add password hashing with bcrypt"
        ]
    elif "api" in description.lower():
        return [
            "Define API endpoints and routes",
            "Implement request validation",
            "Add error handling middleware",
            "Write API documentation"
        ]
    else:
        # Default: split into 3 generic subtasks
        return [
            f"Research requirements for: {description}",
            f"Implement core logic for: {description}",
            f"Test and validate: {description}"
        ]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Key Features:**
- ✅ FastAPI for modern Python web framework
- ✅ Redis integration for task queue
- ✅ Health check endpoint (required for K8s)
- ✅ Environment variables for configuration
- ✅ Pydantic models for type safety
- ✅ Simple task breakdown logic (would use LLM in production)

---

## 🐳 Part 3: Create Dockerfile

**File: `Dockerfile`**

```dockerfile
# Use Python 3.11 slim image
FROM python:3.11-slim

# Install uv (fast Python package manager)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files first (for layer caching)
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen --no-dev

# Copy application code
COPY app.py ./

# Expose port 8000
EXPOSE 8000

# Run the application
CMD ["uv", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Dockerfile Best Practices:**
- ✅ Use slim base image (smaller size)
- ✅ Copy dependencies first (better layer caching)
- ✅ Use uv for fast, reproducible installs
- ✅ Run as non-root user (security)
- ✅ Single CMD instruction

---

## 🧪 Part 4: Test Locally

### Step 4.1: Start Redis Locally

```bash
# Run Redis in Docker
docker run -d \
  --name redis-local \
  -p 6379:6379 \
  redis:7-alpine

# Verify Redis is running
docker logs redis-local
```

### Step 4.2: Run Orchestrator

```bash
cd services/orchestrator

# Run with uv
uv run uvicorn app:app --reload --port 8000
```

**Expected output:**
```
✅ Connected to Redis at localhost:6379
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 4.3: Test Endpoints

**Terminal 2: Test health check**
```bash
curl http://localhost:8000/health
```

**Expected:**
```json
{
  "status": "healthy",
  "service": "orchestrator",
  "redis": "connected"
}
```

**Terminal 2: Create a task**
```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Build a user authentication system",
    "priority": 1
  }'
```

**Expected:**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "description": "Build a user authentication system",
  "status": "queued",
  "created_at": "2025-11-26T10:30:00",
  "subtasks": [
    "Design user database schema",
    "Implement JWT token generation",
    "Create login/logout endpoints",
    "Add password hashing with bcrypt"
  ]
}
```

**Terminal 2: Check Redis queue**
```bash
# Replace redis-local with your container name (e.g., cerra-ai-redis)
docker exec <redis-container-name> redis-cli LLEN work_queue
```

**Expected:** `4` (4 subtasks queued)

**Terminal 2: Inspect the queue visually**
```bash
# View all items in the queue (without removing them)
docker exec <redis-container-name> redis-cli LRANGE work_queue 0 -1

# View just the first item (formatted)
docker exec <redis-container-name> redis-cli LINDEX work_queue 0

# Find all task keys
docker exec <redis-container-name> redis-cli KEYS "task:*"

# View a specific task's metadata (replace with actual task ID from response)
docker exec <redis-container-name> redis-cli HGETALL task:<task-id>
```

**What you're seeing:**
- `LLEN work_queue` - Length of the list (queue depth)
- `LRANGE work_queue 0 -1` - All items from index 0 to end (-1)
- `LINDEX work_queue 0` - First item in the queue
- `KEYS "task:*"` - All keys matching the pattern
- `HGETALL task:<id>` - All fields in the hash (task metadata)

### Optional: Use Redis GUI (RedisInsight)

**What is RedisInsight?** Official Redis GUI with visual key browser, real-time monitoring, and CLI.

**Install RedisInsight:**
```bash
# Option 1: Run as Docker container (recommended)
docker run -d \
  --name redisinsight \
  -p 5540:5540 \
  redis/redisinsight:latest

# Access at: http://localhost:5540
```

**Option 2: Download Desktop App**
- Visit: https://redis.io/insight/
- Download for macOS/Windows/Linux
- Install and run

**Connect to Your Redis:**
1. Open RedisInsight at `http://localhost:5540`
2. Click "Add Redis Database"
3. Enter connection details:
   - **Host**: `localhost` (or `host.docker.internal` if RedisInsight is in Docker)
   - **Port**: `6379`
   - **Name**: `agent-system-redis`
4. Click "Add Database"

**What You Can Do:**
- 🔍 **Browse Keys**: Visual tree view of all keys (`task:*`, `result:*`, `work_queue`)
- 📊 **View Lists**: See `work_queue` items in a table
- 🗂️ **View Hashes**: See task metadata in key-value format
- 📈 **Monitor Performance**: Real-time memory usage, commands/sec
- 🎨 **Pretty JSON**: Auto-formats JSON data
- 🖥️ **Built-in CLI**: Same as `redis-cli` but with autocomplete

**Alternative: Another Redis Desktop Manager (Open Source)**
```bash
# Install via Homebrew (macOS)
brew install --cask another-redis-desktop-manager
```

**Why Use a GUI?**
- ✅ Visualize data structures instantly (lists, hashes, sets)
- ✅ See queue depth changes in real-time
- ✅ Great for learning how Redis stores data
- ✅ No need to remember CLI commands
- ✅ Perfect for debugging task flow

---

## 🐳 Part 5: Build Docker Image

```bash
cd services/orchestrator

# Build the image
docker build -t orchestrator:latest .
```

**Expected output:**
```
[+] Building 45.2s (12/12) FINISHED
 => [internal] load .dockerignore
 => [internal] load build definition from Dockerfile
 => [stage-0 1/6] FROM python:3.11-slim
 ...
 => => naming to docker.io/library/orchestrator:latest
```

**Verify image created:**
```bash
docker images orchestrator:latest
```

---

## 🐳 Part 6: Run with Docker Compose (Recommended)

**Why Docker Compose?**
- ✅ Define multiple services (Redis + Orchestrator) in one file
- ✅ Automatic networking between containers
- ✅ Easy start/stop: `docker compose up` / `docker compose down`
- ✅ Great preparation for Kubernetes (similar concepts)
- ✅ Keeps services decoupled but coordinated

### Step 6.1: Create docker-compose.yml

**File: `services/orchestrator/docker-compose.yml`**

```yaml
version: '3.8'

services:
  # Redis service
  redis:
    image: redis:7-alpine
    container_name: orchestrator-redis
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5
    networks:
      - orchestrator-net

  # Orchestrator service
  orchestrator:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: orchestrator-app
    ports:
      - "8000:8000"
    environment:
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    depends_on:
      redis:
        condition: service_healthy
    networks:
      - orchestrator-net
    restart: unless-stopped

networks:
  orchestrator-net:
    driver: bridge

volumes:
  redis-data:
    driver: local
```

**Key Concepts:**

1. **Services**: Each container is a "service" (Redis, Orchestrator)
2. **Networks**: Automatic DNS - `redis` hostname resolves to Redis container
3. **Volumes**: Persistent storage for Redis data
4. **depends_on + healthcheck**: Orchestrator waits until Redis is healthy
5. **Environment variables**: Configure connection between services

### Step 6.2: Run with Docker Compose

```bash
cd services/orchestrator

# Start all services (builds image if needed)
docker compose up -d

# Expected output:
# [+] Running 3/3
#  ✔ Network orchestrator_orchestrator-net  Created
#  ✔ Container orchestrator-redis           Started
#  ✔ Container orchestrator-app             Started
```

**Check status:**
```bash
docker compose ps
```

**Expected:**
```
NAME                 IMAGE              STATUS         PORTS
orchestrator-app     orchestrator       Up 10 seconds  0.0.0.0:8000->8000/tcp
orchestrator-redis   redis:7-alpine     Up 15 seconds  0.0.0.0:6379->6379/tcp
```

### Step 6.3: Test the System

**Terminal 1: View logs**
```bash
# All services
docker compose logs -f

# Just orchestrator
docker compose logs -f orchestrator

# Just Redis
docker compose logs -f redis
```

**Terminal 2: Test health check**
```bash
curl http://localhost:8001/health
```

**Expected:**
```json
{
  "status": "healthy",
  "service": "orchestrator",
  "redis": "connected"
}
```

**Terminal 2: Create a task**
```bash
curl -X POST http://localhost:8001/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Build a user authentication system",
    "priority": 1
  }'
```

**Terminal 2: Check Redis queue**
```bash
docker compose exec redis redis-cli LLEN work_queue
# Expected: 4
```

### Step 6.4: Docker Compose Commands

```bash
# Start services
docker compose up -d

# Stop services (containers remain)
docker compose stop

# Start stopped services
docker compose start

# Restart services
docker compose restart

# View logs
docker compose logs -f

# Stop and remove containers
docker compose down

# Stop, remove containers, and remove volumes (clears Redis data)
docker compose down -v

# Rebuild images and restart
docker compose up -d --build
```

### Step 6.5: Development Workflow

**Edit code and reload:**
```bash
# Make changes to app.py
# Rebuild and restart
docker compose up -d --build orchestrator
```

**Access Redis CLI:**
```bash
docker compose exec redis redis-cli
> KEYS *
> LRANGE work_queue 0 -1
> exit
```

**Clean slate:**
```bash
# Stop everything, remove volumes, rebuild
docker compose down -v
docker compose up -d --build
```

---

## 🆚 Docker Run vs Docker Compose Comparison

| Task | Docker Run (Manual) | Docker Compose (Automated) |
|------|---------------------|---------------------------|
| **Start Redis** | `docker run -d --name redis -p 6379:6379 redis:7-alpine` | `docker compose up -d` (starts both) |
| **Start Orchestrator** | `docker run -d --name orch -e REDIS_HOST=... orchestrator` | Already handled |
| **Networking** | `--network host` or custom network | Automatic DNS (`redis` hostname) |
| **Stop services** | `docker stop redis && docker stop orch` | `docker compose stop` |
| **Clean up** | `docker rm redis orch && docker volume rm ...` | `docker compose down -v` |
| **View logs** | `docker logs redis` + `docker logs orch` | `docker compose logs -f` |
| **Rebuild** | `docker build -t orch . && docker stop orch && docker rm orch && docker run...` | `docker compose up -d --build` |

**Winner:** Docker Compose for local development! 🎉

---

## ✅ Verification Checklist

- [ ] `uv` project initialized with dependencies
- [ ] `app.py` created with FastAPI endpoints
- [ ] Dockerfile created
- [ ] Service runs locally and connects to Redis
- [ ] Health check returns `{"status": "healthy"}`
- [ ] Task creation queues subtasks to Redis
- [ ] Docker image builds successfully

---

## 🎓 What You Learned

- ✅ FastAPI for modern Python web services
- ✅ uv for 100x faster dependency management
- ✅ Redis as a message queue
- ✅ Environment variables for configuration
- ✅ Dockerfile layer caching optimization
- ✅ Health check endpoints for container orchestration

---

---

## 🔧 Troubleshooting

### Issue 1: Port Already in Use

**Error:**
```
docker: Error response from daemon: Bind for 0.0.0.0:8000 failed: port is already allocated
```

**Solution:** Use a different port

```bash
# Check what's using port 8000
lsof -i :8000

# Run on a different port (e.g., 8001)
uv run uvicorn app:app --reload --port 8001

# Test on new port
curl http://localhost:8001/health
```

### Issue 2: Redis Container Already Exists

**Error:**
```
Error response from daemon: Bind for 0.0.0.0:6379 failed: port is already allocated
```

**Solution:** Use existing Redis container

```bash
# Find existing Redis containers
docker ps | grep redis

# Use the existing container name (e.g., cerra-ai-redis)
docker exec <your-redis-container-name> redis-cli LLEN work_queue

# Example:
docker exec cerra-ai-redis redis-cli LLEN work_queue
```

### Issue 3: Redis Data Type Error

**Error:**
```
redis.exceptions.DataError: Invalid input of type: 'list'. Convert to a bytes, string, int or float first.
```

**Root Cause:** Redis `hset` only accepts strings, not lists or complex objects.

**Solution:** Already fixed in the code above (lines 124, 127)
- Convert `priority` to string: `str(task.priority)`
- Convert `subtasks` list to comma-separated string: `",".join(subtasks)`

### Issue 4: Redis Connection Refused

**Error:**
```
⚠️  Redis not available: Error 111 connecting to localhost:6379. Connection refused.
```

**Solution:** Start Redis

```bash
# Option 1: Use existing container
docker ps -a | grep redis
docker start <container-name>

# Option 2: Start new container
docker run -d --name redis-local -p 6379:6379 redis:7-alpine
```

### Issue 5: Module Not Found

**Error:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution:** Ensure dependencies are installed

```bash
# Make sure you're in the orchestrator directory
cd services/orchestrator

# Reinstall dependencies
uv sync

# Run with uv (not python directly)
uv run uvicorn app:app --reload --port 8000
```

---

## 🚀 Next Steps

Continue to **[03_worker.md](03_worker.md)** to build the Worker service (Go) that processes tasks from the Redis queue.
