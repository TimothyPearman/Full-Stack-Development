# app/crud/notice.py
from sqlalchemy import Column
from sqlalchemy.orm import Session
from app.models.notice import Notice as NoticeModel
from app.schemas.notice import NoticeCreate

def get_notices(db: Session):
    """Return all Notice records from the database."""
    return db.query(NoticeModel).all()

def get_notice(db: Session, notice_id: int):
    """Return a single Notice by id, or None if it does not exist."""
    return db.query(NoticeModel).filter(NoticeModel.NoticeID == notice_id).first()
def create_notice(db: Session, notice_in: NoticeCreate):
    """Create a new Notice from NoticeCreate data."""
    notice = NoticeModel(
        NoticeID=notice_in.NoticeID,
        IndividualID=notice_in.IndividualID,
        VehicleID=notice_in.VehicleID,
        InformationID=notice_in.InformationID,
        ViolationID=notice_in.ViolationID,
        OfficerID=notice_in.OfficerID,
        ActionSelection=notice_in.ActionSelection,
        DriversSignature=notice_in.DriversSignature,
    )
    db.add(notice)
    db.commit()
    db.refresh(notice)  # load generated ID and any defaults
    return notice

def update_notice(db: Session, notice_id: int, notice_in: NoticeCreate):
    """Update an existing Notice. Return the updated Notice or None if not found."""
    notice = get_notice(db, notice_id)
    if not notice:
        return None
    notice.NoticeID=notice_in.NoticeID
    notice.IndividualID=notice_in.IndividualID
    notice.VehicleID=notice_in.VehicleID
    notice.InformationID=notice_in.InformationID
    notice.ViolationID=notice_in.ViolationID
    notice.OfficerID=notice_in.OfficerID
    notice.ActionSelection=notice_in.ActionSelection
    notice.DriversSignature=notice_in.DriversSignature
    db.commit()
    db.refresh(notice)
    return notice

def delete_notice(db: Session, notice_id: int):
    """Delete a Notice by id. Return the deleted Notice or None if not found."""
    notice = get_notice(db, notice_id)
    if not notice:
        return None
    db.delete(notice)
    db.commit()
    return notice
