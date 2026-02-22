from fastapi import APIRouter
from backend.api import chat, roadmap, resources, productivity

router = APIRouter()

router.include_router(chat.router, prefix="/chat", tags=["Chat"])
router.include_router(roadmap.router, prefix="/roadmap", tags=["Roadmap"])
router.include_router(resources.router, prefix="/resources", tags=["Resources"])
router.include_router(productivity.router, prefix="/productivity", tags=["Productivity"])
