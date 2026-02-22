from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
import json

router = APIRouter()

class RoadmapRequest(BaseModel):
    department: str
    level: str # Beginner, Intermediate, Advanced
    goals: Optional[str] = None

@router.post("/generate")
async def generate_roadmap(request: RoadmapRequest):
    # In a real scenario, this would call the LLM to generate a dynamic JSON.
    # For the prototype, we can check for cached roadmaps or generate one.
    
    from backend.rag.engine import rag_engine
    roadmap_data = await rag_engine.generate_roadmap(request.department, request.level)
    return roadmap_data
