from sqlalchemy import Column, Integer, String, Float
from database import Base

class DBStudent(Base):
    __tablename__ = "students"

    student_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    grade_level = Column(Integer)
    interest_goals = Column(String)