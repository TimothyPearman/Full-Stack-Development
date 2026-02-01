# app/crud/user.py
from sqlalchemy.orm import Session
from app.models.user import User as UserModel
from app.schemas.user import UserCreate

def get_users(db: Session):
    """Return all users."""
    return db.query(UserModel).all()

def create_user(db: Session, user_in: UserCreate):
    """Create a new user."""
    user = UserModel(name=user_in.name, email=user_in.email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
