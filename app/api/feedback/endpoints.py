from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.deps import get_current_user, get_db
from app.models.schema import Feedback

router = APIRouter()

class FeedbackRequest(BaseModel):
    query: str
    answer: str
    score: int  # 1 or -1

@router.post("/")
async def submit_feedback(
    feedback: FeedbackRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    db_feedback = Feedback(
        query=feedback.query,
        answer=feedback.answer,
        score=feedback.score,
        user_id=current_user.id
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return {"message": "Feedback submitted successfully", "id": db_feedback.id}
