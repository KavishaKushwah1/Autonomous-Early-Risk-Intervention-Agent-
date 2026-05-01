from sqlalchemy import Column, Integer, String, Float
from database import Base

class DBStudent(Base):
    __tablename__ = "students"

    student_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    grade_level = Column(Integer)
    interest_goals = Column(String)

class DBAcademicRecord(Base):
    __tablename__ = "academic_records"
    
    record_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, index=True)
    subject = Column(String, index=True)
    score = Column(Float)
    assessment_type = Column(String)

class DBBehavioralEngagement(Base):
    __tablename__ = "behavioral_engagement"
    
    engagement_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, index=True)
    activity_type = Column(String)
    engagement_score = Column(Integer)
    self_reflection_notes = Column(String, nullable=True)