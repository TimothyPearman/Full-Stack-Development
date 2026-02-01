# app/schemas/review.py
from pydantic import BaseModel
from typing import Optional

class ReviewBase(BaseModel):
    notice_id: int
    rating: int
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    """Schema for creating a new review."""
    pass

class Review(ReviewBase):
    """Schema returned by the API for a review."""
    id: int

    class Config:
        from_attributes = True
