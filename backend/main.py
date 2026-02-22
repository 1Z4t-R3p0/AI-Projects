import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import router as api_router
from backend.scheduler.tasks import start_scheduler

app = FastAPI(
    title="AI Learning Roadmap Assistant",
    description="Final Year Project - Backend API",
    version="1.0.0"
)

# CORS Middleware (Allow Frontend Access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routes
app.include_router(api_router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    print("🚀 System Starting Up...")
    start_scheduler()
    print("⏰ Scheduler Started")

@app.get("/")
def read_root():
    return {"status": "active", "message": "AI Roadmap Assistant Backend is Running"}
