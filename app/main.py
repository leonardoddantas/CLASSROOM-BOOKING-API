from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.classrooms import classroom_router
from app.routers.professors import professor_router
from app.routers.schedules import schedule_router

app = FastAPI(
    title="Smart Classroom Scheduler API",
    description="IoT-based classroom energy management and scheduling system for UFRN - Caicó.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

app.include_router(classroom_router)
app.include_router(professor_router)
app.include_router(schedule_router)