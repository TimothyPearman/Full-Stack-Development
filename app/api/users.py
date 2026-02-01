# app/api/users.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.user import User, UserCreate
from app.crud import user as crud_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("/", response_model=List[User], summary="List all users")
async def list_users(db: Session = Depends(get_db)):
    """Get all users from the database."""
    return crud_user.get_users(db)

@router.post("/", response_model=User, status_code=201, summary="Create a user")
async def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """Create a new user."""
    return crud_user.create_user(db, user_in)
