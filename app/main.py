from fastapi import FastAPI
import logging
# Import the notices, users, and reviews router modules from the api package.
from app.api import notice, users, reviews
from app.db.init_db import init_db

# Create the FastAPI application instance.
app = FastAPI(
    title="NYC Traffic Violation Notices API",
    version="1.0.0",
    summary="API for managing NYC traffic violation notices",
    description="This API allows users to manage and retrieve information about NYC traffic violation notices.",
)

logger = logging.getLogger("uvicorn.error")

@app.middleware("http")
async def log_exceptions(request, call_next):
    try:
        return await call_next(request)
    except Exception:
        logger.exception("Unhandled error during request")
        raise

# Ensure database tables exist.
try:
    init_db()
except Exception as e:
    print(f"Error initializing the database: {e}") # database is unreachable

# Register the routers with the main app.
app.include_router(notice.router)
app.include_router(users.router)
app.include_router(reviews.router)

#@app.get("/")
#async def root():
#    """Simple health-check endpoint."""
#    return {"message": "Week 11 app is running"}