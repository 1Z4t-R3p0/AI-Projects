from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.rag.engine import rag_engine

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    department: str = "General"
    session_id: str = None  # Optional session ID for context memory

@router.post("/query")
async def query_chat(request: ChatRequest):
    try:
        response = await rag_engine.process_query(request.message, request.department, request.session_id)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{session_id}")
async def get_chat_history(session_id: str):
    try:
        # We can access redis_client from rag_engine since it's already initialized there
        history = rag_engine.redis.get_chat_history(session_id)
        return {"history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/session/{session_id}")
async def delete_session(session_id: str):
    try:
        rag_engine.redis.delete_session_data(session_id)
        return {"message": "Session deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
