from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User as UserModel
from app.schemas import user

def authenticate_user(db: Session, username: str, password: str):
    """authenticate a user by username and password"""
    user = get_user_by_username(db, username)   # retrieve user from database
    
    if not user:                    # check if user exists
        return None
    
    if user.password != password:   # check if password matches
        return None
    
    return user

def get_user_by_username(db: Session, username: str):
    """return a user by username"""
    return db.query(UserModel).filter(UserModel.Username == username).first()   # retrieve user record from the database by username

def create_user(db: Session, username: str, password: str, clearance: str):
    """create a new user"""
    user = UserModel(Username=username, password=password, Clearance=clearance) # create a new user object with the given username, password, and clearance level
    
    db.add(user)        # add new user to database session
    db.commit()         # commit transaction to save new user to database
    db.refresh(user)    # refresh user object to get new id from database
    
    return user         # return newly created user object