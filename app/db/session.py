from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

import MySQLdb

# database connection URL for my pc
#SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost:3306/Traffic_Correction_Notices"
# database connection URL for labs pc
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:computing@127.0.0.1:3306/Traffic_Correction_Notices"

# create the SQLAlchemy engine that manages DB connections
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,             # checks connections before using them
)

# creates sessions to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """provides a database session to FastAPI endpoints"""
    db: Session = SessionLocal()    # create a new database session

    try:
        yield db                    # allow the endpoint to use the database session, and then close it when done
    finally:                        # ensure the database session is closed after the endpoint is finished
        db.close()

