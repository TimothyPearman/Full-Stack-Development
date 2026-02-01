# app/models/review.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Review(Base):
    """SQLAlchemy model for the 'reviews' table."""
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    notice_id = Column(Integer, ForeignKey("Notice.NoticeID"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String(500), nullable=True)

    # Relationship to the Notice model (notice.reviews gives all reviews for a notice).
    notice = relationship("Notice", backref="reviews")
