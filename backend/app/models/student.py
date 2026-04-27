from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.database import Base
import uuid
from datetime import datetime

def gen_uuid():
    return str(uuid.uuid4())

class Student(Base):
    __tablename__ = "students"
    id = Column(String, primary_key=True, default=gen_uuid)
    name = Column(String(100), nullable=False)
    roll_number = Column(String(20), unique=True)
    class_section = Column(String(10))
    email = Column(String(150), unique=True)
    parent_email = Column(String(150))
    created_at = Column(DateTime, default=datetime.now)

    academic_records = relationship("AcademicRecord", back_populates="student")
    attendance_records = relationship("Attendance", back_populates="student")
    activities = relationship("Activity", back_populates="student")
    library_visits = relationship("LibraryVisit", back_populates="student")
    learning_streaks = relationship("LearningStreak", back_populates="student")

class AcademicRecord(Base):
    __tablename__ = "academic_records"
    id = Column(String, primary_key=True, default=gen_uuid)
    student_id = Column(String, ForeignKey("students.id"))
    subject = Column(String(50))
    score = Column(Float)
    max_score = Column(Float, default=100)
    exam_type = Column(String(30))
    exam_date = Column(DateTime, default=datetime.now)
    submitted_on_time = Column(Boolean, default=True)
    student = relationship("Student", back_populates="academic_records")

class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(String, primary_key=True, default=gen_uuid)
    student_id = Column(String, ForeignKey("students.id"))
    date = Column(DateTime, default=datetime.now)
    status = Column(String(10))
    lms_login_time = Column(DateTime, nullable=True)
    lms_activity_duration = Column(Integer, nullable=True)
    student = relationship("Student", back_populates="attendance_records")

class Activity(Base):
    __tablename__ = "activities"
    id = Column(String, primary_key=True, default=gen_uuid)
    student_id = Column(String, ForeignKey("students.id"))
    category = Column(String(20))
    activity_name = Column(String(100))
    achievement = Column(String(200), nullable=True)
    participation_date = Column(DateTime, default=datetime.now)
    student = relationship("Student", back_populates="activities")

class LibraryVisit(Base):
    __tablename__ = "library_visits"
    id = Column(String, primary_key=True, default=gen_uuid)
    student_id = Column(String, ForeignKey("students.id"))
    visit_date = Column(DateTime, default=datetime.now)
    books_borrowed = Column(JSON)
    duration_minutes = Column(Integer)
    student = relationship("Student", back_populates="library_visits")

class LearningStreak(Base):
    __tablename__ = "learning_streaks"
    id = Column(String, primary_key=True, default=gen_uuid)
    student_id = Column(String, ForeignKey("students.id"))
    interest_topic = Column(String(100))
    streak_days = Column(Integer, default=0)
    reflection_note = Column(Text, nullable=True)
    last_activity_date = Column(DateTime, default=datetime.now)
    student = relationship("Student", back_populates="learning_streaks")