# Checkpoint 1: Docker Containers - Overview

## 🎯 Learning Objectives

By the end of this checkpoint, you will:

✅ Understand **why containers exist** and what problems they solve
✅ Build **5 Docker images** for your AI Agent system (Python, Go, TypeScript)
✅ Create **Dockerfiles** for each microservice
✅ Run containers locally and test inter-service communication
✅ Use **docker-compose** to orchestrate all services together
✅ See how local Docker setup maps to Kubernetes concepts

**Time Estimate:** 90-120 minutes

---

## 📖 Why Start with Docker?

Before we deploy to Kubernetes, we need to understand **containers** - the foundation of everything in K8s.

### The Problem Containers Solve

**Scenario:** You write a Python app on your Mac. It works perfectly!

```bash
# On your Mac
python app.py  # Works! ✅
```

**You deploy to production server:**

```bash
# On production Linux server
python app.py  # Error: ModuleNotFoundError ❌
```

**Why?** Different Python versions, missing dependencies, different OS libraries!

### Containers = Portable Environments

A **container** packages your app + all its dependencies into a single unit that runs the same everywhere.

```
┌─────────────────────────────────────┐
│         Docker Container            │
│                                     │
│  ┌────────────────────────────┐    │
│  │  Your App (app.py)         │    │
│  ├────────────────────────────┤    │
│  │  Dependencies              │    │
│  │  - Python 3.11             │    │
│  │  - FastAPI                 │    │
│  │  - Redis client            │    │
│  ├────────────────────────────┤    │
│  │  OS Libraries              │    │
│  │  - Linux base              │    │
│  └────────────────────────────┘    │
└─────────────────────────────────────┘
```

**Result:** Runs identically on your Mac, AWS, or anywhere!

---

## 🏗️ What We're Building

We'll create **5 microservices** as Docker containers:

| Service | Language | Purpose | Port |
|---------|----------|---------|------|
| **Frontend** | TypeScript/React | Web UI | 3000 |
| **API Gateway** | Go | Route requests | 8080 |
| **Orchestrator** | Python/FastAPI | Break tasks into jobs | 8000 |
| **Chat Service** | TypeScript/Node.js | Handle chat with LLM | 3001 |
| **Workers** | Go | Execute tasks from queue | N/A |

**Plus supporting services:**
- Redis (official image)
- PostgreSQL (official image)

---

## 🔄 System Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                         Frontend (React)                      │
│                         Port 3000                            │
└────────────────────────┬─────────────────────────────────────┘
                         │ HTTP
┌────────────────────────▼─────────────────────────────────────┐
│                    API Gateway (Go)                          │
│                         Port 8080                            │
└─────┬──────────────────────────────────────────┬────────────┘
      │ Route /tasks                             │ Route /chat
      │                                          │
┌─────▼──────────────────┐              ┌───────▼─────────────┐
│  Orchestrator (Python) │              │  Chat Service (TS)  │
│     Port 8000          │              │     Port 3001       │
└─────┬──────────────────┘              └─────────────────────┘
      │ Push to queue
      │
┌─────▼──────────────────────────────────────────────────────┐
│                         Redis Queue                         │
│                         Port 6379                          │
└─────┬──────────────────────────────────────────────────────┘
      │ Pop from queue
┌─────▼──────────────────┐
│     Workers (Go)       │              ┌─────────────────────┐
│     Multiple pods      │──────────────│  PostgreSQL         │
└────────────────────────┘   Store      │  Port 5432         │
                             results    └─────────────────────┘
```

---

## 📚 Checkpoint Structure

This checkpoint is broken into 8 sub-documents:

1. **[01_setup.md](01_setup.md)** - Monorepo structure & tooling installation
2. **[02_orchestrator.md](02_orchestrator.md)** - Python/FastAPI service
3. **[03_worker.md](03_worker.md)** - Go worker service
4. **[04_gateway.md](04_gateway.md)** - Go API gateway
5. **[05_chat.md](05_chat.md)** - TypeScript/Node.js chat service
6. **[06_frontend.md](06_frontend.md)** - React frontend
7. **[07_compose.md](07_compose.md)** - Docker Compose orchestration
8. **[08_summary.md](08_summary.md)** - Lessons learned & K8s mapping

---

## 🎓 Key Concepts You'll Learn

As we build, you'll understand:

- **Dockerfile layers** - Why order matters for build speed
- **Multi-stage builds** - How to create smaller images (Go services use this)
- **Environment variables** - How services find each other
- **Docker networking** - How containers communicate
- **docker-compose** - Orchestrating multiple services
- **Health checks** - Ensuring services are ready
- **Volume mounts** - Persisting data

---

## 🚀 Let's Start!

Continue to **[01_setup.md](01_setup.md)** to set up your monorepo structure and install modern tooling.
