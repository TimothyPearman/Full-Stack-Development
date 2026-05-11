import os
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import notice, user    # import the routers to be registered with the main app
from app.db.init_db import init_db  # import the database initialization function to ensure tables exist on startup


# Startup sanity check: ensure SECRET_KEY is set and long enough for HMAC-SHA256
secret_key = os.getenv("SECRET_KEY", "")
if len(secret_key) < 32:
    raise RuntimeError(
        "SECRET_KEY must be at least 32 characters long. "
        "Set a secure SECRET_KEY in .env or the environment before starting the app."
    )

# create the fastapi application instance.
app = FastAPI(
    title="NYC Traffic Violation Notices API",
    version="1.? (i lost count)",
    summary="API for managing NYC traffic violation notices",
    description="This API allows users to manage and retrieve information about NYC traffic violation notices. yippee",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)


# ensure database tables exist
try:
    init_db()
except Exception as e:
    print(f"Error initializing the database: {e}") # database is unreachable

# Register the routers with the main app.
app.include_router(notice.router)
app.include_router(user.router)

# root endpoint for debugging
@app.get("/")
async def root():
    """Simple root endpoint."""
    return {"message": "assessment 3 API is working, yippee!"}

# health endpoint for testing
@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}
