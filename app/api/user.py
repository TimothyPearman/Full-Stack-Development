# app/api/reviews.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Annotated

from app.db.session import get_db
from app.schemas.user import User, UserCreate, Token
from app.crud import user as crud_user

from app.api.notice import check_valid_user, check_user_clearance
    
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token/")

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

@router.post("/user/create", response_model=User, summary="create a new user")
async def add_user(username: str, password: str, clearance: str, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """create a new user"""
    # check if logged in user is an officer
    user = check_valid_user(token, db)
    user_clearance = check_user_clearance(user, db) # check the users clearance level to see if they are allowed to create a notice
    if user_clearance != "Officer":
        raise HTTPException(status_code=403, detail="insufficient clearance: only officers can create users")

    # check if new user username already exists
    existing_user = crud_user.get_user_by_username(db, username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # check if new user clearance level is valid
    if clearance not in ["Officer", "Civilian"]:
        raise HTTPException(status_code=400, detail="Invalid clearance level: must be 'Officer' or 'Civilian'")
    
    new_user = crud_user.create_user(db, username, password, clearance)
    return new_user


@router.post("/token/", response_model=Token, summary="provide token")
async def issue_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    """Issue a bearer token using username/password form data.
    Authenticates against the users table in the database."""
    user = crud_user.authenticate_user(db, form_data.username, form_data.password)      # see if user exists and password is correct
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = f"token-{user.id}"                                                   # if valid user, create a token with their user id
    return {"access_token": access_token, "token_type": "bearer"}                       # return the token to the client

@router.put("/token/", summary="refresh token")
async def refresh_token(db: Session = Depends(get_db)):
    pass

@router.delete("/token", summary="revoke token")
async def revoke_token(db: Session = Depends(get_db)):
    pass