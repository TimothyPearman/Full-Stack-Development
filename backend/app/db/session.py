import os
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


def get_database_url() -> str:
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url

    database_host = os.getenv("DB_HOST", "localhost")
    database_port = os.getenv("DB_PORT", "3306")
    database_user = quote_plus(os.getenv("DB_USER", "root"))
    database_password = quote_plus(os.getenv("DB_PASSWORD", ""))
    database_name = quote_plus(os.getenv("DB_NAME", "CompuTaught"))

    return (
        f"mysql+pymysql://{database_user}:{database_password}"
        f"@{database_host}:{database_port}/{database_name}"
    )


SQLALCHEMY_DATABASE_URL = get_database_url()

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

