# app/models/notice.py
from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Notice(Base):
    """SQLAlchemy ORM model for the 'notices' table."""
    __tablename__ = "Notice"

    NoticeID = Column(Integer, primary_key=True, index=True)
    IndividualID  = Column(Integer, nullable=False)
    VehicleID = Column(Integer, nullable=False)
    InformationID = Column(Integer, nullable=False)
    ViolationID = Column(Integer, nullable=False)
    OfficerID = Column(Integer, nullable=False)
    ActionSelection = Column(Integer, nullable=False)
    DriversSignature = Column(String(40), nullable=False)
