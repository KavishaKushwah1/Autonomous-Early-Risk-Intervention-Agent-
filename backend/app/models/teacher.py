from sqlalchemy import Column, String, DateTime, Text, Integer, ForeignKey
from app.database import Base
from datetime import datetime
import uuid

def gen_uuid():
    return str(uuid.uuid4())

class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(String, primary_key=True, default=gen_uuid)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True)
    subject = Column(String(50))
    created_at = Column(DateTime, default=datetime.now)

class AnonymousFeedback(Base):
    __tablename__ = "anonymous_feedback"
    id = Column(String, primary_key=True, default=gen_uuid)
    teacher_id = Column(String, ForeignKey("teachers.id"))
    feedback_text = Column(Text)
    rating = Column(Integer)
    submitted_at = Column(DateTime, default=datetime.now)
    sentiment = Column(String(10), nullable=True)

class PrivateMessage(Base):
    __tablename__ = "private_messages"
    id = Column(String, primary_key=True, default=gen_uuid)
    sender_id = Column(String)
    receiver_id = Column(String)
    teacher_id = Column(String, ForeignKey("teachers.id"))
    sender_role = Column(String(10))
    content = Column(Text)
    sent_at = Column(DateTime, default=datetime.now)
    is_read = Column(String(5), default="false")