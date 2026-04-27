from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.student import Student, AcademicRecord, Attendance, Activity, LibraryVisit, LearningStreak
from app.models.teacher import AnonymousFeedback
from datetime import datetime, timedelta
import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

router = APIRouter(prefix="/api/ai", tags=["AI Agent"])

def collect_student_context(student_id: str, db: Session) -> dict:
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        return None

    since = datetime.now() - timedelta(days=90)

    academics = db.query(AcademicRecord).filter(
        AcademicRecord.student_id == student_id
    ).all()

    attendance = db.query(Attendance).filter(
        Attendance.student_id == student_id
    ).all()

    activities = db.query(Activity).filter(
        Activity.student_id == student_id
    ).all()

    library = db.query(LibraryVisit).filter(
        LibraryVisit.student_id == student_id
    ).all()

    streaks = db.query(LearningStreak).filter(
        LearningStreak.student_id == student_id
    ).all()

    total_days = len(attendance)
    present_days = sum(1 for a in attendance if a.status == "present")
    attendance_pct = round((present_days / total_days * 100), 1) if total_days > 0 else 0
    avg_score = round(sum(r.score for r in academics) / len(academics), 1) if academics else 0
    late_submissions = sum(1 for r in academics if not r.submitted_on_time)

    return {
        "student_name": student.name,
        "class": student.class_section,
        "attendance_percentage": attendance_pct,
        "total_days_recorded": total_days,
        "academic_average": avg_score,
        "late_submissions": late_submissions,
        "subject_scores": [
            {"subject": r.subject, "score": r.score, "max": r.max_score, "exam_type": r.exam_type}
            for r in academics
        ],
        "non_academic_activities": [
            {"category": a.category, "name": a.activity_name, "achievement": a.achievement}
            for a in activities
        ],
        "library_visits": len(library),
        "books_borrowed": [b for v in library for b in (v.books_borrowed or [])],
        "learning_streaks": [
            {"topic": s.interest_topic, "days": s.streak_days, "reflection": s.reflection_note}
            for s in streaks
        ]
    }

@router.get("/student/{student_id}/recommendations")
async def get_recommendations(student_id: str, db: Session = Depends(get_db)):
    context = collect_student_context(student_id, db)
    if not context:
        raise HTTPException(status_code=404, detail="Student not found")

    prompt = f"""
You are an expert educational AI agent. Analyze this student profile and respond with JSON only.

STUDENT DATA:
{json.dumps(context, indent=2)}

Return this exact JSON structure:
{{
  "overall_assessment": "2-3 sentence summary",
  "strengths": ["strength1", "strength2", "strength3"],
  "areas_of_concern": ["concern1", "concern2"],
  "academic_recommendations": ["tip1", "tip2", "tip3"],
  "wellbeing_observations": "one sentence",
  "risk_level": "low or medium or high",
  "risk_reason": "why this risk level",
  "predicted_trajectory": "improving or stable or declining",
  "suggested_interventions": ["action1", "action2"],
  "parent_message": "warm 2-3 sentence message for parents",
  "teacher_alert": "what teacher should watch for"
}}

Be specific. Use actual numbers from the data. Return ONLY valid JSON.
"""
    try:
        response = model.generate_content(prompt)
        raw = response.text.strip()
        if "```" in raw:
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return {"status": "success", "data": json.loads(raw)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/student/{student_id}/parent-report")
async def get_parent_report(student_id: str, month: int, year: int, db: Session = Depends(get_db)):
    context = collect_student_context(student_id, db)
    if not context:
        raise HTTPException(status_code=404, detail="Student not found")

    prompt = f"""
Write a monthly parent report for {month}/{year}.

Student data:
{json.dumps(context, indent=2)}

Write a professional, warm letter covering:
1. Academic performance with subject highlights
2. Attendance and punctuality
3. Non-academic participation
4. Library and self-learning
5. Areas needing home support
6. Overall encouragement

Start with "Dear Parent/Guardian,". 300-400 words. No bullet points.
"""
    try:
        response = model.generate_content(prompt)
        return {"status": "success", "report": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/teacher/{teacher_id}/feedback-analysis")
async def get_feedback_analysis(teacher_id: str, db: Session = Depends(get_db)):
    feedbacks = db.query(AnonymousFeedback).filter(
        AnonymousFeedback.teacher_id == teacher_id
    ).all()

    if not feedbacks:
        return {"status": "success", "message": "No feedback submitted yet"}

    avg_rating = round(sum(f.rating for f in feedbacks) / len(feedbacks), 1)
    texts = [f.feedback_text for f in feedbacks]

    prompt = f"""
Analyze anonymous student feedback for a teacher.

Total feedback: {len(feedbacks)}
Average rating: {avg_rating}/5
Comments:
{chr(10).join(f'- {t}' for t in texts)}

Return ONLY this JSON:
{{
  "sentiment_summary": "overall sentiment",
  "key_positives": ["positive1", "positive2", "positive3"],
  "key_concerns": ["concern1", "concern2"],
  "teaching_style_observation": "brief observation",
  "actionable_suggestions": ["suggestion1", "suggestion2", "suggestion3"],
  "admin_note": "summary for administration"
}}
"""
    try:
        response = model.generate_content(prompt)
        raw = response.text.strip()
        if "```" in raw:
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return {"status": "success", "avg_rating": avg_rating, "analysis": json.loads(raw)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))