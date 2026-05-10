# app/models/notice.py
from sqlalchemy import Column, Integer, String, DateTime, CHAR, Text
from app.db.base import Base

class Individual(Base):
    """SQLAlchemy ORM model for the 'Individual' table"""
    __tablename__ = "Individual"

    id = Column("IndividualID", Integer, primary_key=True, index=True)
    first_name = Column("FirstName", String(20), nullable=False)
    last_name = Column("LastName", String(20), nullable=False)
    address = Column("Address", String(100), nullable=False)
    city = Column("City", String(21))
    state_id = Column("StateID", Integer, nullable=False)
    zip_code = Column("ZipCode", String(10))
    drivers_license = Column("DriversLicense", String(15))
    state_issued_id = Column("StateIssuedID", Integer, nullable=False)
    birth_date = Column("BirthDate", DateTime, nullable=False)
    height = Column("Height", String(5), nullable=False)
    weight = Column("Weight", Integer, nullable=False)
    eyes = Column("Eyes", String(2), nullable=False)


class Vehicle(Base):
    """SQLAlchemy ORM model for the 'Vehicle' table"""
    __tablename__ = "Vehicle"

    id = Column("VehicleID", Integer, primary_key=True, index=True)
    vehicle_license = Column("VehicleLicense", String(8))
    state_id = Column("StateID", Integer, nullable=False)
    colour = Column("Colour", String(100))
    year = Column("Year", Integer, nullable=False)
    make = Column("Make", String(20), nullable=False)
    type = Column("Type", String(30), nullable=False)
    vin = Column("VIN", Integer)
    registered_owner = Column("RegisteredOwner", String(40))
    address = Column("Address", String(100))


class Location(Base):
    """SQLAlchemy ORM model for the 'Location' table"""
    __tablename__ = "Location"

    id = Column("LocationID", Integer, primary_key=True, index=True)
    miles = Column("Miles", Integer, nullable=False)
    direction = Column("Direction", CHAR, nullable=False)
    town = Column("Town", String(50), nullable=False)
    road = Column("Road", String(50), nullable=False)


class Information(Base):
    """SQLAlchemy ORM model for the 'Information' table"""
    __tablename__ = "Information"

    id = Column("InformationID", Integer, primary_key=True, index=True)
    location_id = Column("LocationID", Integer, nullable=False)
    violation_date = Column("ViolationDate", DateTime, nullable=False)
    district = Column("District", Integer, nullable=False)
    detachment = Column("Detachment", Integer, nullable=False)


class Violation(Base):
    """SQLAlchemy ORM model for the 'Violation' table"""
    __tablename__ = "Violation"

    id = Column("ViolationID", Integer, primary_key=True, index=True)
    violation = Column("Violation", Text, nullable=False)


class Action(Base):
    """SQLAlchemy ORM model for the 'Action' lookup table"""
    __tablename__ = "Action"

    id = Column("ActionID", Integer, primary_key=True, index=True)
    description = Column("Description", Text)


class Officer(Base):
    """SQLAlchemy ORM model for the 'Officer' table."""
    __tablename__ = "Officer"

    id = Column("OfficerID", Integer, primary_key=True, index=True)
    officers_signature = Column("OfficersSignature", String(40), nullable=False)
    personnel_number = Column("PersonnelNumber", Integer, nullable=False)


class Notice(Base):
    """SQLAlchemy ORM model for the 'Notice' table"""
    __tablename__ = "Notice"

    id = Column("NoticeID", Integer, primary_key=True, index=True)
    individual_id = Column("IndividualID", Integer, nullable=False)
    vehicle_id = Column("VehicleID", Integer, nullable=False)
    information_id = Column("InformationID", Integer, nullable=False)
    violation_id = Column("ViolationID", Integer, nullable=False)
    officer_id = Column("OfficerID", Integer, nullable=False)
    action_id = Column("ActionID", Integer, nullable=False)
    drivers_signature = Column("DriversSignature", String(100), nullable=False)


class FullNotice(Base):
    """SQLAlchemy ORM model for the 'Full_Notice' view"""
    __tablename__ = "Full_Notice"

    NoticeID = Column(Integer, primary_key=True, index=True)
    IndividualID = Column(Integer)
    VehicleID = Column(Integer)
    InformationID = Column(Integer)
    ViolationID = Column(Integer)
    OfficerID = Column(Integer)
    ActionID = Column(Integer)
    # Individual fields
    FirstName = Column(String(100))
    LastName = Column(String(100))
    IndividualAddress = Column(String(100))
    City = Column(String(100))
    ResidenceState = Column(String(100))
    ZipCode = Column(String(100))
    DriversLicense = Column(String(100))
    IssuedState = Column(String(100))
    BirthDate = Column(DateTime)
    Height = Column(String(100))
    Weight = Column(Integer)
    Eyes = Column(String(100))
    # Vehicle fields
    VehicleLicense = Column(String(100))
    RegisteredState = Column(String(100))
    Colour = Column(String(100))
    Year = Column(Integer)
    Make = Column(String(100))
    Type = Column(String(100))
    VIN = Column(Integer)
    RegisteredOwner = Column(String(100))
    VehicleAddress = Column(String(100))
    # Information fields
    ViolationDate = Column(DateTime)
    District = Column(Integer)
    Detachment = Column(Integer)
    # Location fields
    Miles = Column(Integer)
    Direction = Column(CHAR)
    Town = Column(String(100))
    Road = Column(String(100))
    # Violation field
    Violation = Column(Text)
    # Officer fields
    OfficersSignature = Column(String(100))
    PersonnelNumber = Column(Integer)
    # Notice fields
    ActionSelection = Column(String(100))
    DriversSignature = Column(String(100))
