# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Replace username, password, host and database name as needed: i.e, root for
# username and empty password (no password)
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost:3306/Traffic_Correction_Notices"

# Create the SQLAlchemy engine that manages DB connections.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # checks connections before using them
)

# Factory for Session objects (database sessions).
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency that provides a database session to FastAPI endpoints."""
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

