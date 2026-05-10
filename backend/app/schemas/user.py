# app/schemas/review.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Token(BaseModel):
    """schema for the token response when a user logs in"""
    access_token: str
    token_type: str
    expires_in: int
    clearance: str

class UserBase(BaseModel):
    """base schema for a user"""
    Username: str
    Clearance: str

class User(UserBase):
    """schema returned by the API for a user"""
    id: int
    FullName: Optional[str] = None
    DateOFBirth: Optional[datetime] = None
    CurrentAddress: Optional[str] = None
    LicenseNumber: Optional[str] = None
    licensePostcode: Optional[str] = None
    NationalInsuranceNumber: Optional[str] = None
    RegistrationNumber: Optional[str] = None
    Email: Optional[str] = None
    PhoneNumber: Optional[str] = None

    class Config:
        from_attributes = True

class Clearance(BaseModel):
    """schema for clearance response"""
    clearance: str

class UserRegister(BaseModel):
    """schema for user registration form"""
    username: str
    password: str
    clearance: str
    fullName: Optional[str] = None
    dateOfBirth: Optional[str] = None
    currentAddress: Optional[str] = None
    driverLicenseNumber: Optional[str] = None
    postcode: Optional[str] = None
    nationalInsurance: Optional[str] = None
    vehicleRegNumber: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
