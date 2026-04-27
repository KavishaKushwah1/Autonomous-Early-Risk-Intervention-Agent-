from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.teacher import Teacher, AnonymousFeedback, PrivateMessage
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/api/teachers", tags=["Teachers"])

class TeacherCreate(BaseModel):
    name: str
    email: str
    subject: str

class FeedbackCreate(BaseModel):
    teacher_id: str
    feedback_text: str
    rating: int

class MessageCreate(BaseModel):
    sender_id: str
    receiver_id: str
    teacher_id: str
    sender_role: str
    content: str

@router.post("/")
def create_teacher(data: TeacherCreate, db: Session = Depends(get_db)):
    teacher = Teacher(**data.model_dump())
    db.add(teacher)
    db.commit()
    db.refresh(teacher)
    return teacher

@router.get("/")
def get_all_teachers(db: Session = Depends(get_db)):
    return db.query(Teacher).all()

@router.get("/{teacher_id}")
def get_teacher(teacher_id: str, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher

@router.post("/feedback")
def submit_feedback(data: FeedbackCreate, db: Session = Depends(get_db)):
    feedback = AnonymousFeedback(**data.model_dump())
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return {"message": "Feedback submitted anonymously"}

@router.get("/{teacher_id}/feedback")
def get_feedback(teacher_id: str, db: Session = Depends(get_db)):
    return db.query(AnonymousFeedback).filter(
        AnonymousFeedback.teacher_id == teacher_id
    ).all()

@router.post("/message")
def send_message(data: MessageCreate, db: Session = Depends(get_db)):
    msg = PrivateMessage(**data.model_dump())
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg

@router.get("/messages/{teacher_id}")
def get_messages(teacher_id: str, db: Session = Depends(get_db)):
    return db.query(PrivateMessage).filter(
        PrivateMessage.teacher_id == teacher_id
    ).all()