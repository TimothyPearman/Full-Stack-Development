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

def create_user(db: Session, username: str, password: str, clearance: str, 
                fullName: str = None, dateOfBirth: str = None, currentAddress: str = None,
                driverLicenseNumber: str = None, postcode: str = None, 
                nationalInsurance: str = None, vehicleRegNumber: str = None,
                email: str = None, phone: str = None):
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

def update_user_contact_info(db: Session, user_id: int, email: str = None, phone: str = None):
    """update a user's email and/or phone number"""
    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not user:
        return None

    if email is not None:
        user.Email = email

    if phone is not None:
        user.PhoneNumber = phone

    db.commit()
    db.refresh(user)

    return user