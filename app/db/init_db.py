from app.db.base import Base
from app.db.session import engine

# import models so SQLAlchemy knows about them
from app.models.notice import (
    Individual,
    Vehicle,
    Location,
    Information,
    Violation,
    Officer,
    Notice,
    FullNotice,
)  # noqa: F401  # tell it to shut up with the annoying warning

from app.models.user import User  # noqa: F401

def init_db():
    """create tables in the database if they do not already exist"""
    Base.metadata.create_all(bind=engine)
    

