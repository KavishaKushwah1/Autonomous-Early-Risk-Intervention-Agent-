from fastapi import FastAPI
from models import AcademicRecord, BehavioralEngagement
import db_models
from database import engine, Base

# This is the magic line that creates the database file!
Base.metadata.create_all(bind=engine)

# Initialize the FastAPI app
app = FastAPI(
    title="Autonomous Early Risk Intervention Agent API",
    description="Backend API for tracking student holistic development and AI interventions.",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Autonomous Education Agent API! Server is running smoothly."}

@app.post("/api/v1/observe/academic")
def record_academic_data(data: AcademicRecord):
    return {
        "status": "success", 
        "message": f"Recorded {data.subject} score of {data.score} for student {data.student_id}"
    }

@app.post("/api/v1/observe/behavior")
def record_behavioral_data(data: BehavioralEngagement):
    return {
        "status": "success", 
        "message": f"Recorded {data.activity_type} engagement for student {data.student_id}"
    }