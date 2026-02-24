# app/api/reviews.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Annotated

from app.db.session import get_db
from app.schemas.user import User, Token
from app.crud import user as crud_user
from app.core.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.token import revoke_token as denylist_revoke_token

from app.api.notice import check_valid_user, get_user_clearance
    
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token/")           # define the OAuth2 scheme for token authentication
router = APIRouter(
    prefix="/user",
    tags=["user"],
)

@router.post("/create", response_model=User, summary="create a new user")
async def add_user(username: str, password: str, clearance: str, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """create a new user"""
    user = check_valid_user(token, db)                                  # check if logged in user exists
    user_clearance = get_user_clearance(user, db)                       # get users clearance
    
    if user_clearance != "Officer":                                     # check if user is an officer
        raise HTTPException(status_code=403, detail="insufficient clearance: only officers can create users")

    existing_user = crud_user.get_user_by_username(db, username)        # get any exisiting user with the same username
    if existing_user:                                                   # check if user exists
        raise HTTPException(status_code=409, detail="Username already exists")
    
    if clearance not in ["Officer", "Civilian"]:                        # check if new user clearance level is valid
        raise HTTPException(status_code=400, detail="Invalid clearance level: must be 'Officer' or 'Civilian'")
    
    new_user = crud_user.create_user(db, username, password, clearance) # create new user
    return new_user

@router.post("/token", response_model=Token, summary="provide token")
async def issue_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    """issue a bearer token"""
    user = crud_user.authenticate_user(db, form_data.username, form_data.password)      # get user from database with matching username and password
    
    if not user:                                                                        # check user exists and password is correct
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(user.id)                                         # create tokenr
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES,
    }

@router.put("/token", response_model=Token, summary="refresh token")
async def refresh_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """refresh the current token by revoking the old one and issuing a new one"""
    user = check_valid_user(token, db)                                                  # check if logged in user still exists
    access_token = create_access_token(user.id)                                         # create new token              
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES,
    }

@router.delete("/token", summary="revoke token")
async def revoke_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """revoke current bearer token"""
    #user = check_valid_user(token, db) # dont need to check if user exists since the token is being revoked anyway right?
    
    denylist_revoke_token(token)                                                        # add token to denylist
    
    return {"message": "Token revoked successfully"} 