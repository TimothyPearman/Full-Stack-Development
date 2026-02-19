from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.notice import Notice, FullNotice, NoticeCreate
from app.crud import notice as crud_notice, user as crud_user
from app.models.user import User as UserModel

# Create a router for all notice-related endpoints.
# All paths defined here will be prefixed with /notices in the final API.
router = APIRouter(
    prefix="/notices",
    tags=["notices"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token/")

def check_valid_user(token, db: Session = Depends(get_db)):
    try:
        user_id = int(token.replace("token-", "", 1))                       # remove token prefix and convert value to an integer
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token value")

    user = db.query(UserModel).filter(UserModel.id == user_id).first()      # query the database for a user with the given id from the token
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user

def check_user_clearance(user, db: Session = Depends(get_db)):

    clearance = db.query(UserModel.Clearance).filter(UserModel.id == user.id).scalar()    # query the database for the users clearance level
    if clearance is None:
        raise HTTPException(status_code=401, detail="User clearance not found")
    else:
        return clearance
    
"""
GET Endpoints:
"""
@router.get("/me", response_model=List[FullNotice], summary="Get all notices")
async def get_notices(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Get all notices for the authenticated user."""
    user = check_valid_user(token, db)

    notices = crud_notice.get_notices_for_individual(db, user.id)   # get all notices for the authenticated user using their user id as the individual id
    return notices

@router.get("/me/vehicle/{vehicle_id}", response_model=List[FullNotice], summary="Get all notices for a specific vehicle")
async def get_notices_by_vehicle(vehicle_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Get all notices for a specific vehicle of the authenticated user."""
    user = check_valid_user(token, db)
    
    notices = crud_notice.get_notices_for_individual_by_vehicle(db, user.id, vehicle_id)    # get all notices for the authenticated user using their user id as the individual id
    return notices

@router.get("/me/officer/{officer_id}", response_model=List[FullNotice], summary="Get all notices from a specific officer")
async def get_notices_by_officer(officer_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Get all notices for a specific officer of the authenticated user."""
    user = check_valid_user(token, db)
    
    notices = crud_notice.get_notices_for_individual_by_officer(db, user.id, officer_id)    # get all notices for the authenticated user using their user id as the individual id
    return notices

"""
POST Endpoints:
"""
@router.post("/create", response_model=Notice, status_code=201, summary="Create a new notice")
async def create_notice(notice_in: NoticeCreate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Create a new notice in the database."""
    user = check_valid_user(token, db) # check if the user is valid
    clearance = check_user_clearance(user, db) # check the users clearance level to see if they are allowed to create a notice
    if clearance == "Officer":
        return crud_notice.create_notice(db, notice_in)
    else:
        raise HTTPException(status_code=403, detail="insufficient clearance: only officers can create notices")

"""
PUT Endpoints:
"""
@router.put("/{id}", response_model=List[Notice], summary="Update a notice")
async def update_notice(id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Create a new notice in the database."""
    user = check_valid_user(token, db) # check if the user is valid
    clearance = check_user_clearance(user, db) # check the users clearance level to see if they are allowed to create a notice
    if clearance == "Officer":
        return crud_notice.update_notice()
    else:
        raise HTTPException(status_code=403, detail="insufficient clearance: only officers can create notices")

@router.put("/{id}/violations/{violation_id}", response_model=List[Notice], summary="Update a violation in a notice")
async def update_violation(id: int, violation_id: int, db: Session = Depends(get_db)):
    pass

"""
DELETE Endpoints:
"""
@router.delete("/{id}", response_model=List[Notice], summary="Delete a notice")
async def delete_notice(id: int, db: Session = Depends(get_db)):
    pass

@router.delete("/{id}/violations/{violation_id}", response_model=List[Notice], summary="Remove a violation from a notice")
async def delete_violation(id: int, violation_id: int, db: Session = Depends(get_db)):
    pass

#@router.get("/timmy/", response_model=List[Notice], summary="Get all notices")
#async def list_notices(db: Session = Depends(get_db)):
#    """Get all notices from the database."""
#    notices = crud_notice.get_notices(db)
#    return notices
#
#@router.get("/{notice_id}", response_model=Notice, summary="Get a notice by ID")
#async def get_notice_by_id(notice_id: int, db: Session = Depends(get_db)):
#    """Get a specific notice by ID."""
#    notice = crud_notice.get_notice(db, notice_id)
#    if not notice:
#        raise HTTPException(status_code=404, detail="Notice not found")
#    return notice
#

#
#@router.put("/{notice_id}", response_model=Notice, summary="Update an existing notice")
#async def update_notice(notice_id: int, notice_in: NoticeCreate, db: Session = Depends(get_db)):
#    """Update an existing notice."""
#    notice = crud_notice.update_notice(db, notice_id, notice_in)
#    if not notice:
#        raise HTTPException(status_code=404, detail="Notice not found")
#    return notice
#
#@router.delete("/{notice_id}", summary="Delete a notice")
#async def delete_notice(notice_id: int, db: Session = Depends(get_db)):
#    """Delete a notice from the database."""
#    notice = crud_notice.delete_notice(db, notice_id)
#    if not notice:
#        raise HTTPException(status_code=404, detail="Notice not found")
#    return {"message": "Notice deleted", "id": notice_id}