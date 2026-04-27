import google.generativeai as genai
from app.config import settings
from app.models.student import Student, AcademicRecord, Attendance, Activity
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import json

genai.configure(api_key=settings.GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

def collect_student_context(student_id: str, db: Session) -> dict:
    """Gather all data for a student into one context object."""
    student = db.query(Student).filter(Student.id == student_id).first()
    
    # Academic records - last 90 days
    since = datetime.now() - timedelta(days=90)
    academics = db.query(AcademicRecord).filter(
        AcademicRecord.student_id == student_id,
        AcademicRecord.exam_date >= since
    ).all()
    
    attendance = db.query(Attendance).filter(
        Attendance.student_id == student_id,
        Attendance.date >= since
    ).all()
    
    activities = db.query(Activity).filter(
        Activity.student_id == student_id
    ).all()
    
    library = db.query(LibraryVisit).filter(
        LibraryVisit.student_id == student_id
    ).all()
    
    # Calculate metrics
    total_days = len(attendance)
    present_days = sum(1 for a in attendance if a.status == "present")
    attendance_pct = (present_days / total_days * 100) if total_days > 0 else 0
    
    avg_score = sum(r.score for r in academics) / len(academics) if academics else 0
    late_submissions = sum(1 for r in academics if not r.submitted_on_time)
    
    return {
        "student_name": student.name,
        "class": student.class_section,
        "attendance_percentage": round(attendance_pct, 1),
        "academic_average": round(avg_score, 1),
        "late_submissions": late_submissions,
        "subject_scores": [
            {"subject": r.subject, "score": r.score, "exam": r.exam_type}
            for r in academics
        ],
        "non_academic_activities": [
            {"category": a.category, "name": a.activity_name, "achievement": a.achievement}
            for a in activities
        ],
        "library_visits_count": len(library),
        "books_read": [b for v in library for b in (v.books_borrowed or [])],
    }

async def generate_student_recommendations(student_id: str, db: Session) -> dict:
    """Main AI agent function — reasons over student data and returns insights."""
    context = collect_student_context(student_id, db)
    
    prompt = f"""
You are an expert educational AI agent. Analyze this student's complete profile and provide 
structured recommendations. Think step by step before answering.

STUDENT DATA:
{json.dumps(context, indent=2)}

Your task — provide a JSON response with these exact keys:

{{
  "overall_assessment": "2-3 sentence summary of student's current standing",
  "strengths": ["list of 3 genuine strengths based on data"],
  "areas_of_concern": ["list of specific concerns with evidence from data"],
  "academic_recommendations": ["3-5 specific, actionable academic tips"],
  "wellbeing_observations": "note on balance between academic and non-academic life",
  "risk_level": "low | medium | high",
  "risk_reason": "if medium or high risk, explain why clearly",
  "parent_message": "warm, encouraging 3-sentence message for parents",
  "teacher_alert": "if risk is medium/high, what should teacher pay attention to",
  "predicted_trajectory": "improving | stable | declining",
  "suggested_interventions": ["specific steps school should take if any"]
}}

Be specific. Reference actual numbers from the data. Do not give generic advice.
Respond ONLY with valid JSON, no markdown formatting.
"""
    
    response = model.generate_content(prompt)
    
    # Parse JSON from response
    raw = response.text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    
    return json.loads(raw)

async def generate_monthly_parent_report(student_id: str, month: int, year: int, db: Session) -> str:
    """Generate a complete monthly parent summary letter."""
    context = collect_student_context(student_id, db)
    
    prompt = f"""
You are writing a monthly student performance summary for parents.

Student data for {month}/{year}:
{json.dumps(context, indent=2)}

Write a professional, warm, and honest parent report covering:
1. Academic performance summary with subject-wise highlights
2. Attendance and punctuality observations
3. Non-academic participation and achievements
4. Library and self-learning activity
5. Areas needing parental support at home
6. Overall encouragement and next month's focus

Tone: Warm, professional, honest. Not overly positive or negative.
Length: 300-400 words. Use clear paragraphs, no bullet points.
Address the parent directly as "Dear Parent/Guardian".
"""
    
    response = model.generate_content(prompt)
    return response.text

async def analyze_anonymous_feedback(teacher_id: str, db: Session) -> dict:
    """Aggregate and analyze anonymous student feedback for a teacher."""
    feedbacks = db.query(AnonymousFeedback).filter(
        AnonymousFeedback.teacher_id == teacher_id
    ).all()
    
    if not feedbacks:
        return {"message": "No feedback yet"}
    
    feedback_texts = [f.feedback_text for f in feedbacks]
    avg_rating = sum(f.rating for f in feedbacks) / len(feedbacks)
    
    prompt = f"""
Analyze these anonymous student feedback comments for a teacher.

Feedback count: {len(feedbacks)}
Average rating: {avg_rating:.1f}/5

Comments:
{chr(10).join(f'- {text}' for text in feedback_texts)}

Return JSON with:
{{
  "sentiment_summary": "overall sentiment analysis",
  "key_positives": ["top 3 things students appreciate"],
  "key_concerns": ["top 3 areas students want improvement"],
  "teaching_style_observation": "brief professional observation",
  "actionable_suggestions": ["3 concrete improvements"],
  "admin_note": "summary for school administration"
}}

Be constructive and professional. Respond ONLY with valid JSON.
"""
    
    response = model.generate_content(prompt)
    raw = response.text.strip().lstrip("```json").rstrip("```")
    return json.loads(raw)