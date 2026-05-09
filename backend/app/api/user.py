# app/api/reviews.py
from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Annotated, Optional

from app.db.session import get_db
from app.schemas.user import User, Token, Clearance, UserRegister
from app.crud import user as crud_user
from app.core.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.token import revoke_token as denylist_revoke_token

from app.api.notice import check_valid_user, get_user_clearance

# Dependency to parse registration form
async def get_user_register_form(
    username: str = Form(),
    password: str = Form(),
    clearance: str = Form(),
    fullName: str = Form(None),
    dateOfBirth: str = Form(None),
    currentAddress: str = Form(None),
    driverLicenseNumber: str = Form(None),
    postcode: str = Form(None),
    nationalInsurance: str = Form(None),
    vehicleRegNumber: str = Form(None),
    email: str = Form(None),
    phone: str = Form(None)
) -> UserRegister:
    """Extract form fields into UserRegister model"""
    return UserRegister(
        username=username,
        password=password,
        clearance=clearance,
        fullName=fullName,
        dateOfBirth=dateOfBirth,
        currentAddress=currentAddress,
        driverLicenseNumber=driverLicenseNumber,
        postcode=postcode,
        nationalInsurance=nationalInsurance,
        vehicleRegNumber=vehicleRegNumber,
        email=email,
        phone=phone
    )
    
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token/")           # define the OAuth2 scheme for token authentication
router = APIRouter(
    prefix="/user",
    tags=["user"],
)

@router.post("/create", response_model=User, summary="create a new user")
async def add_user(form: Annotated[UserRegister, Depends(get_user_register_form)], db: Session = Depends(get_db)):
    """create a new user"""
    #user = check_valid_user(token, db)                                  # check if logged in user exists
    #user_clearance = get_user_clearance(user, db)                       # get users clearance
    
    #if user_clearance != "Officer":                                     # check if user is an officer
    #    raise HTTPException(status_code=403, detail="insufficient clearance: only officers can create users")

    existing_user = crud_user.get_user_by_username(db, form.username)        # get any exisiting user with the same username
    if existing_user:                                                   # check if user exists
        raise HTTPException(status_code=409, detail="Username already exists")
    
    if form.clearance not in ["Officer", "Civilian"]:                        # check if new user clearance level is valid
        raise HTTPException(status_code=400, detail="Invalid clearance level: must be 'Officer' or 'Civilian'")
    
    new_user = crud_user.create_user(
        db, 
        form.username, 
        form.password, 
        form.clearance,
        form.fullName,
        form.dateOfBirth,
        form.currentAddress,
        form.driverLicenseNumber,
        form.postcode,
        form.nationalInsurance,
        form.vehicleRegNumber,
        form.email,
        form.phone
    )
    return new_user

@router.get("/get", response_model=User, summary="get current user profile")
async def get_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """get current user's profile with all fields"""
    user = check_valid_user(token, db)                                                  # check if logged in user still exists
    
    if not user:                                                                        # check user exists
        raise HTTPException(
            status_code=404,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

@router.put("/update", response_model=User, summary="update current user contact information")
async def update_user_contact_info(
    token: str = Depends(oauth2_scheme),
    email: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    """update the authenticated user's email and/or phone number"""
    user = check_valid_user(token, db)

    updated_user = crud_user.update_user_contact_info(db, user.id, email=email, phone=phone)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")

    return updated_user

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
        "clearance": user.Clearance,
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

@router.post("/clearance", response_model=Clearance, summary="get user clearance")
async def get_clearance(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    """get user clearance level by username and password"""
    user = crud_user.authenticate_user(db, form_data.username, form_data.password)      # authenticate user
    
    if not user:                                                                        # check user exists and password is correct
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {
        "clearance": user.Clearance,
    } 