from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
import app.models.student
import app.models.teacher
from app.routers import students, teachers, ai_agent

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student AI Platform", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(students.router)
app.include_router(teachers.router)
app.include_router(ai_agent.router)

@app.get("/")
def root():
    return {"message": "Student AI Platform API", "docs": "/docs"}