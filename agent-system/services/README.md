# Agent System - 3-Service Architecture

This project is structured with **3 independent services** that communicate via a shared Docker network. This architecture mirrors how services work in Kubernetes.

## Architecture Overview

```
┌──────────────────────────────────────────────────────┐
│              agent-system-net (Docker Network)       │
│                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────┐ │
│  │    Redis     │  │ Orchestrator │  │  Worker   │ │
│  │ agent-redis  │  │   (FastAPI)  │  │   (Go)    │ │
│  │   :6379      │  │   :8000      │  │           │ │
│  └──────┬───────┘  └──────┬───────┘  └─────┬─────┘ │
│         │                 │                 │       │
│         └─────────────────┴─────────────────┘       │
│                   DNS Resolution                    │
│         (agent-redis resolves to Redis IP)          │
└──────────────────────────────────────────────────────┘
         │                 │
    Port 6380         Port 8001
    (Host)            (Host)
```

## Services

### 1. Redis (`services/redis/`)
- **Purpose**: Message queue and data storage
- **Port**: 6380 (host) → 6379 (container)
- **Container Name**: `agent-redis`
- **DNS Hostname**: `agent-redis` (used by other services)

### 2. Orchestrator (`services/orchestrator/`)
- **Purpose**: REST API for task creation
- **Port**: 8001 (host) → 8000 (container)
- **Container Name**: `agent-orchestrator`
- **Connects to**: `agent-redis:6379`

### 3. Worker (`services/worker/`)
- **Purpose**: Processes jobs from Redis queue
- **Container Name**: `agent-worker`
- **Connects to**: `agent-redis:6379`

## Quick Start

### Step 1: Create Shared Network
```bash
docker network create agent-system-net
```

### Step 2: Start Services (in order)

```bash
# 1. Start Redis first
cd services/redis
docker compose up -d

# 2. Start Orchestrator
cd ../orchestrator
docker compose up -d

# 3. Start Worker
cd ../worker
docker compose up -d
```

### Step 3: Verify All Services Running
```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep agent-
```

**Expected output:**
```
NAMES                 STATUS                    PORTS
agent-worker          Up X seconds
agent-orchestrator    Up X seconds              0.0.0.0:8001->8000/tcp
agent-redis           Up X seconds (healthy)    0.0.0.0:6380->6379/tcp
```

### Step 4: Test the System
```bash
# Create a task
curl -X POST http://localhost:8001/tasks \
  -H "Content-Type: application/json" \
  -d '{"description":"Build a user authentication system","priority":1}'

# Check worker logs
docker logs agent-worker --tail=20
```

## Development Workflow

### View Logs
```bash
# All services at once
docker logs agent-redis -f &
docker logs agent-orchestrator -f &
docker logs agent-worker -f

# Individual service
docker logs -f agent-worker
```

### Restart a Service
```bash
# Restart just the worker (without affecting Redis or Orchestrator)
cd services/worker
docker compose restart

# Or rebuild after code changes
docker compose up -d --build
```

### Stop All Services
```bash
# Stop each service
cd services/worker && docker compose down
cd ../orchestrator && docker compose down
cd ../redis && docker compose down
```

### Clean Slate (Remove All Data)
```bash
# Stop and remove containers + volumes
cd services/worker && docker compose down -v
cd ../orchestrator && docker compose down -v
cd ../redis && docker compose down -v

# Remove network
docker network rm agent-system-net
```

## Service Independence (Key Learning)

Each service can be **deployed, scaled, and restarted independently**:

```bash
# Scale worker to 3 instances
cd services/worker
docker compose up -d --scale worker=3

# Restart orchestrator without affecting worker
cd services/orchestrator
docker compose restart

# Update Redis version without touching app services
cd services/redis
# Edit docker-compose.yml to use redis:7.2-alpine
docker compose up -d
```

This is **exactly how Kubernetes works**!

## Kubernetes Migration Path

This Docker Compose setup maps directly to Kubernetes:

| Docker Compose | Kubernetes |
|----------------|------------|
| `agent-system-net` network | Namespace |
| `agent-redis` container | Pod with Redis container |
| `agent-orchestrator` container | Deployment with 1+ replicas |
| `agent-worker` container | Deployment with 1+ replicas |
| DNS: `agent-redis` | Service: `agent-redis.default.svc.cluster.local` |
| `docker compose up -d` | `kubectl apply -f deployment.yaml` |
| `docker compose scale worker=3` | `kubectl scale deployment worker --replicas=3` |

## Network Communication

Services communicate via **Docker DNS**:

```python
# Orchestrator connects to Redis
REDIS_HOST = "agent-redis"  # Not "localhost"!
```

```go
// Worker connects to Redis
redisHost := "agent-redis"  // DNS resolution
```

Docker automatically resolves `agent-redis` to the Redis container's IP address within the `agent-system-net` network.

## Troubleshooting

### Service Can't Connect to Redis
```bash
# Check if all containers are on the same network
docker network inspect agent-system-net

# Should show: agent-redis, agent-orchestrator, agent-worker
```

### Port Already in Use
```bash
# Check what's using the port
lsof -i :6380
lsof -i :8001

# Change port in docker-compose.yml if needed
```

### Redis Connection Refused
```bash
# Check Redis is healthy
docker ps --filter name=agent-redis

# Test Redis connectivity from orchestrator
docker exec agent-orchestrator ping -c 2 agent-redis
```

## Live Reload

Both orchestrator and worker have live reload enabled:

- **Orchestrator**: Edit `app.py` → auto-reloads
- **Worker**: Edit `main.go` → Air rebuilds automatically

## Next Steps

- Add more workers: `docker compose up -d --scale worker=5`
- Convert to Kubernetes: `kubectl apply -f k8s/`
- Add monitoring: Prometheus + Grafana
- Add service mesh: Istio

---

**Why This Architecture?**

This 3-service separation teaches you:
1. **Service independence** - Each service has its own lifecycle
2. **Network communication** - Services discover each other via DNS
3. **Kubernetes patterns** - Direct mapping to K8s concepts
4. **Scalability** - Scale workers without touching Redis/Orchestrator
5. **Real-world practices** - How microservices actually work
