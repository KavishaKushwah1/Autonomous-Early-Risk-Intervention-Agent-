from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from models import AcademicRecord, BehavioralEngagement
import db_models
from database import engine, Base, SessionLocal

# --- NEW: Import the AI Brain ---
from agent import run_ai_analysis 

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Autonomous Early Risk Intervention Agent API",
    version="1.0.0"
)

# Dependency to open and close the database connection for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Autonomous Education Agent API! Server is running smoothly."}

@app.post("/api/v1/observe/academic")
def record_academic_data(data: AcademicRecord, db: Session = Depends(get_db)):
    # 1. Save to Database
    new_record = db_models.DBAcademicRecord(
        student_id=data.student_id,
        subject=data.subject,
        score=data.score,
        assessment_type=data.assessment_type
    )
    db.add(new_record)
    db.commit()
    
    # 2. --- THE AI TRIGGER ---
    # We translate the raw data into a readable sentence for the AI
    student_text = f"Student ID {data.student_id} just scored {data.score}% on their {data.subject} {data.assessment_type}."
    
    # Wake up the AI to analyze it!
    ai_intervention = run_ai_analysis(student_text)
    
    return {
        "status": "success", 
        "message": f"Permanently saved {data.subject} score for student {data.student_id}",
        "ai_analysis": ai_intervention # We return the AI's plan so you can see it!
    }

@app.post("/api/v1/observe/behavior")
def record_behavioral_data(data: BehavioralEngagement, db: Session = Depends(get_db)):
    # 1. Save to Database
    new_engagement = db_models.DBBehavioralEngagement(
        student_id=data.student_id,
        activity_type=data.activity_type,
        engagement_score=data.engagement_score,
        self_reflection_notes=data.self_reflection_notes
    )
    db.add(new_engagement)
    db.commit()
    
    # 2. --- THE AI TRIGGER ---
    student_text = f"Student ID {data.student_id} showed an engagement score of {data.engagement_score}/10 during {data.activity_type}. Teacher notes: {data.self_reflection_notes}."
    
    ai_intervention = run_ai_analysis(student_text)
    
    return {
        "status": "success", 
        "message": f"Permanently saved {data.activity_type} engagement for student {data.student_id}",
        "ai_analysis": ai_intervention
    }