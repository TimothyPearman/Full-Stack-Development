# app/schemas/user.py
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    """Schema for creating a new user."""
    pass

class User(UserBase):
    """Schema returned by the API for a user."""
    id: int

    class Config:
        from_attributes = True
