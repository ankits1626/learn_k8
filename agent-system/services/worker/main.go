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
	TaskID      string `json:"task_id"`
	SubtaskID   string `json:"subtask_id"`
	Description string `json:"description"`
	Priority    int    `json:"priority"`
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
		"subtask_id":   job.SubtaskID,
		"task_id":      job.TaskID,
		"status":       "completed",
		"worker_id":    w.id,
		"completed_at": time.Now().UTC().Format(time.RFC3339),
		"description":  job.Description,
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
