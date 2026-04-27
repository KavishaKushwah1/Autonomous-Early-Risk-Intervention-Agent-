class PrivateMessage(Base):
    __tablename__ = "private_messages"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    sender_id = Column(String)
    receiver_id = Column(String)
    sender_role = Column(String(10))  # "student" or "teacher"
    content = Column(Text)
    sent_at = Column(DateTime)
    is_read = Column(Boolean, default=False)

class AnonymousFeedback(Base):
    __tablename__ = "anonymous_feedback"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    teacher_id = Column(String, ForeignKey("teachers.id"))
    feedback_text = Column(Text)
    rating = Column(Integer)  # 1-5
    # Note: NO student_id — fully anonymous
    submitted_at = Column(DateTime)
    sentiment = Column(String(10), nullable=True)  # filled by AI