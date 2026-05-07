from app.db.base import Base
from app.db.session import engine

def init_db():
    """create tables in the database if they do not already exist"""
    Base.metadata.create_all(bind=engine)
    

