import os
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


def get_database_url() -> str:
    # Try environment variables for known database URLs
    for env_name in ("DATABASE_URL_HOME", "DATABASE_URL_LAB"):
        # strip whitespace and quotes
        database_url = os.getenv(env_name, "").strip().strip('"').strip("'")
        if database_url:
            return database_url

    # If no full database URL is found, try to construct one from individual components
    database_host = os.getenv("DB_HOST", "").strip()
    database_port = os.getenv("DB_PORT", "").strip()
    database_user = os.getenv("DB_USER", "").strip()
    database_password = os.getenv("DB_PASSWORD", "")
    database_name = os.getenv("DB_NAME", "").strip()

    if all((database_host, database_port, database_user, database_name)):
        return (
            f"mysql+pymysql://{quote_plus(database_user)}:{quote_plus(database_password)}"
            f"@{database_host}:{database_port}/{quote_plus(database_name)}"
        )

    raise RuntimeError(
        "No database configuration was found. Set DATABASE_URL_HOME, DATABASE_URL_LAB, "
        ",or all of DB_HOST, DB_PORT, DB_USER, and DB_NAME for a new user."
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

