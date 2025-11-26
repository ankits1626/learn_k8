# Checkpoint 1.3: Worker Service (Go)

## 🎯 Goals

Build high-performance workers that pull tasks from Redis queue and execute them.

- ✅ Create Go service with Redis integration
- ✅ Implement task processing loop
- ✅ Write multi-stage Dockerfile
- ✅ Test with orchestrator

**Time:** 20 minutes

---

## 📦 Part 1: Initialize Go Module

```bash
cd services/worker

# Initialize Go module
go mod init github.com/yourusername/agent-system/worker

# Add Redis client dependency
go get github.com/redis/go-redis/v9
```

**What just happened?**
- `go mod init` creates `go.mod` (dependency manifest)
- `go get` downloads Redis client library
- Go automatically manages dependencies (no separate tool needed)

---

## 🧑‍💻 Part 2: Create Application Code

**File: `main.go`**

```go
package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/redis/go-redis/v9"
)

// Job represents a task from the queue
type Job struct {
	TaskID     string `json:"task_id"`
	SubtaskID  string `json:"subtask_id"`
	Description string `json:"description"`
	Priority   int    `json:"priority"`
}

// Worker processes jobs from Redis queue
type Worker struct {
	id          string
	redisClient *redis.Client
	ctx         context.Context
}

func main() {
	// Get configuration from environment
	redisHost := getEnv("REDIS_HOST", "localhost")
	redisPort := getEnv("REDIS_PORT", "6379")
	workerID := getEnv("WORKER_ID", "worker-1")

	ctx := context.Background()

	// Connect to Redis
	rdb := redis.NewClient(&redis.Options{
		Addr:         fmt.Sprintf("%s:%s", redisHost, redisPort),
		Password:     "",
		DB:           0,
		DialTimeout:  2 * time.Second,
		ReadTimeout:  2 * time.Second,
		WriteTimeout: 2 * time.Second,
	})

	// Test connection
	if err := rdb.Ping(ctx).Err(); err != nil {
		log.Fatalf("❌ Failed to connect to Redis: %v", err)
	}
	log.Printf("✅ Worker %s connected to Redis at %s:%s", workerID, redisHost, redisPort)

	// Create worker
	worker := &Worker{
		id:          workerID,
		redisClient: rdb,
		ctx:         ctx,
	}

	// Setup graceful shutdown
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)

	// Start worker loop
	go worker.processJobs()

	// Wait for shutdown signal
	sig := <-sigChan
	log.Printf("🛑 Received signal %v, shutting down gracefully...", sig)

	// Cleanup
	if err := rdb.Close(); err != nil {
		log.Printf("⚠️  Error closing Redis: %v", err)
	}
	log.Println("👋 Worker shutdown complete")
}

// processJobs continuously pulls jobs from Redis queue and processes them
func (w *Worker) processJobs() {
	log.Printf("🚀 Worker %s started processing jobs", w.id)

	for {
		// Block until a job is available (BRPOP with 1 second timeout)
		result, err := w.redisClient.BRPop(w.ctx, 1*time.Second, "work_queue").Result()

		if err == redis.Nil {
			// Timeout - no jobs available, continue polling
			continue
		}

		if err != nil {
			log.Printf("⚠️  Error fetching job: %v", err)
			time.Sleep(2 * time.Second)
			continue
		}

		// result[0] is the queue name, result[1] is the job data
		jobData := result[1]

		// Parse job
		var job Job
		if err := json.Unmarshal([]byte(jobData), &job); err != nil {
			log.Printf("❌ Failed to parse job: %v", err)
			continue
		}

		// Process the job
		w.executeJob(job)
	}
}

// executeJob simulates task execution
func (w *Worker) executeJob(job Job) {
	log.Printf("📋 [%s] Processing: %s (Task: %s)", w.id, job.Description, job.TaskID)

	// Simulate work with random duration (1-3 seconds)
	workDuration := time.Duration(1+job.Priority) * time.Second
	time.Sleep(workDuration)

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

	if err := w.redisClient.Set(w.ctx, key, resultJSON, 24*time.Hour).Err(); err != nil {
		log.Printf("❌ Failed to store result: %v", err)
		return
	}

	log.Printf("✅ [%s] Completed: %s", w.id, job.Description)
}

// getEnv gets environment variable with fallback default
func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}
```

**Key Features:**
- ✅ Blocking Redis queue pop (BRPOP) - efficient waiting
- ✅ Graceful shutdown handling (SIGTERM/SIGINT)
- ✅ JSON job parsing
- ✅ Simulated work with configurable duration
- ✅ Store results back to Redis
- ✅ Environment-based configuration

---

## 🐳 Part 3: Create Multi-Stage Dockerfile

**File: `Dockerfile`**

