# Task Flow: Orchestrator → Redis → Worker

Complete guide to understanding how tasks flow through the agent system.

---

## 📋 Table of Contents

1. [System Overview](#system-overview)
2. [Step-by-Step Flow](#step-by-step-flow)
3. [Redis Data Structures](#redis-data-structures)
4. [Worker Processing](#worker-processing)
5. [Inspecting Redis](#inspecting-redis)
6. [Common Questions](#common-questions)

---

## 🎯 System Overview

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│   Client    │       │ Orchestrator│       │    Redis    │
│   (curl)    │──────▶│   (Python)  │──────▶│   (Queue)   │
└─────────────┘       └─────────────┘       └──────┬──────┘
                                                    │
                                                    ▼
                                             ┌─────────────┐
                                             │   Worker    │
                                             │    (Go)     │
                                             └─────────────┘
```

**Components:**
- **Client**: Sends HTTP POST request with task description
- **Orchestrator**: Receives task, breaks into subtasks, queues to Redis
- **Redis**: Message queue + data store
- **Worker**: Pulls jobs from queue, executes them, stores results

---

## 🔄 Step-by-Step Flow

### Step 1: Client Sends Task

**Example Request:**
```bash
curl -X POST http://localhost:8001/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Build a user authentication system",
    "priority": 1
  }'
```

**What Happens:**
- HTTP POST → Orchestrator endpoint `/tasks`
- Request body contains task description and priority
- Orchestrator receives: `TaskRequest` object

---

### Step 2: Orchestrator Breaks Task into Subtasks

**Code Location:** [app.py:78](../services/orchestrator/app.py#L78)

```python
# Generate unique task ID
task_id = str(uuid.uuid4())  # Example: "58fcc421-abc5-41d0-90ff-328f625194d9"

# Break task into subtasks (simplified AI logic)
subtasks = _generate_subtasks(task.description)
# Returns: [
#   "Design user database schema",
#   "Implement JWT token generation",
#   "Create login/logout endpoints",
#   "Add password hashing with bcrypt"
# ]
```

**What Happens:**
- Task ID generated (UUID format)
- `_generate_subtasks()` uses keyword matching to break down task
- In production, this would call an LLM API

---

### Step 3: Orchestrator Stores Task Metadata in Redis

**Code Location:** [app.py:80-91](../services/orchestrator/app.py#L80-L91)

```python
# Create task object
task_obj = {
    "task_id": task_id,
    "description": "Build a user authentication system",
    "priority": "1",  # Converted to string for Redis
    "status": "queued",
    "created_at": "2025-11-26T15:49:28.450997",
    "subtasks": "Design user database schema,Implement JWT token generation,..."  # Comma-separated
}

# Store in Redis hash
redis_client.hset(f"task:{task_id}", mapping=task_obj)
```

**Redis Command Equivalent:**
```bash
HSET task:58fcc421-abc5-41d0-90ff-328f625194d9 \
  task_id "58fcc421-abc5-41d0-90ff-328f625194d9" \
  description "Build a user authentication system" \
  priority "1" \
  status "queued" \
  created_at "2025-11-26T15:49:28.450997" \
  subtasks "Design user database schema,Implement JWT token generation,..."
```

**What's Stored:**
- **Redis Data Structure:** Hash (key-value pairs)
- **Key:** `task:<task_id>`
- **Purpose:** Task metadata for status tracking

---

### Step 4: Orchestrator Queues Subtasks to Redis

**Code Location:** [app.py:93-101](../services/orchestrator/app.py#L93-L101)

```python
# Queue each subtask for workers
for idx, subtask in enumerate(subtasks):
    job = {
        "task_id": task_id,
        "subtask_id": f"{task_id}-{idx}",  # Example: "58fcc421-...-0"
        "description": subtask,
        "priority": task.priority
    }
    redis_client.lpush("work_queue", json.dumps(job))
```

**Redis Command Equivalent:**
```bash
LPUSH work_queue '{"task_id": "58fcc421-...", "subtask_id": "58fcc421-...-0", "description": "Design user database schema", "priority": 1}'
LPUSH work_queue '{"task_id": "58fcc421-...", "subtask_id": "58fcc421-...-1", "description": "Implement JWT token generation", "priority": 1}'
LPUSH work_queue '{"task_id": "58fcc421-...", "subtask_id": "58fcc421-...-2", "description": "Create login/logout endpoints", "priority": 1}'
LPUSH work_queue '{"task_id": "58fcc421-...", "subtask_id": "58fcc421-...-3", "description": "Add password hashing with bcrypt", "priority": 1}'
```

**What's Stored:**
- **Redis Data Structure:** List (queue)
- **Key:** `work_queue`
- **Purpose:** Job queue for workers to consume

**IMPORTANT:** `LPUSH` adds to the **left** of the list, so newest items go to the front!

---

### Step 5: Orchestrator Returns Response

**Code Location:** [app.py:111-117](../services/orchestrator/app.py#L111-L117)

```python
return TaskResponse(
    task_id=task_id,
    description=task.description,
    status="queued",
    created_at=created_at,
    subtasks=subtask_objects  # List of {subtask_id, description}
)
```

**Response Body:**
```json
{
  "task_id": "58fcc421-abc5-41d0-90ff-328f625194d9",
  "description": "Build a user authentication system",
  "status": "queued",
  "created_at": "2025-11-26T15:49:28.450997",
  "subtasks": [
    {
      "subtask_id": "58fcc421-abc5-41d0-90ff-328f625194d9-0",
      "description": "Design user database schema"
    },
    {
      "subtask_id": "58fcc421-abc5-41d0-90ff-328f625194d9-1",
      "description": "Implement JWT token generation"
    },
    {
      "subtask_id": "58fcc421-abc5-41d0-90ff-328f625194d9-2",
      "description": "Create login/logout endpoints"
    },
    {
      "subtask_id": "58fcc421-abc5-41d0-90ff-328f625194d9-3",
      "description": "Add password hashing with bcrypt"
    }
  ]
}
```

---

### Step 6: Worker Pulls Job from Redis Queue

**Code Location:** [worker/main.go:124-125](../../checkpoints/01_docker_containers/03_worker.md#L124-L125)

```go
// Block until a job is available (BRPOP with 1 second timeout)
result, err := w.redisClient.BRPop(w.ctx, 1*time.Second, "work_queue").Result()
```

**Redis Command Equivalent:**
```bash
BRPOP work_queue 1
# Returns: ["work_queue", "{\"task_id\": \"58fcc421-...\", ...}"]
```

**What Happens:**
- Worker uses `BRPOP` (Blocking Right Pop) - waits until job available
- Pops from **right** side of list (oldest job first - FIFO queue)
- Returns array: `[queue_name, job_data]`
- If no job available, waits 1 second then tries again

**Why BRPOP?**
- **Efficient:** Worker sleeps until job available (no busy polling)
- **FIFO:** Right pop ensures oldest jobs processed first
- **Atomic:** One worker gets the job, no duplicates

---

### Step 7: Worker Executes Job

**Code Location:** [worker/main.go:154-159](../../checkpoints/01_docker_containers/03_worker.md#L154-L159)

```go
func (w *Worker) executeJob(job Job) {
    log.Printf("📋 [%s] Processing: %s (Task: %s)", w.id, job.Description, job.TaskID)

    // Simulate work with duration based on priority (1-3 seconds)
    workDuration := time.Duration(1+job.Priority) * time.Second
    time.Sleep(workDuration)

    // Store result...
}
```

**What Happens:**
- Worker logs which job it's processing
- Simulates work (in production, this would be actual code execution)
- Duration depends on priority

---

### Step 8: Worker Stores Result in Redis

**Code Location:** [worker/main.go:161-177](../../checkpoints/01_docker_containers/03_worker.md#L161-L177)

```go
// Store result in Redis
result := map[string]interface{}{
    "subtask_id":  job.SubtaskID,
    "task_id":     job.TaskID,
    "status":      "completed",
    "worker_id":   w.id,
    "completed_at": time.Now().UTC().Format(time.RFC3339),
    "description": job.Description,
}

resultJSON, _ := json.Marshal(result)
key := fmt.Sprintf("result:%s", job.SubtaskID)

w.redisClient.Set(w.ctx, key, resultJSON, 24*time.Hour).Err()
```

**Redis Command Equivalent:**
```bash
SET result:58fcc421-abc5-41d0-90ff-328f625194d9-0 \
  '{"subtask_id":"58fcc421-...-0","task_id":"58fcc421-...","status":"completed","worker_id":"worker-1","completed_at":"2025-11-26T16:40:29Z","description":"Design user database schema"}' \
  EX 86400  # Expires in 24 hours
```

**What's Stored:**
- **Redis Data Structure:** String (JSON)
- **Key:** `result:<subtask_id>`
- **Purpose:** Job completion status
- **TTL:** 24 hours (auto-cleanup)

---

## 🗄️ Redis Data Structures

### 1. Task Metadata (Hash)

**Key Pattern:** `task:<task_id>`

**Data Structure:** Redis Hash (like a dictionary/object)

**Example:**
```bash
redis-cli HGETALL task:58fcc421-abc5-41d0-90ff-328f625194d9
```

**Output:**
```
subtasks         "Design user database schema,Implement JWT token generation,..."
priority         "1"
created_at       "2025-11-26T15:49:28.450997"
task_id          "58fcc421-abc5-41d0-90ff-328f625194d9"
description      "Build a user authentication system"
status           "queued"
```

**Purpose:**
- Store task metadata for tracking
- Used by `GET /tasks/{task_id}` endpoint

**Why Hash?**
- Efficient field updates (e.g., update status without rewriting whole object)
- Can query individual fields: `HGET task:123 status`

---

### 2. Work Queue (List)

**Key:** `work_queue`

**Data Structure:** Redis List (ordered collection, used as queue)

**Example:**
```bash
redis-cli LLEN work_queue        # Get queue length
redis-cli LRANGE work_queue 0 -1 # View all items
redis-cli LINDEX work_queue 0    # View first item
```

**Output:**
```
1) "{\"task_id\":\"58fcc421-...\",\"subtask_id\":\"58fcc421-...-3\",\"description\":\"Add password hashing with bcrypt\",\"priority\":1}"
2) "{\"task_id\":\"58fcc421-...\",\"subtask_id\":\"58fcc421-...-2\",\"description\":\"Create login/logout endpoints\",\"priority\":1}"
3) "{\"task_id\":\"58fcc421-...\",\"subtask_id\":\"58fcc421-...-1\",\"description\":\"Implement JWT token generation\",\"priority\":1}"
4) "{\"task_id\":\"58fcc421-...\",\"subtask_id\":\"58fcc421-...-0\",\"description\":\"Design user database schema\",\"priority\":1}"
```

**Purpose:**
- Queue jobs for workers
- FIFO (First In, First Out) processing

**Operations:**
- `LPUSH` - Add job to left (orchestrator)
- `BRPOP` - Remove job from right (worker)

**Why List?**
- Native queue support in Redis
- Atomic operations (no race conditions)
- Blocking pop (efficient waiting)

---

### 3. Results (String with JSON)

**Key Pattern:** `result:<subtask_id>`

**Data Structure:** Redis String (stores JSON)

**Example:**
```bash
redis-cli GET result:58fcc421-abc5-41d0-90ff-328f625194d9-0
```

**Output:**
```json
{
  "completed_at": "2025-11-26T16:40:29Z",
  "description": "Design user database schema",
  "status": "completed",
  "subtask_id": "58fcc421-abc5-41d0-90ff-328f625194d9-0",
  "task_id": "58fcc421-abc5-41d0-90ff-328f625194d9",
  "worker_id": "worker-local"
}
```

**Purpose:**
- Store job completion results
- Used by API to check subtask status

**Why String (not Hash)?**
- Result is immutable once written
- JSON format is flexible for future fields
- TTL (24 hour expiration) works well with strings

---

### 4. Kombu Bindings (Set) - FROM OTHER APPS

**Key Pattern:** `_kombu.binding.*`

**Data Structure:** Redis Set

**Example Keys:**
```
_kombu.binding.celeryev
_kombu.binding.audit
_kombu.binding.celery.pidbox
```

**What Are These?**
- **NOT created by our agent system!**
- Created by Celery (Python task queue framework)
- If you see these, another app on your machine is using the same Redis

**Should You Worry?**
- No! They don't interfere with our system
- Different key namespaces (we use `task:*`, `result:*`, `work_queue`)
- You can ignore them

**How to Filter Them Out:**
```bash
# Only show our keys
redis-cli KEYS "task:*"
redis-cli KEYS "result:*"
redis-cli KEYS "work_queue"
```

---

## 🔍 Inspecting Redis

### Check Queue Status

```bash
# Queue length (number of pending jobs)
docker exec cerra-ai-redis redis-cli LLEN work_queue

# View all jobs in queue (without removing)
docker exec cerra-ai-redis redis-cli LRANGE work_queue 0 -1

# View first 3 jobs
docker exec cerra-ai-redis redis-cli LRANGE work_queue 0 2
```

---

### View Task Metadata

```bash
# List all tasks
docker exec cerra-ai-redis redis-cli KEYS "task:*"

# View specific task
docker exec cerra-ai-redis redis-cli HGETALL task:58fcc421-abc5-41d0-90ff-328f625194d9

# Get just the status
docker exec cerra-ai-redis redis-cli HGET task:58fcc421-abc5-41d0-90ff-328f625194d9 status
```

---

### View Results

```bash
# List all results
docker exec cerra-ai-redis redis-cli KEYS "result:*"

# View specific result
docker exec cerra-ai-redis redis-cli GET result:58fcc421-abc5-41d0-90ff-328f625194d9-0

# Pretty print JSON (requires jq)
docker exec cerra-ai-redis redis-cli GET result:58fcc421-abc5-41d0-90ff-328f625194d9-0 | jq .
```

---

### Monitor Redis in Real-Time

```bash
# Watch all commands being executed
docker exec cerra-ai-redis redis-cli MONITOR

# You'll see:
# 1731860968.450997 [0 127.0.0.1:56818] "HSET" "task:58fcc421-..." "task_id" "58fcc421-..."
# 1731860968.451234 [0 127.0.0.1:56818] "LPUSH" "work_queue" "{\"task_id\":...}"
```

---

### Use RedisInsight (Visual GUI)

**Already installed at:** http://localhost:5540

**Steps:**
1. Open http://localhost:5540 in browser
2. Connect to `localhost:6379`
3. Browse keys visually:
   - 📋 `work_queue` - See queue as a list
   - 🗂️ `task:*` - See task metadata as key-value
   - ✅ `result:*` - See completed results

---

## ❓ Common Questions

### Q1: Why is `work_queue` length 0 even though I created tasks?

**Answer:** Workers already processed them!

- Jobs are **consumed** from the queue when workers process them
- Empty queue = all jobs completed (good!)
- Check results instead: `redis-cli KEYS "result:*"`

---

### Q2: What are the `_kombu.binding.*` keys?

**Answer:** Created by Celery (not our system).

- Another app on your machine is using the same Redis
- Doesn't affect our system (different namespace)
- Ignore them or filter: `redis-cli KEYS "task:*"`

---

### Q3: How do I know if a job is still processing vs completed?

**Check these:**

1. **Queue status:**
   ```bash
   redis-cli LLEN work_queue  # > 0 means jobs pending
   ```

2. **Results status:**
   ```bash
   redis-cli KEYS "result:<subtask_id>"  # Exists = completed
   redis-cli GET "result:<subtask_id>" | jq .status  # "completed"
   ```

3. **Worker logs:**
   ```bash
   docker logs -f worker-1  # See what worker is doing
   ```

---

### Q4: Why use LPUSH + BRPOP instead of RPUSH + BLPOP?

**Answer:** Convention for FIFO queue.

- `LPUSH` adds to **left** (newest at position 0)
- `BRPOP` removes from **right** (oldest at position -1)
- Result: **FIFO (First In, First Out)** queue

**Visualization:**
```
LPUSH work_queue "job-3"
LPUSH work_queue "job-2"
LPUSH work_queue "job-1"

Redis List:
[job-1, job-2, job-3]
 ↑                 ↑
LEFT            RIGHT

BRPOP work_queue  → Returns "job-3" (oldest)
BRPOP work_queue  → Returns "job-2"
BRPOP work_queue  → Returns "job-1"
```

---

### Q5: Why store results with 24-hour TTL?

**Answer:** Auto-cleanup to save memory.

- Results are temporary (only needed for status checks)
- After 24 hours, they're no longer relevant
- Redis auto-deletes expired keys (no manual cleanup!)

**Check TTL:**
```bash
redis-cli TTL result:58fcc421-...-0  # Returns seconds remaining
```

---

### Q6: Can I replay completed jobs?

**No, once BRPOP removes a job, it's gone from the queue.**

**Options:**
1. **Re-queue manually:**
   ```bash
   redis-cli LPUSH work_queue '{"task_id":"...","subtask_id":"...","description":"...","priority":1}'
   ```

2. **Create new task via API:**
   ```bash
   curl -X POST http://localhost:8001/tasks -H "Content-Type: application/json" -d '{"description":"...","priority":1}'
   ```

3. **Production pattern:** Store jobs in permanent storage (PostgreSQL) before queuing

---

### Q7: How do multiple workers share the queue?

**Answer:** Redis BRPOP is atomic - only ONE worker gets each job.

**Example with 3 workers:**
```
Queue: [job-1, job-2, job-3, job-4]

Worker-1: BRPOP → Gets job-4
Worker-2: BRPOP → Gets job-3
Worker-3: BRPOP → Gets job-2
Worker-1: BRPOP → Gets job-1

No duplicates! Each job processed exactly once.
```

---

### Q8: What happens if a worker crashes mid-job?

**Current System:** Job is lost (BRPOP removed it from queue).

**Production Solution:** Use Redis Streams or reliable queue pattern:
```python
# Move job to "processing" list first
redis.rpoplpush("work_queue", "processing_queue")

# Process job...

# On success, remove from processing
redis.lrem("processing_queue", job)

# On crash, another worker can retry jobs in "processing_queue"
```

---

## 🎓 Summary

### Data Flow
```
1. Client sends task → Orchestrator
2. Orchestrator breaks into subtasks
3. Orchestrator stores task metadata (Hash: task:*)
4. Orchestrator queues subtasks (List: work_queue)
5. Worker pulls job (BRPOP work_queue)
6. Worker executes job
7. Worker stores result (String: result:*)
8. Client checks status (GET /tasks/{task_id})
```

### Redis Keys
- **`task:<task_id>`** - Task metadata (Hash)
- **`work_queue`** - Job queue (List)
- **`result:<subtask_id>`** - Job results (String with JSON, 24h TTL)
- **`_kombu.binding.*`** - Ignore (from other apps)

### Important Concepts
- **LPUSH + BRPOP** = FIFO queue
- **Blocking Pop** = Efficient waiting (no polling)
- **Atomic Operations** = No race conditions
- **TTL** = Auto-cleanup (memory efficient)

---

**Next:** Build the Worker service (Checkpoint 1.3) to start processing these jobs!
