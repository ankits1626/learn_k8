# Checkpoint 1: Build Services Locally with Docker

## 🎯 Learning Objectives

By the end of this checkpoint, you will:

✅ Understand **why containers exist** and what problems they solve
✅ Build **5 Docker images** for your AI Agent system (Python, Go, TypeScript)
✅ Create **Dockerfiles** for each microservice
✅ Run containers locally and test inter-service communication
✅ Use **docker-compose** to orchestrate all services together
✅ See how local Docker setup maps to Kubernetes concepts

**Time Estimate:** 60-90 minutes

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

## 🏗️ What We're Building in Checkpoint 1

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

## 🔧 Part 1: Setup Monorepo Structure

Let's organize this as a **monorepo** - all code in one place, easy to version control and share.

### Step 1.1: Create Monorepo Structure

```bash
cd ~/code/learn/learn_k8

# Create the monorepo root
mkdir -p agent-system
cd agent-system

# Service code directories
mkdir -p services/orchestrator
mkdir -p services/worker
mkdir -p services/gateway
mkdir -p services/chat
mkdir -p services/frontend

# Docker Compose for local development
mkdir -p deploy/local

# Kubernetes manifests (for later checkpoints)
mkdir -p deploy/k8s

# Documentation
mkdir -p docs
```

**Verify:**
```bash
tree -L 2 . || find . -type d -maxdepth 2
```

**Expected structure:**
```
agent-system/
├── services/
│   ├── orchestrator/    # Python/FastAPI
│   ├── worker/          # Go
│   ├── gateway/         # Go
│   ├── chat/            # TypeScript/Node.js
│   └── frontend/        # TypeScript/React
├── deploy/
│   ├── local/           # docker-compose.yml
│   └── k8s/             # Kubernetes YAML (later)
└── docs/                # Additional documentation
```

### Step 1.2: Initialize Git (Monorepo Best Practice)

```bash
# Initialize git repository
git init

# Create .gitignore
cat > .gitignore << 'EOF'
# Dependencies
node_modules/
__pycache__/
*.pyc
vendor/

# Build outputs
build/
dist/
*.exe

# IDE
.vscode/
.idea/
*.swp

# Environment
.env
*.local

# OS
.DS_Store
Thumbs.db
EOF

# Initial commit
git add .
git commit -m "Initial monorepo structure"
```

**Why Monorepo?**

- ✅ All services versioned together
- ✅ Easy to see cross-service changes
- ✅ Simplified CI/CD (build all or specific services)
- ✅ Matches industry best practices (Google, Meta, Microsoft use monorepos)
- ✅ Easy for your coach to help debug!

---

## 🛠️ Part 2: Install Modern Tooling

Before we build services, let's install the **fastest** package managers available in 2025.

### Step 2.1: Install `uv` (Python - 100x faster than pip)

**What is uv?** Python package manager written in Rust. Replaces pip, poetry, pyenv, virtualenv in one tool!

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify installation
uv --version
```

**Expected output:** `uv 0.5.x` or higher

### Step 2.2: Install `pnpm` (Node.js - 3-4x faster than npm)

**What is pnpm?** Fast, disk-efficient package manager using symlinks to a global store.

```bash
# Install pnpm
curl -fsSL https://get.pnpm.io/install.sh | sh -

# Verify installation
pnpm --version
```

**Expected output:** `9.x.x` or higher

**Why not Bun?** While Bun is the fastest (7x faster than npm), pnpm offers better stability for production and excellent monorepo support - perfect for our multi-service setup.

### Step 2.3: Verify Go is Ready

Go already has excellent built-in dependency management (go modules).

```bash
go version
```

**Expected:** `go1.21` or higher (from Checkpoint 0)

---

## 📦 Part 3: Build the Orchestrator Service (Python + uv)

The **brain** of our system - receives tasks, breaks them into subtasks, queues to Redis.

### Step 3.1: Initialize Python Project with uv

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

### Step 3.2: Create the Application Code

**File 1: `app.py`** (Main application code - we'll write this together)

Would you like me to show you the complete code for each service, or would you prefer to go step-by-step with explanations?

Let me know and we'll continue building!

---

## 🎓 Key Concepts Preview

As we build, you'll learn:

- **Dockerfile layers** - Why order matters for build speed
- **Multi-stage builds** - How to create smaller images (Go worker will use this)
- **Environment variables** - How services find each other
- **Docker networking** - How containers communicate
- **docker-compose** - Orchestrating multiple services

Ready to start coding? 🚀
