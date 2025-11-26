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


class Subtask(BaseModel):
    subtask_id: str
    description: str


class TaskResponse(BaseModel):
    task_id: str
    description: str
    status: str
    created_at: str
    subtasks: list[Subtask]


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
    print(f"🔧 Generated {len(subtasks)} subtasks: {subtasks}")

    # Create task object
    task_obj = {
        "task_id": task_id,
        "description": task.description,
        "priority": str(task.priority),
        "status": "queued",
        "created_at": created_at,
        "subtasks": ",".join(subtasks)  # Convert list to comma-separated string
    }
    print(f"🔧 Task object created: {task_obj}")

    # Store task in Redis hash
    print(f"🔧 Storing task in Redis: task:{task_id}")
    redis_client.hset(f"task:{task_id}", mapping=task_obj)
    print(f"🔧 Task stored successfully")

    # Queue each subtask for workers
    print(f"🔧 Queuing {len(subtasks)} jobs to work_queue")
    for idx, subtask in enumerate(subtasks):
        job = {
            "task_id": task_id,
            "subtask_id": f"{task_id}-{idx}",
            "description": subtask,
            "priority": task.priority
        }
        print(f"🔧 Pushing job {idx}: {job}")
        redis_client.lpush("work_queue", json.dumps(job))
        print(f"🔧 Job {idx} pushed successfully")

    print(f"📋 Created task {task_id} with {len(subtasks)} subtasks")

    # Build subtask objects with IDs
    subtask_objects = [
        {"subtask_id": f"{task_id}-{idx}", "description": subtask}
        for idx, subtask in enumerate(subtasks)
    ]

    return TaskResponse(
        task_id=task_id,
        description=task.description,
        status="queued",
        created_at=created_at,
        subtasks=subtask_objects
    )


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: str):
    """Get task status by ID"""
    if not redis_client:
        raise HTTPException(status_code=503, detail="Redis unavailable")

    task_data = redis_client.hgetall(f"task:{task_id}")

    if not task_data:
        raise HTTPException(status_code=404, detail="Task not found")

    # Parse comma-separated subtasks back into list
    subtasks_list = task_data.get("subtasks", "").split(",")

    # Reconstruct subtask objects with IDs
    subtask_objects = [
        {"subtask_id": f"{task_id}-{idx}", "description": subtask}
        for idx, subtask in enumerate(subtasks_list) if subtask
    ]

    return TaskResponse(
        task_id=task_data["task_id"],
        description=task_data["description"],
        status=task_data["status"],
        created_at=task_data["created_at"],
        subtasks=subtask_objects
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