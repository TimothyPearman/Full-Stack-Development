# app/schemas/review.py
from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class UserBase(BaseModel):
    Username: str
    Clearance: str

class UserCreate(UserBase):
    """Schema for creating a new user."""
    pass

class User(UserBase):
    """Schema returned by the API for a user."""
    id: int

    class Config:
        from_attributes = True
