# app/schemas/notice.py
from pydantic import BaseModel, Field
from typing import Optional, Annotated
from datetime import datetime
from pydantic import StringConstraints

# Used when returning a full notice from the Full_Notice view.
class NoticeBase(BaseModel):
    # Individual fields
    FirstName: Optional[str] = None
    LastName: Optional[str] = None
    IndividualAddress: Optional[str] = None
    City: Optional[str] = None
    ResidenceState: Optional[str] = None
    ZipCode: Optional[str] = None
    DriversLicense: Optional[str] = None
    IssuedState: Optional[str] = None
    BirthDate: Optional[datetime] = None
    Height: Optional[str] = None
    Weight: Optional[int] = None
    Eyes: Optional[str] = None
    # Vehicle fields
    VehicleLicense: Optional[str] = None
    RegisteredState: Optional[str] = None
    Colour: Optional[str] = None
    Year: Optional[int] = None
    Make: Optional[str] = None
    Type: Optional[str] = None
    VIN: Optional[int] = None
    RegisteredOwner: Optional[str] = None
    VehicleAddress: Optional[str] = None
    # Information fields
    ViolationDate: Optional[datetime] = None
    District: Optional[int] = None
    Detachment: Optional[int] = None
    # Location fields
    Miles: Optional[int] = None
    Direction: Optional[str] = None
    Town: Optional[str] = None
    Road: Optional[str] = None
    # Violation field
    Violation: Optional[str] = None
    # Officer fields
    OfficersSignature: Optional[str] = None
    PersonnelNumber: Optional[int] = None
    # Notice fields
    ActionSelection: Optional[int] = None
    DriversSignature: Optional[str] = None

    class Config:
        from_attributes = True

# Used when creating or fully updating a notice via the API.
class NoticeCreate(NoticeBase):
    
    # Make these required for creation
    FirstName: str
    LastName: str
    IndividualAddress: str
    City: str
    ResidenceState: int  # StateID must be an integer
    ZipCode: str
    DriversLicense: str
    IssuedState: int  # StateIssuedID must be an integer
    BirthDate: datetime
    Height: str
    Weight: int
    Eyes: str
    # Vehicle fields
    VehicleLicense: str
    RegisteredState: int  # StateID must be an integer
    Colour: str
    Year: int
    Make: str
    Type: str
    VIN: int
    RegisteredOwner: str
    VehicleAddress: str
    # Information fields
    ViolationDate: datetime
    District: int
    Detachment: int
    # Location fields
    Miles: int
    Direction: str
    Town: str
    Road: str
    # Violation field
    Violation: str
    # Officer fields
    OfficersSignature: str
    PersonnelNumber: int
    # Notice fields
    ActionSelection: int
    DriversSignature: str

# Used when returning a single notice from the API.
class Notice(NoticeBase):
    NoticeID: int

    class Config:
        # from_attributes allows Pydantic to work with SQLAlchemy models.
        from_attributes = True

# Alias for Full_Notice view response
class FullNotice(NoticeBase):
    class Config:
        from_attributes = True