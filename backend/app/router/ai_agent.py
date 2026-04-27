from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.ai_agent_service import (
    generate_student_recommendations,
    generate_monthly_parent_report,
    analyze_anonymous_feedback
)

router = APIRouter(prefix="/api/ai", tags=["AI Agent"])

@router.get("/student/{student_id}/recommendations")
async def get_student_recommendations(student_id: str, db: Session = Depends(get_db)):
    """AI-powered full student analysis and recommendations."""
    try:
        result = await generate_student_recommendations(student_id, db)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/student/{student_id}/parent-report")
async def get_parent_report(student_id: str, month: int, year: int, db: Session = Depends(get_db)):
    """Generate monthly parent performance letter."""
    report = await generate_monthly_parent_report(student_id, month, year, db)
    return {"status": "success", "report": report}

@router.get("/teacher/{teacher_id}/feedback-analysis")
async def get_feedback_analysis(teacher_id: str, db: Session = Depends(get_db)):
    """Analyze anonymous student feedback for a teacher."""
    result = await analyze_anonymous_feedback(teacher_id, db)
    return {"status": "success", "analysis": result}

@router.post("/student/{student_id}/feedback")
async def submit_anonymous_feedback(
    teacher_id: str,
    feedback_text: str,
    rating: int,
    db: Session = Depends(get_db)
):
    """Submit anonymous feedback — no student ID stored."""
    feedback = AnonymousFeedback(
        teacher_id=teacher_id,
        feedback_text=feedback_text,
        rating=rating,
        submitted_at=datetime.now()
    )
    db.add(feedback)
    db.commit()
    return {"status": "submitted", "message": "Your feedback is anonymous and submitted."}