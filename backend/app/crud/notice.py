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
from app.schemas.notice import NoticeCreate, NoticeUpdate

"""GET Endpoints functions"""
def get_notices_for_individual(db: Session, individual_id: int):
    """return all Notice records from Full_Notice view for a specific individual"""
    query = text("""
        SELECT *
        FROM Full_Notice
        WHERE IndividualID = :individual_id
        ORDER BY NoticeID ASC
    """)

    result = db.execute(query, {"individual_id": individual_id})    # execute query with provided parameter

    return result.fetchall()

def get_notices_for_individual_by_vehicle(db: Session, individual_id: int, vehicle_id: int):
    """return all Notice records from Full_Notice view for a specific individual and vehicle"""
    query = text("""
        SELECT *
        FROM Full_Notice 
        WHERE IndividualID = :individual_id AND VehicleID = :vehicle_id
        ORDER BY NoticeID ASC
    """)

    result = db.execute(query, {"individual_id": individual_id, "vehicle_id": vehicle_id}) # execute query with provided parameters
    
    return result.fetchall()

def get_notices_for_individual_by_officer(db: Session, individual_id: int, officer_id: int):
    """return all Notice records from Full_Notice view for a specific individual and officer"""
    query = text("""
        SELECT *
        FROM Full_Notice 
        WHERE IndividualID = :individual_id AND OfficerID = :officer_id
        ORDER BY NoticeID ASC
    """)

    result = db.execute(query, {"individual_id": individual_id, "officer_id": officer_id})  # execute query with provided parameters

    return result.fetchall()


