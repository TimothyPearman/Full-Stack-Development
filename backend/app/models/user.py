# app/models/user.py
from sqlalchemy import Column, Integer, String
from app.db.base import Base

class User(Base):
    """SQLAlchemy ORM model for the 'User' table"""
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, index=True)
    Username = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    Clearance = Column(String(255), nullable=False)
