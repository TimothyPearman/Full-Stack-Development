# app/models/user.py
from sqlalchemy import Column, Integer, String, DateTime
from app.db.base import Base

class User(Base):
    """SQLAlchemy ORM model for the 'User' table"""
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, index=True)
    Username = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    Clearance = Column(String(100), nullable=False)
    FullName = Column(String(100), nullable=True)
    DateOFBirth = Column(DateTime, nullable=True)
    CurrentAddress = Column(String(100), nullable=True)
    LicenseNumber = Column(String(100), nullable=True)
    licensePostcode = Column(String(100), nullable=True)
    NationalInsuranceNumber = Column(String(100), nullable=True)
    RegistrationNumber = Column(String(100), nullable=True)
    Email = Column(String(100), nullable=True)
    PhoneNumber = Column(String(100), nullable=True)