def create_notice(db: Session, notice_in: NoticeCreate):
    """Create a new Notice record with all related tables in a transaction"""
    if notice_in.ResidenceState < 1 or notice_in.ResidenceState > 50:   # api default value is 0, table ids start at 1, added error checking so i dont have to read through giant error messages constantly when testing
        raise ValueError("invalid ResidenceState id: ids must be 1-50")
    if notice_in.IssuedState < 1 or notice_in.IssuedState > 50:
        raise ValueError("invalid IssuedState id: ids must be 1-50")
    if notice_in.RegisteredState < 1 or notice_in.RegisteredState > 50:
        raise ValueError("invalid RegisteredState id: ids must be 1-50")
    
    try:
        individual = Individual(                        # fill records in `Individual` table
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
        db.add(individual)                              # add to database session
        db.flush()                                      # get the auto-incremented `IndividualID`
        
        vehicle = Vehicle(                              # fill records in `Vehicle` table          
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
        db.flush()    
        
        location = Location(
            miles=notice_in.Miles,
            direction=notice_in.Direction,
            town=notice_in.Town,
            road=notice_in.Road,
        )
        db.add(location)
        db.flush()
        
        information = Information(
            location_id=location.id,
            violation_date=notice_in.ViolationDate,
            district=notice_in.District,
            detachment=notice_in.Detachment,
        )
        db.add(information)
        db.flush()
        
        violation = Violation(
            violation=notice_in.Violation,
        )
        db.add(violation)
        db.flush()
        
        officer = Officer(
            officers_signature=notice_in.OfficersSignature,
            personnel_number=notice_in.PersonnelNumber,
        )
        db.add(officer)
        db.flush()
        
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
        db.commit()         # commit the transaction to save all records to the database
        db.refresh(notice)  # refresh the notice to get the new id from the database

        return {            # return the newly created notice as a dict compatible with the Notice schema
            "NoticeID": notice.id,
            "IndividualID": notice.individual_id,
            "VehicleID": notice.vehicle_id,
            "InformationID": notice.information_id,
            "ViolationID": notice.violation_id,
            "OfficerID": notice.officer_id,
            "ActionSelection": notice.action_selection,
            "DriversSignature": notice.drivers_signature,
        }
    
    except Exception as e:  # catch any exception that occurs during the transaction
        db.rollback()       # rollback the transaction if any error occurs :C
        raise e


def update_notice(db: Session, notice_id: int, notice_in: NoticeUpdate):
    """update an existing Notice"""
    notice = db.query(Notice).filter(Notice.id == notice_id).first()    # get notice to be updated

    if not notice:                                                      # ensure notice exists
        return None

    update_data = notice_in.model_dump(exclude_unset=True)              # convert model to dict and exclude unset fields to allow for partial updates
    
    if "ActionSelection" in update_data:                                
        notice.action_selection = update_data["ActionSelection"]
    if "DriversSignature" in update_data:
        notice.drivers_signature = update_data["DriversSignature"]

    db.commit()                                                         # commit changes to database
    db.refresh(notice)                                                  # refresh notice to get updated data                                  
    
    return {                                                            # return updated notice as a dict compatible with Notice schema
        "NoticeID": notice.id,
        "IndividualID": notice.individual_id,
        "VehicleID": notice.vehicle_id,
        "InformationID": notice.information_id,
        "ViolationID": notice.violation_id,
        "OfficerID": notice.officer_id,
        "ActionSelection": notice.action_selection,
        "DriversSignature": notice.drivers_signature,
    }

def update_violation(db: Session, notice_id: int, violation_in: str):
    """update the violation of an existing Notice"""
    notice = db.query(Notice).filter(Notice.id == notice_id).first()    # get notice to be updated

    if not notice:                                                      # ensure notice exists
        return None
    
    violation = db.query(Violation).filter(Violation.id == notice.violation_id).first()   # get violation to be updated
    violation.violation = violation_in                                  # update violation field

    db.commit()                                                         # commit changes to database
    db.refresh(notice)                                                  # refresh notice to get updated data                                  
    
    return {                                                            # return updated notice as a dict compatible with Notice schema
        "NoticeID": notice.id,
        "IndividualID": notice.individual_id,
        "VehicleID": notice.vehicle_id,
        "InformationID": notice.information_id,
        "ViolationID": notice.violation_id,
        "OfficerID": notice.officer_id,
        "ActionSelection": notice.action_selection,
        "DriversSignature": notice.drivers_signature,
    }


def delete_notice(db: Session, notice_id: int):
    """delete an existing Notice"""
    notice = db.query(Notice).filter(Notice.id == notice_id).first()    # get notice to be deleted

    if not notice:                                                      # ensure notice exists
        return None

    deleted_notice = {
        "NoticeID": notice.id,
        "IndividualID": notice.individual_id,
        "VehicleID": notice.vehicle_id,
        "InformationID": notice.information_id,
        "ViolationID": notice.violation_id,
        "OfficerID": notice.officer_id,
        "ActionSelection": notice.action_selection,
        "DriversSignature": notice.drivers_signature,
    }

    try:
        db.delete(notice)
        db.commit()
        return deleted_notice
    except Exception as e:
        db.rollback()
        raise e
    
def delete_violation(db: Session, notice_id: int):
    """delete the violation of an existing Notice by setting it to an empty string"""
    notice = db.query(Notice).filter(Notice.id == notice_id).first()    # get notice to be updated

    if not notice:                                                      # ensure notice exists
        return None

    violation = db.query(Violation).filter(Violation.id == notice.violation_id).first()   # get violation to be updated
    violation.violation = "violation resolved"                          # indicate violation has been eddited since notice was issued

    db.commit()                                                         # commit changes to database
    db.refresh(notice)                                                  # refresh notice to get updated data                                  
    
    return {                                                            # return updated notice as a dict compatible with Notice schema
        "NoticeID": notice.id,
        "IndividualID": notice.individual_id,
        "VehicleID": notice.vehicle_id,
        "InformationID": notice.information_id,
        "ViolationID": notice.violation_id,
        "OfficerID": notice.officer_id,
        "ActionSelection": notice.action_selection,
        "DriversSignature": notice.drivers_signature,
    }