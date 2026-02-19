# app/crud/user.py
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User as UserModel
from app.schemas import user
from app.schemas.user import UserCreate

def authenticate_user(db: Session, username: str, password: str):
    """Authenticate a user by username and password. Returns user if valid, None otherwise."""
    user = db.query(UserModel).filter(UserModel.Username == username).first() # check the database for a user with the given username
    if not user:
        return None # no user with that username exists
    if user.password != password:
        return None # password does not match
    return user

def get_user_by_username(db: Session, username: str):
    """Return a user by username, or None if not found."""
    return db.query(UserModel).filter(UserModel.Username == username).first() # query the database for a user with the given username and return it, or None if not found

def create_user(db: Session, username: str, password: str, clearance: str):
    """Create a new user"""
    user = UserModel(Username=username, password=password, Clearance=clearance) # create a new user object with the given username, password, and clearance level
    db.add(user) # add the new user to the database session
    db.commit() # commit the transaction to save the new user to the database
    db.refresh(user) # refresh the user object to get the new id from the database
    return user # return the newly created user object

#def get_users(db: Session):
#    """Return all notices for a users."""
#    return db.query(UserModel).all()
#
#def get_user_by_id(db: Session, user_id: int):
#    """Return a user by ID, or None if not found."""
#    return db.query(UserModel).filter(UserModel.id == user_id).first()
#def create_user(db: Session, user_in: UserCreate):
#    """Create a new user."""
#    user = UserModel(
#        username=user_in.username,
#        password=user_in.password,
#
#    )
#    db.add(user)
#    db.commit()
#    db.refresh(user)
#    return user
#
#def get_user_by_username(db: Session, username: str):
#    """Return a user by username, or None if not found."""
#    return db.query(UserModel).filter(UserModel.username == username).first()
#
#
#def authenticate_user(db: Session, username: str, password: str):
#    """Authenticate a user by username and password. Returns user if valid, None otherwise."""
#    user = get_user_by_username(db, username)
#    if not user:
#        return None
#    if user.password != password:
#        return None
#    return user
#
#def create_user(db: Session, username: str, password: str):
#    """Create a new user with a hashed password."""
#
#    user = UserModel(username=username, password=password)
#    db.add(user)
#    db.commit()
#    db.refresh(user)
#    return user
