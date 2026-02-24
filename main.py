from fastapi import FastAPI
from app.api import notice, user    # import the routers to be registered with the main app
from app.db.init_db import init_db  # import the database initialization function to ensure tables exist on startup

# create the fastapi application instance.
app = FastAPI(
    title="NYC Traffic Violation Notices API",
    version="1.? (i lost count)",
    summary="API for managing NYC traffic violation notices",
    description="This API allows users to manage and retrieve information about NYC traffic violation notices. yippee",
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
#@app.get("/")
#async def root():
#    """Simple health-check endpoint."""
#    return {"message": "assessment 2 API is working, yay!"}