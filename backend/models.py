from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Model for the Academic Data
class AcademicRecord(BaseModel):
    student_id: int
    subject: str
    score: float
    assessment_type: str  # e.g., 'Quiz', 'Final', 'Homework'

# Model for the Non-Academic/Behavioral Data
class BehavioralEngagement(BaseModel):
    student_id: int
    activity_type: str    # e.g., 'Forum Post', 'Extracurricular'
    engagement_score: int # 1-10 scale
    self_reflection_notes: Optional[str] = None # Optional, since not every action has a reflection