# app/db/init_db.py
from app.db.base import Base
from app.db.session import engine

# Import models so SQLAlchemy knows about them.
from app.models.notice import (
    Individual,
    Vehicle,
    Location,
    Information,
    Violation,
    Officer,
    Notice,
    FullNotice,
)  # noqa: F401
from app.models.user import User  # noqa: F401

def init_db():
    """Create tables in the database if they do not already exist."""
    Base.metadata.create_all(bind=engine)
    

