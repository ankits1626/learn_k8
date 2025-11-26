# Checkpoint 1.1: Setup Monorepo & Tooling

## 🎯 Goals

By the end of this section:
- ✅ Create monorepo structure for all services
- ✅ Install modern package managers (uv, pnpm)
- ✅ Initialize Git repository
- ✅ Verify Go installation

**Time:** 15 minutes

---

## 🔧 Part 1: Create Monorepo Structure

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

---

## 📦 Part 2: Initialize Git Repository

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
.venv/

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

---

## 🛠️ Part 3: Install Modern Tooling

### Step 3.1: Install `uv` (Python - 100x faster than pip)

**What is uv?** Python package manager written in Rust. Replaces pip, poetry, pyenv, virtualenv in one tool!

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify installation
uv --version
```

**Expected output:** `uv 0.5.x` or higher

**Features:**
- 🚀 100x faster than pip (Rust-based)
- 📦 Built-in virtual environment management
- 🔒 Lockfile for reproducible builds (uv.lock)
- 🎯 Drop-in replacement for pip/poetry/pyenv

### Step 3.2: Install `pnpm` (Node.js - 3-4x faster than npm)

**What is pnpm?** Fast, disk-efficient package manager using symlinks to a global store.

```bash
# Install pnpm
curl -fsSL https://get.pnpm.io/install.sh | sh -

# Verify installation
pnpm --version
```

**Expected output:** `9.x.x` or higher

**Why pnpm over npm/yarn/bun?**
- ⚡ 3-4x faster than npm
- 💾 70% less disk space (shared global store)
- 🏢 Excellent monorepo support
- 🔒 Strict dependency resolution (no phantom dependencies)
- 🏭 Production-stable (unlike Bun)

### Step 3.3: Verify Go Installation

Go already has excellent built-in dependency management (go modules).

```bash
go version
```

**Expected:** `go1.21` or higher (from Checkpoint 0)

---

## ✅ Verification Checklist

Before proceeding, verify:

- [ ] Monorepo structure created (`agent-system/services/`)
- [ ] Git repository initialized
- [ ] uv installed and working (`uv --version`)
- [ ] pnpm installed and working (`pnpm --version`)
- [ ] Go installed and working (`go version`)

---

## 🚀 Next Steps

Continue to **[02_orchestrator.md](02_orchestrator.md)** to build the Orchestrator service (Python/FastAPI).
