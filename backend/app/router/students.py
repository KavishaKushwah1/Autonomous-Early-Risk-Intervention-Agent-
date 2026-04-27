from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.student import (
    Student, AcademicRecord, Attendance, Activity, LibraryVisit, LearningStreak
)
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/api/students", tags=["Students"])

# --- Schemas ---
class StudentCreate(BaseModel):
    name: str
    roll_number: str
    class_section: str
    email: str
    parent_email: Optional[str] = None

class AcademicCreate(BaseModel):
    student_id: str
    subject: str
    score: float
    max_score: float = 100
    exam_type: str
    submitted_on_time: bool = True

class AttendanceCreate(BaseModel):
    student_id: str
    status: str  # present, absent, late
    lms_activity_duration: Optional[int] = None

class ActivityCreate(BaseModel):
    student_id: str
    category: str
    activity_name: str
    achievement: Optional[str] = None

class LibraryCreate(BaseModel):
    student_id: str
    books_borrowed: list
    duration_minutes: int

class StreakCreate(BaseModel):
    student_id: str
    interest_topic: str
    reflection_note: Optional[str] = None

# --- Routes ---
@router.post("/")
def create_student(data: StudentCreate, db: Session = Depends(get_db)):
    student = Student(**data.model_dump())
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

@router.get("/")
def get_all_students(db: Session = Depends(get_db)):
    return db.query(Student).all()

@router.get("/{student_id}")
def get_student(student_id: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.post("/academic")
def add_academic_record(data: AcademicCreate, db: Session = Depends(get_db)):
    record = AcademicRecord(**data.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.get("/{student_id}/academic")
def get_academic_records(student_id: str, db: Session = Depends(get_db)):
    return db.query(AcademicRecord).filter(AcademicRecord.student_id == student_id).all()

@router.post("/attendance")
def mark_attendance(data: AttendanceCreate, db: Session = Depends(get_db)):
    record = Attendance(**data.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.get("/{student_id}/attendance")
def get_attendance(student_id: str, db: Session = Depends(get_db)):
    return db.query(Attendance).filter(Attendance.student_id == student_id).all()

@router.post("/activity")
def add_activity(data: ActivityCreate, db: Session = Depends(get_db)):
    activity = Activity(**data.model_dump())
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity

@router.post("/library")
def add_library_visit(data: LibraryCreate, db: Session = Depends(get_db)):
    visit = LibraryVisit(**data.model_dump())
    db.add(visit)
    db.commit()
    db.refresh(visit)
    return visit

@router.post("/streak")
def update_streak(data: StreakCreate, db: Session = Depends(get_db)):
    streak = db.query(LearningStreak).filter(
        LearningStreak.student_id == data.student_id,
        LearningStreak.interest_topic == data.interest_topic
    ).first()
    if streak:
        streak.streak_days += 1
        streak.last_activity_date = datetime.now()
        if data.reflection_note:
            streak.reflection_note = data.reflection_note
    else:
        streak = LearningStreak(**data.model_dump(), streak_days=1)
        db.add(streak)
    db.commit()
    db.refresh(streak)
    return streak