```dockerfile
# Stage 1: Build
FROM golang:1.21-alpine AS builder

# Install build dependencies
RUN apk add --no-cache git

# Set working directory
WORKDIR /build

# Copy go.mod and go.sum first (for layer caching)
COPY go.mod go.sum ./

# Download dependencies
RUN go mod download

# Copy source code
COPY main.go ./

# Build the binary
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o worker .

# Stage 2: Runtime
FROM alpine:latest

# Add ca-certificates for HTTPS connections
RUN apk --no-cache add ca-certificates

WORKDIR /app

# Copy binary from builder stage
COPY --from=builder /build/worker .

# Run as non-root user for security
RUN adduser -D -u 1000 worker
USER worker

# Run the worker
CMD ["./worker"]
```

**Multi-Stage Build Benefits:**
- ✅ **Stage 1 (builder):** Full Go toolchain (large ~300MB)
- ✅ **Stage 2 (runtime):** Only compiled binary + Alpine (small ~10MB)
- ✅ Final image is 97% smaller!
- ✅ No Go compiler or source code in production image (security)

---

## 🧪 Part 4: Test Locally

### Step 4.1: Run Worker Locally

```bash
cd services/worker

# Build the Go binary
go build -o worker

# Run worker (make sure Redis is running from previous step)
REDIS_HOST=localhost REDIS_PORT=6379 WORKER_ID=worker-local ./worker
```

**Expected output:**
```
✅ Worker worker-local connected to Redis at localhost:6379
🚀 Worker worker-local started processing jobs
```

### Step 4.2: Send Jobs from Orchestrator

**Terminal 2: Create a task via orchestrator**
```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Build API endpoints",
    "priority": 1
  }'
```

**Terminal 1: Watch worker process jobs**
```
📋 [worker-local] Processing: Define API endpoints and routes (Task: abc123)
✅ [worker-local] Completed: Define API endpoints and routes
📋 [worker-local] Processing: Implement request validation (Task: abc123)
✅ [worker-local] Completed: Implement request validation
...
```

### Step 4.3: Check Results in Redis

```bash
# List all result keys
docker exec redis-local redis-cli KEYS "result:*"

# Get a specific result
docker exec redis-local redis-cli GET "result:abc123-0"
```

**Expected:**
```json
{
  "subtask_id": "abc123-0",
  "task_id": "abc123",
  "status": "completed",
  "worker_id": "worker-local",
  "completed_at": "2025-11-26T10:45:00Z",
  "description": "Define API endpoints and routes"
}
```

---

## 🐳 Part 5: Build Docker Image

```bash
cd services/worker

# Build the image
docker build -t worker:latest .

# Check image size (should be ~10MB!)
docker images worker:latest

# Test the image
docker run -d \
  --name worker-test \
  --network host \
  -e REDIS_HOST=localhost \
  -e REDIS_PORT=6379 \
  -e WORKER_ID=worker-docker \
  worker:latest

# Check logs
docker logs -f worker-test

# Send a job and watch it process
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"description": "Test task", "priority": 1}'

# Cleanup
docker stop worker-test && docker rm worker-test
```

---

## 🐳 Part 6: Test Multiple Workers (Horizontal Scaling)

```bash
# Start 3 workers
docker run -d --name worker-1 --network host \
  -e REDIS_HOST=localhost -e WORKER_ID=worker-1 worker:latest

docker run -d --name worker-2 --network host \
  -e REDIS_HOST=localhost -e WORKER_ID=worker-2 worker:latest

docker run -d --name worker-3 --network host \
  -e REDIS_HOST=localhost -e WORKER_ID=worker-3 worker:latest

# Watch all worker logs
docker logs -f worker-1 &
docker logs -f worker-2 &
docker logs -f worker-3 &

# Send a big task (creates 4 subtasks)
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"description": "Build a user authentication system", "priority": 1}'

# Watch jobs distributed across workers!

# Cleanup
docker stop worker-1 worker-2 worker-3
docker rm worker-1 worker-2 worker-3
```

**You'll see jobs distributed across workers:**
```
worker-1: ✅ Completed: Design user database schema
worker-3: ✅ Completed: Implement JWT token generation
worker-2: ✅ Completed: Create login/logout endpoints
worker-1: ✅ Completed: Add password hashing with bcrypt
```

**This is horizontal scaling in action!** 🚀

---

## ✅ Verification Checklist

- [ ] Go module initialized with Redis dependency
- [ ] `main.go` created with job processing loop
- [ ] Multi-stage Dockerfile created
- [ ] Worker runs locally and processes jobs from Redis
- [ ] Docker image builds successfully (~10MB size)
- [ ] Multiple workers can run concurrently
- [ ] Jobs are distributed across workers
- [ ] Results stored in Redis

---

## 🎓 What You Learned

- ✅ Go for high-performance background workers
- ✅ Redis blocking pop (BRPOP) for efficient queue polling
- ✅ Multi-stage Docker builds for tiny images
- ✅ Graceful shutdown handling
- ✅ Horizontal scaling pattern (multiple workers, one queue)
- ✅ Environment-based configuration

---

## 🚀 Next Steps

Continue to **[04_gateway.md](04_gateway.md)** to build the API Gateway (Go) that routes HTTP requests.
