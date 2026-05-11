from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User as UserModel
# schemas not required in this module

def authenticate_user(db: Session, username: str, password: str):
    """authenticate a user by username and password"""
    user_obj = get_user_by_username(db, username)   # retrieve user from database

    if user_obj is None:                # check if user exists
        return None

    # use getattr to avoid static analysis issues when attribute types are SQLAlchemy columns
    if getattr(user_obj, "password", None) != password:   # check if password matches
        return None

    return user_obj

def get_user_by_username(db: Session, username: str):
    """return a user by username"""
    return db.query(UserModel).filter(UserModel.Username == username).first()   # retrieve user record from the database by username

def create_user(
    db: Session,
    username: str,
    password: str,
    clearance: str,
    fullName: Optional[str] = None,
    dateOfBirth: Optional[str] = None,
    currentAddress: Optional[str] = None,
    driverLicenseNumber: Optional[str] = None,
    postcode: Optional[str] = None,
    nationalInsurance: Optional[str] = None,
    vehicleRegNumber: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
):
    """create a new user"""
    user = UserModel(
        Username=username,
        password=password,
        Clearance=clearance,
        FullName=fullName,
        DateOFBirth=dateOfBirth,
        CurrentAddress=currentAddress,
        LicenseNumber=driverLicenseNumber,
        licensePostcode=postcode,
        NationalInsuranceNumber=nationalInsurance,
        RegistrationNumber=vehicleRegNumber,
        Email=email,
        PhoneNumber=phone
    )
    
    db.add(user)        # add new user to database session
    db.commit()         # commit transaction to save new user to database
    db.refresh(user)    # refresh user object to get new id from database
    
    return user         # return newly created user object

def update_user_contact_info(db: Session, user_id: int, email: str = "", phone: str = ""):
    """update a user's email and/or phone number"""
    user_obj = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not user_obj:
        return None

    if email is not None:
        setattr(user_obj, "Email", email)

    if phone is not None:
        setattr(user_obj, "PhoneNumber", phone)

    db.commit()
    db.refresh(user_obj)

    return user_obj