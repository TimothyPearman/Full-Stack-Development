import logging

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List, cast

from app.db.session import get_db
from app.schemas.notice import Notice, FullNotice, NoticeCreate, NoticeUpdate
from app.crud import notice as crud_notice, user as crud_user
from app.models.user import User as UserModel
from app.core.security import get_user_id_from_token, ExpiredSignatureError, InvalidTokenError

logger = logging.getLogger(__name__)

# Create a router for all notice-related endpoints.
# All paths defined here will be prefixed with /notices in the final API.
router = APIRouter(
    prefix="/notices",
    tags=["notices"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token/")

def check_valid_user(token, db: Session = Depends(get_db)):
    try:
        user_id = get_user_id_from_token(token)
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token value")

    user = db.query(UserModel).filter(UserModel.id == user_id).first()      # query the database for a user with the given id from the token
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

def get_user_clearance(user, db: Session = Depends(get_db)):
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
    logger.info("Notice list requested by user_id=%s", user.id)

    # get user clearance level to determine which notices they are allowed to see
    clearance = get_user_clearance(user, db)

    if clearance == "Officer":                                                   # if user is an officer, they can see all notices
        notices = crud_notice.get_all_notices(db)
        logger.info("Notice list returned for officer user_id=%s count=%s", user.id, len(notices))
    elif clearance == "Civilian":                                                   # if user is a civilian, they can only see notices issued to them
        owner = cast(str, user.Username)  # satisfy type checker
        notices = crud_notice.get_notices_for_individual(db, owner)   # get all notices for the authenticated user using their username as the registered owner
        logger.info("Notice list returned for civilian user_id=%s count=%s", user.id, len(notices))
    else :
        logger.warning("Notice list denied for user_id=%s due to invalid clearance=%s", user.id, clearance)
        raise HTTPException(status_code=403, detail="Invalid clearance level: only officers and civilians can view notices")
    
    return notices


#@router.get("/me/vehicle/{vehicle_id}", response_model=List[FullNotice], summary="Get all notices for a specific vehicle")
#async def get_notices_by_vehicle(vehicle_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#    """Get all notices for a specific vehicle of the authenticated user."""
#    user = check_valid_user(token, db)
#    
#    notices = crud_notice.get_notices_for_individual_by_vehicle(db, user.id, vehicle_id)    # get all notices for the authenticated user using their user id as the individual id
#    return notices
#
#@router.get("/me/officer/{officer_id}", response_model=List[FullNotice], summary="Get all notices from a specific officer")
#async def get_notices_by_officer(officer_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#    """Get all notices for a specific officer of the authenticated user."""
#    user = check_valid_user(token, db)
#    
#    notices = crud_notice.get_notices_for_individual_by_officer(db, user.id, officer_id)    # get all notices for the authenticated user using their user id as the individual id
#    return notices


@router.get("/{id}", response_model=Notice, summary="Get a notice by ID")
async def get_notice_by_id(id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Get a single notice by its NoticeID. Officers may view any notice; civilians may only view their own."""
    user = check_valid_user(token, db)
    logger.info("Notice detail requested for notice_id=%s by user_id=%s", id, user.id)
    clearance = get_user_clearance(user, db)

    notice = crud_notice.get_notice_by_id(db, id)
    if not notice:
        logger.warning("Notice detail request failed: notice not found (notice_id=%s, user_id=%s)", id, user.id)
        raise HTTPException(status_code=404, detail="Notice not found")

    if clearance == "Civilian":
        registered = notice.get("RegisteredOwner")
        if registered != user.Username:
            logger.warning("Notice detail denied for civilian user_id=%s notice_id=%s", user.id, id)
            raise HTTPException(status_code=403, detail="insufficient clearance to view this notice")

    logger.info("Notice detail returned for notice_id=%s to user_id=%s", id, user.id)
    return notice


@router.get("/counts/total", summary="Get total number of notices")
async def get_notices_total(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = check_valid_user(token, db)
    logger.info("Total notice count requested by user_id=%s", user.id)
    clearance = get_user_clearance(user, db)
    if clearance != "Officer":
        logger.warning("Total notice count denied for user_id=%s", user.id)
        raise HTTPException(status_code=403, detail="insufficient clearance")
    logger.info("Total notice count returned to officer user_id=%s", user.id)
    return crud_notice.count_notices_total(db)


@router.get("/counts/by-violation", summary="Get notice counts by violation")
async def get_notices_by_violation(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = check_valid_user(token, db)
    logger.info("Notice counts by violation requested by user_id=%s", user.id)
    clearance = get_user_clearance(user, db)
    if clearance != "Officer":
        logger.warning("Notice counts by violation denied for user_id=%s", user.id)
        raise HTTPException(status_code=403, detail="insufficient clearance")
    logger.info("Notice counts by violation returned to officer user_id=%s", user.id)
    return crud_notice.count_notices_by_violation(db)


@router.get("/counts/by-district", summary="Get notice counts by district")
async def get_notices_by_district(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = check_valid_user(token, db)
    logger.info("Notice counts by district requested by user_id=%s", user.id)
    clearance = get_user_clearance(user, db)
    if clearance != "Officer":
        logger.warning("Notice counts by district denied for user_id=%s", user.id)
        raise HTTPException(status_code=403, detail="insufficient clearance")
    logger.info("Notice counts by district returned to officer user_id=%s", user.id)
    return crud_notice.count_notices_by_district(db)


@router.get("/counts/by-detachment", summary="Get notice counts by detachment")
async def get_notices_by_detachment(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = check_valid_user(token, db)
    logger.info("Notice counts by detachment requested by user_id=%s", user.id)
    clearance = get_user_clearance(user, db)
    if clearance != "Officer":
        logger.warning("Notice counts by detachment denied for user_id=%s", user.id)
        raise HTTPException(status_code=403, detail="insufficient clearance")
    logger.info("Notice counts by detachment returned to officer user_id=%s", user.id)
    return crud_notice.count_notices_by_detachment(db)

"""
POST Endpoints:
"""
@router.post("/create", response_model=Notice, status_code=201, summary="Create a new notice")
async def create_notice(notice_in: NoticeCreate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Create a new notice in the database."""
    user = check_valid_user(token, db)              # check if the user is valid
    logger.info("Notice creation requested by user_id=%s", user.id)
    clearance = get_user_clearance(user, db)        # check the users clearance level to see if they are allowed to create a notice
    if clearance == "Officer":
        created = crud_notice.create_notice(db, notice_in)
        notice_id = created.get("NoticeID") if isinstance(created, dict) else None
        logger.info("Notice created successfully by user_id=%s notice_id=%s", user.id, notice_id)
        return created
    else:
        logger.warning("Notice creation denied for user_id=%s", user.id)
        raise HTTPException(status_code=403, detail="insufficient clearance")

"""
PUT Endpoints:
"""
@router.put("/{id}", response_model=Notice, summary="Update a notice")
async def update_notice(id: int, notice_in: NoticeUpdate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Update an existing notice in the database."""
    user = check_valid_user(token, db)              # check if the user is valid
    logger.info("Notice update requested for notice_id=%s by user_id=%s", id, user.id)
    clearance = get_user_clearance(user, db)        # check the users clearance level to see if they are allowed to create a notice
    if clearance == "Officer":
        notice = crud_notice.update_notice(db, id, notice_in)
        if not notice:
            logger.warning("Notice update failed: notice not found (notice_id=%s, user_id=%s)", id, user.id)
            raise HTTPException(status_code=404, detail="Notice not found")
        logger.info("Notice updated successfully for notice_id=%s by user_id=%s", id, user.id)
        return notice
    else:
        logger.warning("Notice update denied for user_id=%s notice_id=%s", user.id, id)
        raise HTTPException(status_code=403, detail="insufficient clearance: only officers can update notices")

#@router.put("/{id}/violations/{violation}", response_model=Notice, summary="Update a violation in a notice")
#async def update_violation(id: int, violation: str, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#    """Update an existing notice in the database."""
#    user = check_valid_user(token, db)              # check if the user is valid
#    clearance = get_user_clearance(user, db)        # check the users clearance level to see if they are allowed to create a notice
#    if clearance == "Officer":
#        notice = crud_notice.update_violation(db, id, violation)
#        if not notice:
#            raise HTTPException(status_code=404, detail="Notice not found")
#        return notice
#    else:
#        raise HTTPException(status_code=403, detail="insufficient clearance: only officers can update notices")

"""
DELETE Endpoints:
"""
@router.delete("/{id}", response_model=Notice, summary="Delete a notice")
async def delete_notice(id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """delete an existing notice in the database"""
    user = check_valid_user(token, db)              # check if the user is valid
    logger.info("Notice delete requested for notice_id=%s by user_id=%s", id, user.id)
    clearance = get_user_clearance(user, db)        # check the users clearance level to see if they are allowed to delete a notice
    if clearance == "Officer":
        notice = crud_notice.delete_notice(db, id)
        if not notice:
            logger.warning("Notice delete failed: notice not found (notice_id=%s, user_id=%s)", id, user.id)
            raise HTTPException(status_code=404, detail="Notice not found")
        logger.info("Notice deleted successfully for notice_id=%s by user_id=%s", id, user.id)
        return notice
    else:
        logger.warning("Notice delete denied for user_id=%s notice_id=%s", user.id, id)
        raise HTTPException(status_code=403, detail="insufficient clearance: only officers can delete notices")

#@router.delete("/{id}/violations", response_model=Notice, summary="Remove a violation from a notice")
#async def delete_violation(id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#    """delete a violation from an existing notice in the database"""
#    user = check_valid_user(token, db)              # check if the user is valid
#    clearance = get_user_clearance(user, db)        # check the users clearance level to see if they are allowed to delete a notice
#    if clearance == "Officer":
#        notice = crud_notice.delete_violation(db, id)
#        if not notice:
#            raise HTTPException(status_code=404, detail="Notice not found")
#        return notice
#    else:
#        raise HTTPException(status_code=403, detail="insufficient clearance: only officers can delete notices")