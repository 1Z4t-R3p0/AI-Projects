import redis
import json
import os
from typing import List, Dict

class RedisClient:
    def __init__(self, host=os.getenv('REDIS_HOST', 'localhost'), port=int(os.getenv('REDIS_PORT', 6379)), db=0):
        self.client = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        self.expiry = 86400  # 24 hours

    def add_message(self, session_id: str, role: str, content: str):
        """Adds a message to the session history."""
        if not session_id:
            return
            
        key = f"chat:{session_id}"
        message = json.dumps({"role": role, "content": content})
        
        # Push to list (Right Push)
        self.client.rpush(key, message)
        
        # Trim to keep only last 20 messages (10 interactions)
        self.client.ltrim(key, -20, -1)
        
        # Reset expiry on update
        self.client.expire(key, self.expiry)

    def get_context(self, session_id: str, limit: int = 10) -> List[Dict[str, str]]:
        """Retrieves the last N messages for context."""
        if not session_id:
            return []
            
        key = f"chat:{session_id}"
        # Get last 'limit' messages
        messages = self.client.lrange(key, -limit, -1)
        return [json.loads(m) for m in messages]

    def get_chat_history(self, session_id: str) -> List[Dict[str, str]]:
        """Retrieves default full history for the frontend."""
        if not session_id:
            return []
            
        key = f"chat:{session_id}"
        # Get all messages
        messages = self.client.lrange(key, 0, -1)
        return [json.loads(m) for m in messages]


    def clear_history(self, session_id: str):
        """Clears the session history."""
        if session_id:
            self.client.delete(f"chat:{session_id}")

    def delete_session_data(self, session_id: str):
        """Wipes all data associated with a session (chat, tasks, study)."""
        if not session_id:
            return
        keys = [f"chat:{session_id}", f"tasks:{session_id}", f"study:{session_id}"]
        self.client.delete(*keys)

    # --- Productivity Features ---
    def add_task(self, session_id: str, task: Dict) -> str:
        """Adds a task to the user's list."""
        if not session_id: return ""
        task_id = task.get("id")
        key = f"tasks:{session_id}"
        self.client.hset(key, task_id, json.dumps(task))
        return task_id

    def get_tasks(self, session_id: str) -> List[Dict]:
        """Retrieves all tasks for a user."""
        if not session_id: return []
        key = f"tasks:{session_id}"
        tasks = self.client.hgetall(key)
        return [json.loads(t) for t in tasks.values()]

    def update_task(self, session_id: str, task_id: str, data: Dict):
        """Updates a specific task."""
        if not session_id: return
        key = f"tasks:{session_id}"
        # Check if exists first
        current = self.client.hget(key, task_id)
        if current:
            task = json.loads(current)
            task.update(data)
            self.client.hset(key, task_id, json.dumps(task))

    def delete_task(self, session_id: str, task_id: str):
        """Deletes a task."""
        if not session_id: return
        key = f"tasks:{session_id}"
        self.client.hdel(key, task_id)

    def log_study_session(self, session_id: str, minutes: int):
        """Logs a completed study session."""
        if not session_id: return
        key = f"study:{session_id}"
        # Store as simple list of durations
        self.client.rpush(key, minutes)

    def get_study_stats(self, session_id: str) -> Dict[str, int]:
        """Calculates total study intervals."""
        if not session_id: return {"total_sessions": 0, "total_minutes": 0}
        key = f"study:{session_id}"
        sessions = self.client.lrange(key, 0, -1)
        total_minutes = sum([int(m) for m in sessions])
        return {
            "total_sessions": len(sessions),
            "total_minutes": total_minutes
        }
