from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid
from backend.storage.redis_client import RedisClient

router = APIRouter()
redis_client = RedisClient()

# Models
class Task(BaseModel):
    id: Optional[str] = None
    title: str
    completed: bool = False
    session_id: str

class TaskUpdate(BaseModel):
    completed: Optional[bool] = None
    title: Optional[str] = None

class StudySession(BaseModel):
    session_id: str
    minutes: int

# Routes
@router.get("/tasks/{session_id}", response_model=List[Task])
async def get_tasks(session_id: str):
    return redis_client.get_tasks(session_id)

@router.post("/tasks", response_model=Task)
async def add_task(task: Task):
    if not task.session_id:
        raise HTTPException(status_code=400, detail="Session ID is required")
        
    if not task.id:
        task.id = str(uuid.uuid4())
    redis_client.add_task(task.session_id, task.dict())
    return task

@router.put("/tasks/{session_id}/{task_id}")
async def update_task(session_id: str, task_id: str, update: TaskUpdate):
    redis_client.update_task(session_id, task_id, update.dict(exclude_unset=True))
    return {"status": "updated"}

@router.delete("/tasks/{session_id}/{task_id}")
async def delete_task(session_id: str, task_id: str):
    redis_client.delete_task(session_id, task_id)
    return {"status": "deleted"}

@router.post("/timer/log")
async def log_study(session: StudySession):
    redis_client.log_study_session(session.session_id, session.minutes)
    return {"status": "logged"}

@router.get("/analytics/{session_id}")
async def get_analytics(session_id: str):
    stats = redis_client.get_study_stats(session_id)
    tasks = redis_client.get_tasks(session_id)
    completed_tasks = len([t for t in tasks if t.get("completed")])
    
    return {
        "study_stats": stats,
        "task_stats": {
            "total": len(tasks),
            "completed": completed_tasks,
            "pending": len(tasks) - completed_tasks
        }
    }
