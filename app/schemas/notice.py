# app/schemas/notice.py
from pydantic import BaseModel
from typing import Optional

# Base class with fields shared by multiple notice schemas.
class NoticeBase(BaseModel):
    NoticeID: int
    IndividualID: int
    VehicleID: int
    InformationID: int
    ViolationID: int
    OfficerID: int
    ActionSelection: int
    DriversSignature: str

# Used when creating or fully updating a notice via the API.
class NoticeCreate(NoticeBase):
    pass

# Used when returning a notice from the API.
class Notice(NoticeBase):
    class Config:
        # from_attributes allows Pydantic to work with SQLAlchemy models.
        from_attributes = True
