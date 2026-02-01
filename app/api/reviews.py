# app/api/reviews.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.review import Review, ReviewCreate
from app.crud import review as crud_review

router = APIRouter(
    prefix="/reviews",
    tags=["reviews"],
)

@router.get("/notice/{notice_id}", response_model=List[Review], summary="List reviews for a notice")
async def list_reviews_for_notice(notice_id: int, db: Session = Depends(get_db)):
    """Get all reviews for a specific notice."""
    return crud_review.get_reviews_for_notice(db, notice_id)

@router.post("/", response_model=Review, status_code=201, summary="Create a review")
async def create_review(review_in: ReviewCreate, db: Session = Depends(get_db)):
    """Create a new review for a notice."""
    return crud_review.create_review(db, review_in)
