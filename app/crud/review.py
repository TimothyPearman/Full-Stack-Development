# app/crud/review.py
from sqlalchemy.orm import Session
from app.models.review import Review as ReviewModel
from app.schemas.review import ReviewCreate

def get_reviews_for_notice(db: Session, notice_id: int):
    """Return all reviews for a given notice."""
    return db.query(ReviewModel).filter(ReviewModel.notice_id == notice_id).all()

def create_review(db: Session, review_in: ReviewCreate):
    """Create a new review for a notice."""
    review = ReviewModel(
        notice_id=review_in.notice_id,
        rating=review_in.rating,
        comment=review_in.comment,
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review
