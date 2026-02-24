# app/schemas/review.py
from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    """schema for the token response when a user logs in"""
    access_token: str
    token_type: str
    expires_in: int

class UserBase(BaseModel):
    """base schema for a user"""
    Username: str
    Clearance: str

class User(UserBase):
    """schema returned by the API for a user"""
    id: int

    class Config:
        from_attributes = True
