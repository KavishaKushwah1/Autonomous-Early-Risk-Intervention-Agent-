from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from models import AcademicRecord, BehavioralEngagement
import db_models
from database import engine, Base, SessionLocal
from agent import run_ai_analysis 
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

# --- 1. ADD THIS LINE ---
from fastapi.middleware.cors import CORSMiddleware

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Autonomous Early Risk Intervention Agent API",
    version="1.0.0"
)

# --- 2. ADD THIS WHOLE BLOCK ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to open and close the database connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ... (Keep your @app.get and @app.post routes down here exactly as they are!) ...


@app.get("/")
def read_root():
    return {"message": "Welcome to the Autonomous Education Agent API! Server is running smoothly."}

@app.post("/api/v1/observe/academic")
def record_academic_data(data: AcademicRecord, db: Session = Depends(get_db)):
    # 1. Save the new grade to Database
    new_record = db_models.DBAcademicRecord(
        student_id=data.student_id,
        subject=data.subject,
        score=data.score,
        assessment_type=data.assessment_type
    )
    db.add(new_record)
    db.commit()
    
    # 2. --- NEW: FETCH BOTH ACADEMIC AND BEHAVIORAL HISTORY ---
    past_academic = db.query(db_models.DBAcademicRecord).filter(db_models.DBAcademicRecord.student_id == data.student_id).all()
    past_behavior = db.query(db_models.DBBehavioralEngagement).filter(db_models.DBBehavioralEngagement.student_id == data.student_id).all()
    
    # 3. --- NEW: BUILD THE ULTIMATE HOLISTIC PROMPT ---
    ai_prompt = f"Recent update: Student ID {data.student_id} just scored {data.score}% on their {data.subject} {data.assessment_type}.\n\n"
    ai_prompt += "Here is the student's complete academic and behavioral history for context:\n\n"
    
    ai_prompt += "ACADEMIC HISTORY:\n"
    for record in past_academic:
        ai_prompt += f"- {record.subject} ({record.assessment_type}): {record.score}%\n"
        
    ai_prompt += "\nBEHAVIORAL HISTORY:\n"
    if past_behavior:
        for record in past_behavior:
            ai_prompt += f"- {record.activity_type}: Engagement Score {record.engagement_score}/10. Notes: {record.self_reflection_notes}\n"
    else:
        ai_prompt += "- No behavioral records found yet.\n"
        
    ai_prompt += "\nBased on this student's combined academic and behavioral history, please provide a holistic early risk intervention plan."
    
    # 4. --- THE AI TRIGGER ---
    ai_intervention = run_ai_analysis(ai_prompt)
    
    return {
        "status": "success", 
        "message": f"Permanently saved {data.subject} score for student {data.student_id}",
        "ai_analysis": ai_intervention 
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
# ==========================================
# PHASE 2: GET ROUTE TO VIEW PAST RECORDS
# ==========================================
@app.get("/api/v1/students/{student_id}")
def get_student_history(student_id: int, db: Session = Depends(get_db)):
    """Fetch all academic AND behavioral records for a specific student."""
    
    # 1. Fetch both types of records from the database
    academic_records = db.query(db_models.DBAcademicRecord).filter(db_models.DBAcademicRecord.student_id == student_id).all()
    behavioral_records = db.query(db_models.DBBehavioralEngagement).filter(db_models.DBBehavioralEngagement.student_id == student_id).all()
    
    # 2. If the student doesn't exist in either table, throw an error
    if not academic_records and not behavioral_records:
        raise HTTPException(status_code=404, detail=f"No records found for Student ID {student_id}")
    
    # 3. Send both lists back in the JSON response
    return {
        "status": "success", 
        "student_id": student_id, 
        "academic_history": academic_records,
        "behavioral_history": behavioral_records
    }
# ==========================================
# PHASE 3: CUSTOM ERROR HANDLING
# ==========================================
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """Catches bad data formats and returns a friendly error message."""
    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "message": "Oops! The data sent to the server is missing or in the wrong format. Please ensure IDs are numbers and text fields are not empty.",
            "developer_details": exc.errors() # Keeps the exact error for debugging!
        },
    )