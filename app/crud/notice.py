# app/crud/notice.py
from sqlalchemy import Column, text
from sqlalchemy.orm import Session
from app.models.notice import ( FullNotice,
    Individual,
    Vehicle,
    Location,
    Information,
    Violation,
    Officer,
    Notice,
)
from app.schemas.notice import NoticeCreate

"""GET Endpoints functions"""
def get_notices_for_individual(db: Session, individual_id: int):
    """Return all Notice records from Full_Notice view for a specific individual."""
    query = text("""
        SELECT *
        FROM Full_Notice
        WHERE IndividualID = :individual_id
        ORDER BY NoticeID ASC
    """)
    result = db.execute(query, {"individual_id": individual_id})
    return result.fetchall()

def get_notices_for_individual_by_vehicle(db: Session, individual_id: int, vehicle_id: int):
    """Return all Notice records from Full_Notice view for a specific individual and vehicle."""
    query = text("""
        SELECT *
        FROM Full_Notice 
        WHERE IndividualID = :individual_id AND VehicleID = :vehicle_id
        ORDER BY NoticeID ASC
    """)
    result = db.execute(query, {"individual_id": individual_id, "vehicle_id": vehicle_id})
    return result.fetchall()

def get_notices_for_individual_by_officer(db: Session, individual_id: int, officer_id: int):
    """Return all Notice records from Full_Notice view for a specific individual and officer."""
    query = text("""
        SELECT *
        FROM Full_Notice 
        WHERE IndividualID = :individual_id AND OfficerID = :officer_id
        ORDER BY NoticeID ASC
    """)
    result = db.execute(query, {"individual_id": individual_id, "officer_id": officer_id})
    return result.fetchall()

def create_notice(db: Session, notice_in: NoticeCreate):
    """Create a new Notice record with all related tables in a transaction."""
    if notice_in.ResidenceState < 1 or notice_in.ResidenceState > 50:
        raise ValueError("invalid ResidenceState id: ids must be 1-50")
    if notice_in.IssuedState < 1 or notice_in.IssuedState > 50:
        raise ValueError("invalid IssuedState id: ids must be 1-50")
    if notice_in.RegisteredState < 1 or notice_in.RegisteredState > 50:
        raise ValueError("invalid RegisteredState id: ids must be 1-50")
    try:
        # Create Individual record
        individual = Individual(
            first_name=notice_in.FirstName,
            last_name=notice_in.LastName,
            address=notice_in.IndividualAddress,
            city=notice_in.City,
            state_id=notice_in.ResidenceState,
            zip_code=notice_in.ZipCode,
            drivers_license=notice_in.DriversLicense,
            state_issued_id=notice_in.IssuedState,
            birth_date=notice_in.BirthDate,
            height=notice_in.Height,
            weight=notice_in.Weight,
            eyes=notice_in.Eyes,
        )
        db.add(individual)
        db.flush()  # Get the auto-generated IndividualID
        
        # Create Vehicle record
        vehicle = Vehicle(
            vehicle_license=notice_in.VehicleLicense,
            state_id=notice_in.RegisteredState,
            colour=notice_in.Colour,
            year=notice_in.Year,
            make=notice_in.Make,
            type=notice_in.Type,
            vin=notice_in.VIN,
            registered_owner=notice_in.RegisteredOwner,
            address=notice_in.VehicleAddress,
        )
        db.add(vehicle)
        db.flush()  # Get the auto-generated VehicleID
        
        # Create Location record
        location = Location(
            miles=notice_in.Miles,
            direction=notice_in.Direction,
            town=notice_in.Town,
            road=notice_in.Road,
        )
        db.add(location)
        db.flush()  # Get the auto-generated LocationID
        
        # Create Information record (depends on LocationID)
        information = Information(
            location_id=location.id,
            violation_date=notice_in.ViolationDate,
            district=notice_in.District,
            detachment=notice_in.Detachment,
        )
        db.add(information)
        db.flush()  # Get the auto-generated InformationID
        
        # Create Violation record
        violation = Violation(
            violation=notice_in.Violation,
        )
        db.add(violation)
        db.flush()  # Get the auto-generated ViolationID
        
        # Create Officer record
        officer = Officer(
            officers_signature=notice_in.OfficersSignature,
            personnel_number=notice_in.PersonnelNumber,
        )
        db.add(officer)
        db.flush()  # Get the auto-generated OfficerID
        
        # Create Notice record (links all the above)
        notice = Notice(
            individual_id=db.query(Individual).filter_by(first_name=notice_in.FirstName, last_name=notice_in.LastName).first().id,
            vehicle_id=vehicle.id,
            information_id=information.id,
            violation_id=violation.id,
            officer_id=officer.id,
            action_selection=notice_in.ActionSelection,
            drivers_signature=notice_in.DriversSignature,
        )
        db.add(notice)
        db.commit()
        db.refresh(notice)  # Load the generated NoticeID
        return {
            "NoticeID": notice.id,
            "IndividualID": notice.individual_id,
            "VehicleID": notice.vehicle_id,
            "InformationID": notice.information_id,
            "ViolationID": notice.violation_id,
            "OfficerID": notice.officer_id,
            "ActionSelection": notice.action_selection,
            "DriversSignature": notice.drivers_signature,
        }
    
    except Exception as e:
        db.rollback()
        raise e

    
def add_violation(db: Session, notice_id: int, new_violation: str):
    notice = db.query(Notice).filter(Notice.id == notice_id).first()    # get the notice with the given id from the database

    if not notice:  
        raise ValueError("Notice not found")                            # raise error if notice is not found
    
    violation_obj = Violation(violation=new_violation)
    db.add(violation_obj)
    db.flush()
    notice.violation_id = violation_obj.id
    db.commit()
    db.refresh(notice)
    return [notice]

#def update_notice(db: Session, notice_id: int, notice_in: NoticeCreate):
#    """Update an existing Notice. Return the updated Notice or None if not found."""
#    notice = get_notice(db, notice_id)
#    if not notice:
#        return None
#    notice.NoticeID=notice_in.NoticeID
#    notice.IndividualID=notice_in.IndividualID
#    notice.VehicleID=notice_in.VehicleID
#    notice.InformationID=notice_in.InformationID
#    notice.ViolationID=notice_in.ViolationID
#    notice.OfficerID=notice_in.OfficerID
#    notice.ActionSelection=notice_in.ActionSelection
#    notice.DriversSignature=notice_in.DriversSignature
#    db.commit()
#    db.refresh(notice)
#    return notice
#
#def delete_notice(db: Session, notice_id: int):
#    """Delete a Notice by id. Return the deleted Notice or None if not found."""
#    notice = get_notice(db, notice_id)
#    if not notice:
#        return None
#    db.delete(notice)
#    db.commit()
#    return notice
#