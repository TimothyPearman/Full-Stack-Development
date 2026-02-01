from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.notice import Notice, NoticeCreate
from app.crud import notice as crud_notice

# Create a router for all notice-related endpoints.
# All paths defined here will be prefixed with /notices in the final API.
router = APIRouter(
    prefix="/notices",
    tags=["notices"],
)

@router.get("/", response_model=List[Notice], summary="Get all notices")
async def list_notices(db: Session = Depends(get_db)):
    """Get all notices from the database."""
    notices = crud_notice.get_notices(db)
    return notices

@router.get("/{notice_id}", response_model=Notice, summary="Get a notice by ID")
async def get_notice_by_id(notice_id: int, db: Session = Depends(get_db)):
    """Get a specific notice by ID."""
    notice = crud_notice.get_notice(db, notice_id)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    return notice

@router.post("/", response_model=Notice, status_code=201, summary="Create a new notice")
async def create_notice(notice_in: NoticeCreate, db: Session = Depends(get_db)):
    """Create a new notice in the database."""
    return crud_notice.create_notice(db, notice_in)

@router.put("/{notice_id}", response_model=Notice, summary="Update an existing notice")
async def update_notice(notice_id: int, notice_in: NoticeCreate, db: Session = Depends(get_db)):
    """Update an existing notice."""
    notice = crud_notice.update_notice(db, notice_id, notice_in)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    return notice

@router.delete("/{notice_id}", summary="Delete a notice")
async def delete_notice(notice_id: int, db: Session = Depends(get_db)):
    """Delete a notice from the database."""
    notice = crud_notice.delete_notice(db, notice_id)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    return {"message": "Notice deleted", "id": notice_id}


