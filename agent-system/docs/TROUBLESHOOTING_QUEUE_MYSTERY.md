# Troubleshooting: The Mysterious Disappearing Queue

**Problem**: Tasks were created successfully, but `work_queue` was always empty (length 0).

**Initial Symptoms:**
```bash
$ curl -X POST http://localhost:8001/tasks \
  -H "Content-Type: application/json" \
  -d '{"description":"Build a user authentication system","priority":1}'

# Response: 200 OK with task_id

$ docker exec cerra-ai-redis redis-cli LLEN work_queue
0  # ❌ Expected: 4 (number of subtasks)
```

---

## 🔍 Investigation Process

### Step 1: Check if tasks were created
```bash
$ docker exec cerra-ai-redis redis-cli KEYS "task:*"
task:58fcc421-abc5-41d0-90ff-328f625194d9  # ✅ Task exists!
```

**Finding**: Tasks WERE being created in Redis, just not appearing in the queue.

---

### Step 2: Check for errors in orchestrator logs
```bash
$ docker compose logs orchestrator
...
📋 Created task 58fcc421-abc5-41d0-90ff-328f625194d9 with 4 subtasks
INFO: 200 OK
```

**Finding**: No errors! Log says task was created with 4 subtasks.

---

### Step 3: Added debug logging to trace execution

**Added prints before/after `redis_client.lpush()`:**
```python
print(f"🔧 Pushing job {idx}: {job}")
redis_client.lpush("work_queue", json.dumps(job))
print(f"🔧 Job {idx} pushed successfully")
```

**Initial Result**: Debug logs showed:
```
🔧 Task stored successfully
```
But NEVER showed the "Pushing job" messages!

**Root Cause #1**: Live reload (`--reload` flag) wasn't picking up file changes inside Docker container. Had to manually restart:
```bash
docker compose restart orchestrator
```

---

### Step 4: After restart - debug logs appeared!

```
🔧 Queuing 3 jobs to work_queue
🔧 Pushing job 0: {'task_id': '...', 'subtask_id': '...-0', ...}
🔧 Job 0 pushed successfully
🔧 Pushing job 1: {'task_id': '...', 'subtask_id': '...-1', ...}
🔧 Job 1 pushed successfully
🔧 Pushing job 2: {'task_id': '...', 'subtask_id': '...-2', ...}
🔧 Job 2 pushed successfully
📋 Created task ee59d1d0-dd84-47bb-89fa-d11aefc61646 with 3 subtasks
```

**Finding**: Jobs ARE being pushed! All 3 jobs pushed successfully.

---

### Step 5: Immediately checked Redis queue

```bash
$ docker exec cerra-ai-redis redis-cli LLEN work_queue
0  # Still empty!
```

**How is this possible?** Jobs were pushed successfully but disappeared instantly!

---

### Step 6: Monitored Redis in real-time

```bash
$ docker exec cerra-ai-redis redis-cli MONITOR
1764176807.945810 [0 172.66.0.243:63875] "brpop" "work_queue" "1"
```

**BINGO!** There's a worker at IP `172.66.0.243` constantly polling `work_queue` with `BRPOP`!

---

### Step 7: Found the culprit

```bash
$ docker ps --format "{{.Names}}\t{{.Image}}"
cerra-ai-worker  ai-cerra-ai-worker  # ← This is a Celery worker!
```

**Root Cause #2**: Your `cerra-ai-worker` container (from another project - a Celery-based AI app) was **consuming jobs immediately**!

---

## 🎯 Final Answer

**The orchestrator code was working correctly all along!** Here's what was happening:

```
1. Orchestrator → LPUSH "work_queue" (adds job to left side)
   ✅ Success! Job in queue

2. 0.001 seconds later...
   cerra-ai-worker → BRPOP "work_queue" (removes job from right side)
   ✅ Celery worker got the job!

3. You check queue:
   LLEN work_queue → 0 (empty)
   😕 "Where did my jobs go?"
```

**Timeline visualization:**
```
T+0ms:     Orchestrator pushes 3 jobs  → Queue: [job3, job2, job1]
T+10ms:    Celery worker BRPOP         → Queue: [job3, job2] (took job1)
T+20ms:    Celery worker BRPOP         → Queue: [job3] (took job2)
T+30ms:    Celery worker BRPOP         → Queue: [] (took job3)
T+1000ms:  You check queue             → Queue: [] (empty!)
```

