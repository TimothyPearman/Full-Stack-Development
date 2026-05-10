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
    Action,
)
from app.schemas.notice import NoticeCreate, NoticeUpdate

"""GET Endpoints functions"""
def get_all_notices(db: Session):
    """return all Notice records from Full_Notice view"""
    query = text("""
        SELECT *
        FROM Full_Notice
        ORDER BY NoticeID ASC
    """)
    result = db.execute(query)   # execute query
    return result.fetchall()     # return all results as a list of tuples

def get_notices_for_individual(db: Session, registered_owner: str):
    """return all Notice records from Full_Notice view for a specific registered owner"""
    query = text("""
        SELECT *
        FROM Full_Notice
        WHERE RegisteredOwner = :registered_owner
        ORDER BY NoticeID ASC
    """)

    result = db.execute(query, {"registered_owner": registered_owner})    # execute query with provided parameter

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


def get_notice_by_id(db: Session, notice_id: int):
    """Return a single notice row from Full_Notice view by NoticeID as a dict, or None if not found."""
    query = text("""
        SELECT *
        FROM Full_Notice
        WHERE NoticeID = :notice_id
        LIMIT 1
    """)

    result = db.execute(query, {"notice_id": notice_id})   # execute query with bind param
    row = result.mappings().first()
    if not row:
        return None

    row = dict(row)
    # Ensure ActionSelection is returned as the action description string
    action_val = row.get("ActionSelection")
    if isinstance(action_val, int):
        action_row = db.query(Action).filter(Action.id == action_val).first()
        if action_row:
            row["ActionSelection"] = action_row.description
    elif isinstance(action_val, str):
        # already a description string - leave as-is
        pass
    else:
        try:
            coerced = int(action_val)
            action_row = db.query(Action).filter(Action.id == coerced).first()
            if action_row:
                row["ActionSelection"] = action_row.description
        except Exception:
            row["ActionSelection"] = None

    return row


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
        
        # resolve violation against predefined lookup table instead of creating a new record
        violation_row = db.query(Violation).filter(Violation.violation == notice_in.Violation).first()
        if not violation_row:
            # fallback to 'Unspecified' if the provided violation text is not in lookup
            violation_row = db.query(Violation).filter(Violation.violation == "Unspecified").first()
            if not violation_row:
                raise ValueError("Violation type not found and no 'Unspecified' lookup available")
        
        officer = Officer(
            officers_signature=notice_in.OfficersSignature,
            personnel_number=notice_in.PersonnelNumber,
        )
        db.add(officer)
        db.flush()
        
        # ensure ActionSelection references an existing action
        action_row = db.query(Action).filter(Action.id == notice_in.ActionSelection).first()
        if not action_row:
            raise ValueError("ActionSelection does not reference a valid Action")

        notice = Notice(
            individual_id=db.query(Individual).filter_by(first_name=notice_in.FirstName, last_name=notice_in.LastName).first().id,
            vehicle_id=vehicle.id,
            information_id=information.id,
            violation_id=violation_row.id,
            officer_id=officer.id,
            action_id=notice_in.ActionSelection,
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
            "ActionSelection": action_row.description if action_row else None,
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
    update_data = notice_in.model_dump(exclude_unset=True)

    # preload related objects
    individual = db.query(Individual).filter(Individual.id == notice.individual_id).first() if notice.individual_id else None
    vehicle = db.query(Vehicle).filter(Vehicle.id == notice.vehicle_id).first() if notice.vehicle_id else None
    information = db.query(Information).filter(Information.id == notice.information_id).first() if notice.information_id else None
    location = None
    if information and getattr(information, 'location_id', None):
        location = db.query(Location).filter(Location.id == information.location_id).first()
    officer = db.query(Officer).filter(Officer.id == notice.officer_id).first() if notice.officer_id else None

    # mapping of incoming field -> (target_object_name, attribute_name)
    field_map = {
        'FirstName': ('individual', 'first_name'),
        'LastName': ('individual', 'last_name'),
        'IndividualAddress': ('individual', 'address'),
        'City': ('individual', 'city'),
        'ResidenceState': ('individual', 'state_id'),
        'ZipCode': ('individual', 'zip_code'),
        'DriversLicense': ('individual', 'drivers_license'),
        'IssuedState': ('individual', 'state_issued_id'),
        'BirthDate': ('individual', 'birth_date'),
        'Height': ('individual', 'height'),
        'Weight': ('individual', 'weight'),
        'Eyes': ('individual', 'eyes'),

        'VehicleLicense': ('vehicle', 'vehicle_license'),
        'RegisteredState': ('vehicle', 'state_id'),
        'Colour': ('vehicle', 'colour'),
        'Year': ('vehicle', 'year'),
        'Make': ('vehicle', 'make'),
        'Type': ('vehicle', 'type'),
        'VIN': ('vehicle', 'vin'),
        'RegisteredOwner': ('vehicle', 'registered_owner'),
        'VehicleAddress': ('vehicle', 'address'),

        'ViolationDate': ('information', 'violation_date'),
        'District': ('information', 'district'),
        'Detachment': ('information', 'detachment'),

        'Miles': ('location', 'miles'),
        'Direction': ('location', 'direction'),
        'Town': ('location', 'town'),
        'Road': ('location', 'road'),

        'OfficersSignature': ('officer', 'officers_signature'),
        'PersonnelNumber': ('officer', 'personnel_number'),

        'ActionSelection': ('notice', 'action_id'),
        'DriversSignature': ('notice', 'drivers_signature'),
    }

    for key, val in update_data.items():
        if key == 'Violation':
            # resolve violation text to id
            if val:
                violation_row = db.query(Violation).filter(Violation.violation == val).first()
                if not violation_row:
                    violation_row = db.query(Violation).filter(Violation.violation == 'Unspecified').first()
                if violation_row:
                    notice.violation_id = violation_row.id
            continue

        mapping = field_map.get(key)
        if not mapping:
            # unknown field - ignore
            continue

        target_name, attr = mapping
        target = None
        if target_name == 'individual':
            target = individual
        elif target_name == 'vehicle':
            target = vehicle
        elif target_name == 'information':
            target = information
        elif target_name == 'location':
            target = location
        elif target_name == 'officer':
            target = officer
        elif target_name == 'notice':
            target = notice

        if not target:
            # target object not available - skip
            continue

        try:
            setattr(target, attr, val)
        except Exception:
            # ignore attribute errors and move on
            continue

    db.commit()
    db.refresh(notice)

    action_row = db.query(Action).filter(Action.id == notice.action_id).first() if notice.action_id else None

    return {
        'NoticeID': notice.id,
        'IndividualID': notice.individual_id,
        'VehicleID': notice.vehicle_id,
        'InformationID': notice.information_id,
        'ViolationID': notice.violation_id,
        'OfficerID': notice.officer_id,
        'ActionSelection': action_row.description if action_row else None,
        'DriversSignature': notice.drivers_signature,
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
    
    # resolve action description
    action_row = db.query(Action).filter(Action.id == notice.action_id).first() if notice.action_id else None

    return {                                                            # return updated notice as a dict compatible with Notice schema
        "NoticeID": notice.id,
        "IndividualID": notice.individual_id,
        "VehicleID": notice.vehicle_id,
        "InformationID": notice.information_id,
        "ViolationID": notice.violation_id,
        "OfficerID": notice.officer_id,
        "ActionSelection": action_row.description if action_row else None,
        "DriversSignature": notice.drivers_signature,
    }


def count_notices_total(db: Session):
    """Return total number of notices from Full_Notice view"""
    query = text("""
        SELECT COUNT(*) AS total
        FROM Full_Notice
    """)
    result = db.execute(query).scalar()
    return {"total": int(result or 0)}


def count_notices_by_violation(db: Session):
    """Return counts grouped by Violation (description)"""
    query = text("""
        SELECT Violation, COUNT(*) AS cnt
        FROM Full_Notice
        GROUP BY Violation
        ORDER BY cnt DESC
    """)
    rows = db.execute(query).mappings().all()
    return [{"violation": r.get("Violation"), "count": int(r.get("cnt", 0))} for r in rows]


def count_notices_by_district(db: Session):
    """Return counts grouped by District"""
    query = text("""
        SELECT District, COUNT(*) AS cnt
        FROM Full_Notice
        GROUP BY District
        ORDER BY District ASC
    """)
    rows = db.execute(query).mappings().all()
    return [{"district": r.get("District"), "count": int(r.get("cnt", 0))} for r in rows]


def count_notices_by_detachment(db: Session):
    """Return counts grouped by Detachment"""
    query = text("""
        SELECT Detachment, COUNT(*) AS cnt
        FROM Full_Notice
        GROUP BY Detachment
        ORDER BY Detachment ASC
    """)
    rows = db.execute(query).mappings().all()
    return [{"detachment": r.get("Detachment"), "count": int(r.get("cnt", 0))} for r in rows]


def delete_notice(db: Session, notice_id: int):
    """delete an existing Notice"""
    notice = db.query(Notice).filter(Notice.id == notice_id).first()    # get notice to be deleted

    if not notice:                                                      # ensure notice exists
        return None

    # resolve action description for response
    action_row = db.query(Action).filter(Action.id == notice.action_id).first() if notice.action_id else None

    deleted_notice = {
        "NoticeID": notice.id,
        "IndividualID": notice.individual_id,
        "VehicleID": notice.vehicle_id,
        "InformationID": notice.information_id,
        "ViolationID": notice.violation_id,
        "OfficerID": notice.officer_id,
        "ActionSelection": action_row.description if action_row else None,
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
    
    # resolve action description
    action_row = db.query(Action).filter(Action.id == notice.action_id).first() if notice.action_id else None

    return {                                                            # return updated notice as a dict compatible with Notice schema
        "NoticeID": notice.id,
        "IndividualID": notice.individual_id,
        "VehicleID": notice.vehicle_id,
        "InformationID": notice.information_id,
        "ViolationID": notice.violation_id,
        "OfficerID": notice.officer_id,
        "ActionSelection": action_row.description if action_row else None,
        "DriversSignature": notice.drivers_signature,
    }