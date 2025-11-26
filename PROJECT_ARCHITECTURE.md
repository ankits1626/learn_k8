# 🤖 Project: Minimalist AI Agent System

## 🎯 Learning Objectives

Build a **realistic multi-service AI agent system** using Kubernetes to learn:
- Multi-language microservices (Python, Go, TypeScript)
- Service-to-service communication
- Message queues for async processing
- Database integration
- Agent orchestration patterns
- All K8s concepts from pods to GitOps

---

## 🏗️ System Architecture

### Overview

A simple agentic system where users can submit tasks through a chat interface. The agent orchestrator breaks tasks into subtasks, queues them to workers, and returns results.

**Think of it as:** A mini AutoGPT/LangChain system running on Kubernetes

---

### Visual Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER BROWSER                              │
│                   http://agent.local                             │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│  Kubernetes Ingress                                              │
│  - Routes /        → Frontend                                    │
│  - Routes /api/*   → API Gateway                                 │
└─────────────┬────────────────────────────────────────────────────┘
              │
              ▼
┌──────────────────────────────────────────────────────────────────┐
│  Frontend Service (TypeScript/React)                             │
│  Port: 3000                                                      │
│  - Simple chat UI                                                │
│  - Task submission form                                          │
│  - Display results                                               │
│  Deployment: 1 pod                                               │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│  API Gateway Service (Go)                                        │
│  Port: 8080                                                      │
│  - Route requests to services                                    │
│  - Simple path-based routing                                     │
│  - No complex logic                                              │
│  Deployment: 1 pod                                               │
└─────────────┬────────────────────────────┬───────────────────────┘
              │                            │
              │                            │
      ┌───────▼──────────┐        ┌───────▼────────────────────────┐
      │                  │        │                                │
      ▼                  ▼        ▼                                ▼
┌──────────────┐  ┌──────────────────────┐  ┌───────────────────────┐
│ Orchestrator │  │   Chat Service       │  │  PostgreSQL           │
│   Service    │  │   (TypeScript)       │  │  - Chat history       │
│ (Python)     │  │   Port: 3001         │  │  - Task results       │
│ Port: 8000   │  │                      │  │  - User sessions      │
│              │  │  - Handle chat msgs  │  │                       │
│ - Break task │  │  - Call LLM API      │  │  StatefulSet: 1 pod   │
│   into steps │  │  - Store in DB       │  │  PersistentVolume     │
│ - Queue jobs │  │                      │  └───────────────────────┘
│              │  │  Deployment: 2 pods  │
│ Deployment:  │  └──────────────────────┘
│  2 pods      │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────────┐
│  Redis Service                                                   │
│  Port: 6379                                                      │
│  - Task queue (List data structure)                             │
│  - Worker coordination                                           │
│  - Job status tracking                                           │
│  StatefulSet: 1 pod                                              │
│  PersistentVolume for data persistence                           │
└─────────────┬────────────────────────────────────────────────────┘
              │
              ▼
┌──────────────────────────────────────────────────────────────────┐
│  Task Worker Service (Go)                                        │
│  - Pull tasks from Redis queue                                  │
│  - Execute simple operations                                     │
│  - Write results to PostgreSQL                                   │
│  Deployment: 3 pods (HPA enabled - scales 2-10)                 │
└──────────────────────────────────────────────────────────────────┘
```

---

## 📦 Services Detailed Breakdown

### 1. Frontend (TypeScript/React)
**File:** `services/frontend/`
**Language:** TypeScript + React
**Lines of Code:** ~150
**Port:** 3000

**Purpose:** Simple web UI for user interaction

**Features:**
- Chat interface (message input + history display)
- Task submission form (title + description)
- Results display area
- Basic styling (Tailwind CSS)

**API Calls:**
- `POST /api/chat` - Send chat message
- `POST /api/task` - Submit task
- `GET /api/tasks/:id` - Get task status

**K8s Resources:**
- Deployment: 1 replica
- Service: ClusterIP
- ConfigMap: API Gateway URL

---

### 2. API Gateway (Go)
**File:** `services/gateway/`
**Language:** Go
**Lines of Code:** ~100
**Port:** 8080

**Purpose:** Route incoming requests to appropriate services

**Routing Logic:**
```
/api/chat      → Chat Service (port 3001)
/api/task      → Orchestrator (port 8000)
/api/tasks/:id → Orchestrator (port 8000)
/health        → Return 200 OK
```

**Code Simplicity:**
- Simple HTTP proxy
- No authentication (learning focus)
- Basic path matching
- Service discovery via K8s DNS

**K8s Resources:**
- Deployment: 1 replica
- Service: ClusterIP
- ConfigMap: Service URLs

**Example Service Discovery:**
```go
// Services are discovered via K8s DNS
chatServiceURL := "http://chat-service.default.svc.cluster.local:3001"
orchestratorURL := "http://orchestrator-service.default.svc.cluster.local:8000"
```

---

### 3. Agent Orchestrator (Python/FastAPI)
**File:** `services/orchestrator/`
**Language:** Python + FastAPI
**Lines of Code:** ~150
**Port:** 8000

**Purpose:** Break user tasks into subtasks and queue them

**Example Task Breakdown:**
```
User Task: "Summarize this article: https://example.com/article"

Orchestrator breaks into:
1. fetch_url → https://example.com/article
2. extract_text → Parse HTML
3. summarize → Call LLM or count words
```

**API Endpoints:**
```
POST /task
  Input: {"title": "...", "description": "...", "user_id": "..."}
  Output: {"task_id": "uuid", "status": "queued"}

GET /task/{task_id}
  Output: {"task_id": "...", "status": "completed", "result": "..."}
```

**Redis Queue Operations:**
```python
# Push subtasks to Redis list
redis.lpush("task_queue", json.dumps({
    "task_id": task_id,
    "subtask_type": "fetch_url",
    "params": {"url": "https://example.com"}
}))
```

**K8s Resources:**
- Deployment: 2 replicas
- Service: ClusterIP
- ConfigMap: Redis URL, PostgreSQL URL
- Secrets: N/A (no sensitive data)

---

### 4. Chat Service (TypeScript/Node.js)
**File:** `services/chat/`
**Language:** TypeScript + Express
**Lines of Code:** ~120
**Port:** 3001

**Purpose:** Handle chat conversations with LLM integration

**Features:**
- Store chat history in PostgreSQL
- Call OpenAI/Claude API (or mock)
- Simple context management (last 5 messages)

**API Endpoints:**
```
POST /chat
  Input: {"user_id": "...", "message": "..."}
  Output: {"response": "...", "chat_id": "..."}

GET /chat/history/{user_id}
  Output: [{"role": "user", "content": "..."}, {...}]
```

**LLM Integration (Simplified):**
```typescript
// Option 1: Real LLM (requires API key)
const response = await openai.chat.completions.create({
  model: "gpt-3.5-turbo",
  messages: chatHistory
});

// Option 2: Mock LLM (for learning without API costs)
const response = `Mock response: I received "${userMessage}"`;
```

**K8s Resources:**
- Deployment: 2 replicas
- Service: ClusterIP
- ConfigMap: PostgreSQL connection string
- Secrets: LLM API key (if using real LLM)

---

### 5. Task Workers (Go)
**File:** `services/worker/`
**Language:** Go
**Lines of Code:** ~80
**Port:** N/A (background service)

**Purpose:** Execute queued tasks from Redis

**Task Types (Simplified):**
```go
type Task struct {
    TaskID      string
    SubtaskType string // "fetch_url", "extract_text", "summarize"
    Params      map[string]string
}
```

**Worker Logic:**
```go
for {
    // 1. Pop task from Redis queue (blocking)
    task := redis.BRPop("task_queue", 0)

    // 2. Execute based on type
    switch task.SubtaskType {
    case "fetch_url":
        result = httpGet(task.Params["url"])
    case "extract_text":
        result = extractTextFromHTML(task.Params["html"])
    case "summarize":
        result = fmt.Sprintf("Summary: %d words", len(strings.Split(text, " ")))
    }

    // 3. Save result to PostgreSQL
    db.Exec("UPDATE tasks SET result = ? WHERE task_id = ?", result, task.TaskID)

    // 4. Update Redis status
    redis.Set(fmt.Sprintf("task:%s:status", task.TaskID), "completed")
}
```

**K8s Resources:**
- Deployment: 3 replicas (initially)
- HPA: Scale 2-10 based on CPU or queue depth
- ConfigMap: Redis URL, PostgreSQL URL
- No Service (workers don't receive requests)

---

### 6. Redis (Message Queue)
**Image:** `redis:7-alpine`
**Lines of Code:** 0 (official image)
**Port:** 6379

**Purpose:** Task queue and coordination

**Data Structures Used:**
```
List: "task_queue" → [task1, task2, task3, ...]
Key: "task:{id}:status" → "pending" | "completed" | "failed"
Key: "task:{id}:result" → JSON result
```

**K8s Resources:**
- StatefulSet: 1 replica
- Service: ClusterIP (redis-service.default.svc.cluster.local)
- PersistentVolumeClaim: 1Gi storage
- ConfigMap: redis.conf (if needed)

---

### 7. PostgreSQL (Database)
**Image:** `postgres:16-alpine`
**Lines of Code:** 0 (official image)
**Port:** 5432

**Purpose:** Persist chat history and task results

**Schema (Simplified):**
```sql
CREATE TABLE chat_messages (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255),
    role VARCHAR(50), -- 'user' or 'assistant'
    content TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE tasks (
    task_id UUID PRIMARY KEY,
    user_id VARCHAR(255),
    title VARCHAR(255),
    description TEXT,
    status VARCHAR(50), -- 'queued', 'processing', 'completed', 'failed'
    result TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

**K8s Resources:**
- StatefulSet: 1 replica
- Service: ClusterIP (postgres-service.default.svc.cluster.local)
- PersistentVolumeClaim: 5Gi storage
- Secret: Database credentials (POSTGRES_PASSWORD)

---

## 🔄 Example User Flow

### Scenario: User Chats and Submits Task

**Step 1: User opens browser**
```
http://agent.local
→ Ingress routes to Frontend (port 3000)
→ React app loads
```

**Step 2: User types in chat**
```
User: "Hello, can you help me summarize an article?"

Frontend → POST /api/chat
→ API Gateway (Go) → routes to Chat Service
→ Chat Service (TypeScript):
  - Stores message in PostgreSQL
  - Calls LLM API (or mock): "Yes, I can help! Please provide the URL."
  - Returns response
→ Frontend displays response
```

**Step 3: User submits task**
```
User clicks: "Submit Task"
Title: "Summarize article"
Description: "https://example.com/article"

Frontend → POST /api/task
→ API Gateway → routes to Orchestrator
→ Orchestrator (Python):
  - Creates task_id (UUID)
  - Breaks into subtasks:
    1. fetch_url
    2. extract_text
    3. summarize
  - Pushes 3 jobs to Redis queue
  - Saves task to PostgreSQL (status: 'queued')
  - Returns: {"task_id": "abc-123", "status": "queued"}
→ Frontend shows: "Task submitted! Processing..."
```

**Step 4: Workers process tasks**
```
Worker Pod 1 (Go):
  - Pops "fetch_url" from Redis
  - Downloads HTML from https://example.com/article
  - Saves to PostgreSQL: tasks.result = "<html>..."
  - Updates Redis: task:abc-123:status = "step1_done"

Worker Pod 2 (Go):
  - Pops "extract_text" from Redis
  - Parses HTML, extracts text
  - Saves to PostgreSQL
  - Updates Redis: task:abc-123:status = "step2_done"

Worker Pod 3 (Go):
  - Pops "summarize" from Redis
  - Counts words or calls LLM
  - Saves final result: "Summary: 342 words about AI..."
  - Updates PostgreSQL: tasks.status = 'completed'
  - Updates Redis: task:abc-123:status = "completed"
```

**Step 5: User sees result**
```
Frontend polls: GET /api/tasks/abc-123 every 2 seconds
→ API Gateway → Orchestrator
→ Orchestrator queries PostgreSQL
→ Returns: {"status": "completed", "result": "Summary: 342 words about AI..."}
→ Frontend displays result in UI
```

---

## 🎓 Kubernetes Concepts Map

### Checkpoint 1: Containers (Docker)
- Build 5 Docker images (Python, Go, TypeScript)
- Run locally with `docker run`
- Test inter-container communication with `docker network`

### Checkpoint 2: Pods
- Deploy each service as a Pod
- See how pods get IPs
- Use `kubectl port-forward` to access

### Checkpoint 3: Deployments
- Convert Pods to Deployments
- Scale workers to 3 replicas
- Delete a worker pod, watch it recreate (self-healing)
- Update orchestrator to v2 (rolling update)

### Checkpoint 4: Services
- Create ClusterIP services for each component
- Test DNS: `curl http://chat-service.default.svc.cluster.local:3001/health`
- See load balancing across worker pods

### Checkpoint 5: ConfigMaps & Secrets
- ConfigMap: Store service URLs, Redis/Postgres connection strings
- Secret: Store LLM API key, PostgreSQL password
- Inject as environment variables

### Checkpoint 6: Ingress
- Single entry point: `http://agent.local`
- Path routing:
  - `/` → Frontend
  - `/api/*` → API Gateway
- Configure `/etc/hosts` for local DNS

### Checkpoint 7: Namespaces
- Create `dev` and `prod` namespaces
- Deploy same system to both
- Test cross-namespace communication
- Resource quotas (limit dev to 2GB RAM)

### Checkpoint 8: StatefulSets & Volumes
- Convert Redis and PostgreSQL to StatefulSets
- Add PersistentVolumeClaims
- Delete pod, verify data persists

### Checkpoint 9: Auto-Scaling (HPA)
- Set resource requests/limits on workers
- Create HPA: scale workers 2-10 based on CPU
- Generate load (submit 100 tasks)
- Watch workers scale up, then down

### Checkpoint 10: Helm Charts
- Package entire system as Helm chart
- values.yaml for customization:
  ```yaml
  orchestrator:
    replicas: 2
    image: orchestrator:v1
  workers:
    replicas: 3
    image: worker:v1
  llm:
    provider: "mock" # or "openai"
    apiKey: ""
  ```
- Deploy with: `helm install agent-system ./chart`
- Create dev-values.yaml and prod-values.yaml

### Checkpoint 11: GitOps with ArgoCD
- Push Helm chart to Git repo
- Install ArgoCD
- Create ArgoCD Application pointing to repo
- Change worker replicas in Git → watch auto-deploy
- Experience self-healing (manual change reverted)

### Checkpoint 12: Production Simulation
- Map to AWS EKS:
  - Minikube → EKS cluster
  - Local images → ECR
  - Local volumes → EBS/S3
  - Ingress → ALB
  - Secrets → AWS Secrets Manager
- Compare `kubectl` commands (identical!)
- Understand what changes (infrastructure) vs what stays same (K8s concepts)

---

## 🧩 Why This Architecture is Perfect for Learning

### Multi-Language Stack
- **Python** - Common for AI/ML services, FastAPI is production-ready
- **Go** - High-performance, used for gateways/workers (like K8s itself!)
- **TypeScript** - Frontend + backend, industry standard

### Real-World Patterns
- **API Gateway** - Single entry point (like AWS API Gateway)
- **Message Queue** - Async processing (like SQS, RabbitMQ)
- **Agent Orchestrator** - Task decomposition (like LangChain, AutoGPT)
- **Worker Pool** - Scalable task execution (like Celery, Temporal)
- **Stateful Services** - Database persistence patterns

### Keeps Code Simple
- Each service < 150 lines of actual code
- Workers do trivial tasks (HTTP GET, text parsing, word count)
- No complex AI logic - focus on architecture
- Optional real LLM (can use mock responses)

### Maps to Rewardz Production
| This System | Rewardz/Production Equivalent |
|-------------|------------------------------|
| API Gateway | AWS API Gateway / ALB |
| Orchestrator | Auto-approver processing logic |
| Redis Queue | AWS SQS / EventBridge |
| Workers | Background job processors |
| PostgreSQL | AWS RDS PostgreSQL |
| Chat Service | Backend API services |
| Frontend | React dashboards |
| ConfigMaps | AWS Systems Manager Parameter Store |
| Secrets | AWS Secrets Manager |
| Helm Charts | Deployment automation |
| ArgoCD | GitOps continuous deployment |

---

## 📊 Service Communication Matrix

| From Service | To Service | Protocol | Purpose |
|--------------|-----------|----------|---------|
| Browser | Ingress | HTTP | User access |
| Ingress | Frontend | HTTP | Serve UI |
| Ingress | API Gateway | HTTP | API requests |
| Frontend | API Gateway | HTTP | Chat/task submission |
| API Gateway | Chat Service | HTTP | Route chat messages |
| API Gateway | Orchestrator | HTTP | Route tasks |
| Chat Service | PostgreSQL | TCP/5432 | Store chat history |
| Chat Service | OpenAI/Claude | HTTPS | LLM API calls |
| Orchestrator | Redis | TCP/6379 | Queue tasks |
| Orchestrator | PostgreSQL | TCP/5432 | Store task metadata |
| Workers | Redis | TCP/6379 | Pop tasks from queue |
| Workers | PostgreSQL | TCP/5432 | Save results |

---

## 🎯 Success Criteria

By the end of this project, you will:

✅ Understand **why Kubernetes exists** (managing multi-service systems)
✅ Write **YAML manifests** for Pods, Deployments, Services, etc.
✅ Use **kubectl** commands fluently
✅ Understand **service discovery** via DNS
✅ Manage **configuration** with ConfigMaps and Secrets
✅ Implement **persistent storage** with StatefulSets
✅ Configure **external access** with Ingress
✅ Achieve **auto-scaling** with HPA
✅ Package applications with **Helm**
✅ Implement **GitOps** with ArgoCD
✅ Map local setup to **AWS EKS production**
✅ Debug issues with `kubectl logs`, `describe`, k9s
✅ Build a **realistic multi-language microservices system**

---

## 🌟 2025 Best Practices & Modern Patterns

This architecture incorporates cutting-edge Kubernetes and cloud-native patterns from 2025. Here's what makes it production-ready and forward-thinking:

### 1. **Gateway API (Replacing Ingress)**

**What:** Gateway API is the modern successor to Ingress, reaching v1.0 in 2023 and becoming the standard in 2025.

**Why It Matters:**
- Ingress NGINX officially retired in November 2025
- Gateway API supports both L4 (TCP/UDP) and L7 (HTTP/gRPC) protocols
- Role-based resources (GatewayClass, Gateway, HTTPRoute)
- Built-in support for canary deployments and traffic splitting
- No more annotation hell - capabilities are in the spec!

**In Our Project:**
```yaml
# Checkpoint 6: We'll use Gateway API instead of traditional Ingress
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: agent-system-routes
spec:
  parentRefs:
  - name: agent-gateway
  rules:
  - matches:
    - path:
        type: PathPrefix
        value: /api
    backendRefs:
    - name: api-gateway-service
      port: 8080
  - matches:
    - path:
        type: PathPrefix
        value: /
    backendRefs:
    - name: frontend-service
      port: 3000
```

**Learning Checkpoint:** Checkpoint 6 (External Access)

---

### 2. **KEDA for Event-Driven Autoscaling**

**What:** Kubernetes Event-Driven Autoscaling - scales pods based on event sources (queues, streams, metrics), not just CPU/memory.

**Why It Matters:**
- CNCF Graduated project (August 2023)
- 70+ built-in scalers (Redis, Kafka, PostgreSQL, Prometheus, etc.)
- Scale to zero capability - save costs when idle
- Perfect for AI/Agent workloads with bursty patterns

**In Our Project:**
```yaml
# Checkpoint 9: Scale workers based on Redis queue depth
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: worker-scaler
spec:
  scaleTargetRef:
    name: task-worker-deployment
  minReplicaCount: 2
  maxReplicaCount: 10
  triggers:
  - type: redis
    metadata:
      address: redis-service.default.svc.cluster.local:6379
      listName: task_queue
      listLength: "5"  # Scale up if queue > 5 items per pod
```

**Benefits:**
- Workers scale based on **actual work** (queue depth), not CPU
- Idle system scales to 2 pods, busy system scales to 10
- More efficient than traditional HPA

**Learning Checkpoint:** Checkpoint 9 (Auto-Scaling)

---

### 3. **OpenTelemetry for Observability**

**What:** Unified observability standard for metrics, logs, and traces - the backbone of 2025 observability.

**Why It Matters:**
- Industry-standard way to instrument applications
- Vendor-neutral (works with Prometheus, Grafana, Jaeger, New Relic, etc.)
- Auto-instrumentation via Kubernetes Operator
- Critical for debugging distributed AI agent systems

**In Our Project:**
```yaml
# Checkpoint 11: Add OpenTelemetry auto-instrumentation
apiVersion: opentelemetry.io/v1alpha1
kind: Instrumentation
metadata:
  name: agent-system-instrumentation
spec:
  exporter:
    endpoint: http://otel-collector:4317
  propagators:
    - tracecontext
    - baggage
  sampler:
    type: parentbased_traceidratio
    argument: "1.0"
  python:
    image: ghcr.io/open-telemetry/opentelemetry-operator/autoinstrumentation-python:latest
  nodejs:
    image: ghcr.io/open-telemetry/opentelemetry-operator/autoinstrumentation-nodejs:latest
  go:
    image: ghcr.io/open-telemetry/opentelemetry-operator/autoinstrumentation-go:latest
```

**What You'll See:**
- Trace a request from Browser → Frontend → API Gateway → Chat Service → LLM API
- See exact latency at each hop
- Identify bottlenecks visually
- Track token usage and costs per request

**Learning Checkpoint:** Checkpoint 11 (Production Observability)

---

### 4. **Argo Rollouts for Progressive Delivery**

**What:** Advanced deployment strategies (canary, blue-green) with automated rollback based on metrics.

**Why It Matters:**
- Progressive delivery is the 2025 standard (not just "deploy and hope")
- Automated rollback if error rate increases
- Gradual traffic shifting (10% → 50% → 100%)
- Essential for AI systems where changes can be unpredictable

**In Our Project:**
```yaml
# Checkpoint 11: Progressive delivery for orchestrator updates
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: orchestrator-rollout
spec:
  replicas: 2
  strategy:
    canary:
      steps:
      - setWeight: 20  # Send 20% traffic to new version
      - pause: {duration: 2m}
      - setWeight: 50
      - pause: {duration: 2m}
      - setWeight: 100
      analysis:
        templates:
        - templateName: error-rate-check
        startingStep: 1
  template:
    spec:
      containers:
      - name: orchestrator
        image: orchestrator:v2
```

**Real-World Scenario:**
- Deploy orchestrator v2 with new AI logic
- 20% of requests go to v2
- If error rate spikes → automatic rollback
- If metrics good → gradually increase to 100%

**Learning Checkpoint:** Checkpoint 11 (Advanced Deployments)

---

### 5. **Security Best Practices (2025 Standard)**

**Zero Trust Architecture:**
- Network policies: Deny-all by default, explicit allows
- Pod Security Standards: Enforced restricted policies
- RBAC: Least privilege for service accounts
- Secrets: External Secrets Operator (ESO) for AWS Secrets Manager integration

**In Our Project:**
```yaml
# Checkpoint 7: Network policies for zero trust
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: chat-service-policy
spec:
  podSelector:
    matchLabels:
      app: chat-service
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: api-gateway  # Only API gateway can call chat service
    ports:
    - protocol: TCP
      port: 3001
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: postgres  # Chat service can only talk to postgres
    ports:
    - protocol: TCP
      port: 5432
  - to:  # Allow external LLM API calls
    - namespaceSelector: {}
    ports:
    - protocol: TCP
      port: 443
```

**Pod Security Standards:**
```yaml
# Enforce restricted pod security for all workloads
apiVersion: v1
kind: Namespace
metadata:
  name: agent-system
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

**Learning Checkpoint:** Checkpoint 7 (Security & Namespaces)

---

### 6. **Cilium Service Mesh (Sidecar-less)**

**What:** eBPF-based networking and service mesh without sidecars.

**Why It Matters:**
- Traditional service meshes (Istio sidecar) add latency and complexity
- Cilium uses Linux kernel eBPF = no sidecar overhead
- Networking, security, and observability at kernel level
- 2025 trend: Sidecar-less is the future

**In Our Project (Optional Advanced):**
```yaml
# Checkpoint 12: Enable Cilium service mesh features
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: orchestrator-l7-policy
spec:
  endpointSelector:
    matchLabels:
      app: orchestrator
  ingress:
  - fromEndpoints:
    - matchLabels:
        app: api-gateway
    toPorts:
    - ports:
      - port: "8000"
        protocol: TCP
      rules:
        http:
        - method: "POST"
          path: "/task"
        - method: "GET"
          path: "/task/.*"
```

**Benefits:**
- mTLS between services (automatic encryption)
- L7 traffic control (HTTP path-based policies)
- No sidecar CPU/memory overhead
- Deep observability with Hubble UI

**Learning Checkpoint:** Checkpoint 12 (Production Advanced)

---

### 7. **AI Agent-Specific Patterns (2025)**

**Agent Sandbox (gVisor):**
- Isolate untrusted agent code execution
- Security for LLM-generated code
- Kubernetes-native primitive for agent workloads

**Observable Agentic Systems:**
- Track token usage per request (cost monitoring)
- Trace: Prompt → LLM → Response → Action
- Metrics: Decision quality, response time
- Essential for regulated AI deployments

**In Our Project:**
```yaml
# Checkpoint 11: Add agent observability
apiVersion: v1
kind: ConfigMap
metadata:
  name: orchestrator-config
data:
  ENABLE_TRACING: "true"
  TRACE_ENDPOINT: "http://otel-collector:4317"
  LOG_LEVEL: "info"
  # Agent-specific metrics
  TRACK_TOKEN_USAGE: "true"
  TRACK_DECISION_QUALITY: "true"
  COST_ALERT_THRESHOLD: "10.0"  # Alert if cost > $10/hour
```

**Python Orchestrator with Tracing:**
```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

tracer = trace.get_tracer(__name__)

@app.post("/task")
async def create_task(task_request: TaskRequest):
    with tracer.start_as_current_span("orchestrator.create_task") as span:
        span.set_attribute("task.id", task_id)
        span.set_attribute("task.type", task_request.type)

        # Break into subtasks
        with tracer.start_as_current_span("orchestrator.break_subtasks"):
            subtasks = break_into_subtasks(task_request)
            span.set_attribute("subtasks.count", len(subtasks))

        # Queue to Redis
        with tracer.start_as_current_span("orchestrator.queue_tasks"):
            for subtask in subtasks:
                redis.lpush("task_queue", json.dumps(subtask))

        return {"task_id": task_id, "status": "queued"}
```

**Learning Checkpoint:** Checkpoint 11 (AI Observability)

---

### 8. **Workload Identity & External Secrets**

**What:** Kubernetes workloads authenticate to cloud providers without storing credentials.

**Why It Matters:**
- No hardcoded secrets in cluster
- AWS IAM roles for service accounts (IRSA)
- External Secrets Operator syncs from AWS Secrets Manager
- Automatic secret rotation

**In Our Project:**
```yaml
# Checkpoint 8: External Secrets Operator
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: chat-service-secrets
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-manager
    kind: ClusterSecretStore
  target:
    name: chat-service-secrets
    creationPolicy: Owner
  data:
  - secretKey: OPENAI_API_KEY
    remoteRef:
      key: agent-system/openai-api-key
  - secretKey: ANTHROPIC_API_KEY
    remoteRef:
      key: agent-system/anthropic-api-key
```

**Learning Checkpoint:** Checkpoint 8 (Secrets Management)

---

### 9. **Resource Efficiency & FinOps**

**Right-Sizing with VPA:**
```yaml
# Vertical Pod Autoscaler recommends CPU/memory
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: orchestrator-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: orchestrator-deployment
  updatePolicy:
    updateMode: "Off"  # Recommendation mode (not auto-apply)
```

**Cost Optimization:**
- KEDA scale-to-zero when idle
- Spot instances for workers (tolerates interruptions)
- Resource quotas per namespace (prevent overspending)

**Learning Checkpoint:** Checkpoint 9 (Auto-Scaling & Efficiency)

---

### 10. **GitOps with ArgoCD (2025 Features)**

**ApplicationSet for Multi-Environment:**
```yaml
# Checkpoint 11: Deploy to dev, staging, prod from one definition
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: agent-system
spec:
  generators:
  - list:
      elements:
      - env: dev
        replicas: "1"
      - env: staging
        replicas: "2"
      - env: prod
        replicas: "5"
  template:
    metadata:
      name: 'agent-system-{{env}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/your-repo/agent-system
        targetRevision: HEAD
        path: helm-chart
        helm:
          values: |
            environment: {{env}}
            orchestrator:
              replicas: {{replicas}}
      destination:
        server: https://kubernetes.default.svc
        namespace: '{{env}}'
```

**Self-Healing + Auto-Sync:**
- Any manual change in cluster → ArgoCD reverts to Git state
- Git is single source of truth
- Audit trail: Every deployment = Git commit

**Learning Checkpoint:** Checkpoint 11 (GitOps)

---

## 📊 Modern Architecture Summary

| Traditional Approach (2020) | Our 2025 Approach | Benefit |
|----------------------------|-------------------|---------|
| Ingress Controller | **Gateway API** | L4+L7, canary deployments, no annotations |
| HPA (CPU/memory) | **KEDA** (event-driven) | Scale on queue depth, cost-efficient |
| Manual instrumentation | **OpenTelemetry** auto-instrumentation | Zero-code observability |
| Basic kubectl apply | **Argo Rollouts** + metrics | Progressive delivery, auto-rollback |
| Istio sidecar mesh | **Cilium** sidecar-less | Lower latency, eBPF kernel networking |
| Secrets in cluster | **External Secrets Operator** | Cloud-native secret management |
| Static manifests | **Crossplane** (optional) | Infrastructure as code in K8s |
| Basic RBAC | **Zero Trust** network policies | Explicit allow, deny-all default |
| Hope-based deployment | **Observable agentic systems** | Token tracking, cost alerts, traces |

---

## 🎯 What Makes This Architecture "2025 Production-Ready"

✅ **Gateway API** - Future-proof routing (Ingress is deprecated)
✅ **Event-Driven Autoscaling** - KEDA for cost-efficient scaling
✅ **Unified Observability** - OpenTelemetry for metrics/logs/traces
✅ **Progressive Delivery** - Argo Rollouts for safe deployments
✅ **Zero Trust Security** - Network policies, Pod Security Standards
✅ **Sidecar-less Service Mesh** - Cilium for performance
✅ **External Secrets** - Cloud-native secret management
✅ **AI-Specific Patterns** - Agent sandboxing, token tracking
✅ **GitOps Native** - ArgoCD ApplicationSets for multi-env
✅ **FinOps Optimized** - KEDA scale-to-zero, VPA recommendations

---

## 🚀 Next Steps

Now that we have the architecture defined, we'll proceed with:

1. **Checkpoint 1**: Build each service locally
   - Write simple Python/Go/TypeScript code
   - Create Dockerfiles
   - Build images
   - Test with `docker-compose`

2. **Checkpoint 2**: Deploy to Kubernetes as Pods
   - Write Pod YAML manifests
   - Deploy with `kubectl apply`
   - Access with `kubectl port-forward`

3. **Continue through Checkpoint 12**: Progressive learning!

---

**Ready to start building?** 🎉

Your coach will guide you through each checkpoint, adapting to your learning pace and answering questions along the way!