---

## ✅ Solutions

### Option A: Stop Conflicting Worker (Quick Fix)
```bash
# Stop the Celery worker while testing
docker stop cerra-ai-worker

# Now test your orchestrator
curl -X POST http://localhost:8001/tasks \
  -H "Content-Type: application/json" \
  -d '{"description":"Test","priority":1}'

# Check queue (should have jobs now!)
docker exec cerra-ai-redis redis-cli LLEN work_queue  # Returns: 3
```

### Option B: Use Different Queue Name (Proper Fix)

**Modify `app.py`:**
```python
# Change all instances of "work_queue" to "agent_work_queue"
redis_client.lpush("agent_work_queue", json.dumps(job))  # Line 107
```

**Also update worker (when you build it in Checkpoint 1.3):**
```go
result, err := w.redisClient.BRPop(w.ctx, 1*time.Second, "agent_work_queue").Result()
```

**Benefits:**
- ✅ No conflict with other projects
- ✅ Can run both systems simultaneously
- ✅ Clearer separation of concerns

---

## 🐛 Bonus Issue: Live Reload Not Working

**Problem**: Changes to `app.py` weren't being picked up automatically.

**Root Cause**: Volume mount + `--reload` flag in Docker Compose should work, but file change detection inside containers can be unreliable on macOS (Docker Desktop uses a VM).

**Workarounds:**
1. **Manual restart after code changes:**
   ```bash
   docker compose restart orchestrator
   ```

2. **Watch for the reload message in logs:**
   ```bash
   docker compose logs -f orchestrator
   # Look for: "WARNING: StatReload detected changes in 'app.py'. Reloading..."
   ```

3. **Use rebuild for major changes:**
   ```bash
   docker compose up -d --build
   ```

---

## 📚 Key Learnings

### 1. Multiple Apps Can Share Redis
- Redis is a shared resource - multiple apps can connect to the same instance
- Queue names (`work_queue`, `celery`, etc.) are just string keys
- If two apps use the same queue name, they'll compete for jobs!

### 2. BRPOP is Blocking and Fast
- Celery workers use `BRPOP` with 1-second timeout
- They continuously poll: `BRPOP → process → BRPOP → process...`
- Jobs disappear almost instantly (< 10ms)

### 3. Debug Logging is Essential
- Print statements before/after critical operations
- Helps trace execution flow
- Reveals timing issues (like this one!)

### 4. Docker Volume Mounts Have Quirks
- File change detection isn't always instant
- macOS Docker Desktop adds extra latency (VM layer)
- When in doubt, manual restart is reliable

---

## 🔍 How to Avoid This in Future

### Check for Conflicting Services
```bash
# Before starting your project, check what's using Redis
docker exec <redis-container> redis-cli CLIENT LIST

# Check what's polling your queue
docker exec <redis-container> redis-cli MONITOR | grep work_queue

# List all containers
docker ps --format "{{.Names}}\t{{.Image}}"
```

### Use Project-Specific Queue Names
```python
# ❌ Generic name (conflicts possible)
QUEUE_NAME = "work_queue"

# ✅ Project-specific name
QUEUE_NAME = "agent_system_work_queue"
```

### Add Queue Monitoring
```python
# Before pushing jobs
queue_len_before = redis_client.llen("work_queue")
print(f"Queue length before: {queue_len_before}")

# After pushing jobs
queue_len_after = redis_client.llen("work_queue")
print(f"Queue length after: {queue_len_after}")
print(f"Jobs added: {queue_len_after - queue_len_before}")
```

---

## 🎉 Conclusion

**Your code was working perfectly!** The "bug" was actually another application consuming your jobs. This is a great real-world lesson about:

- Shared resources in development
- Debugging distributed systems
- Redis queue mechanics (LPUSH + BRPOP)
- Docker networking and container interactions

**Next Steps:**
1. Decide: Stop `cerra-ai-worker` OR rename your queue
2. Remove debug logging (or keep it for learning!)
3. Continue to **Checkpoint 1.3: Build the Worker Service** 🚀

---

**Pro Tip**: This exact scenario happens in production too! Always use unique queue names per service/environment:
- `prod_payments_queue`
- `staging_payments_queue`
- `dev_payments_queue`

Never use generic names like `tasks`, `jobs`, `work`, etc.
