from fastapi.testclient import TestClient
from backend.app.core import token
from backend.main import app

client = TestClient(app)

# test the backend is running
def test_root_returns_ok():
    res = client.get("/")
    assert res.status_code == 200
    body = res.json()
    assert body["message"] == "assessment 3 API is working, yippee!"

def test_health_returns_ok():
    res = client.get("/health")
    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "ok"

def test_docs_returns_ok():
    res = client.get("/docs")
    assert res.status_code == 200

def test_openapi_returns_ok():
    res = client.get("/openapi.json")
    assert res.status_code == 200

def test_nonexistent_endpoint_returns_404():
    res = client.get("/this-endpoint-does-not-exist")
    assert res.status_code == 404


# happy path - test token endpoint with valid civilian credentials
def test_token_valid_Civilian():
    user_data = {
        "username": "John_Smith",
        "password": "JPass"
    }
    res = client.post("/user/token", data=user_data)
    assert res.status_code == 200
    body = res.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"
# happy path - test token endpoint with valid officer credentials
def test_token_valid_officer():
    user_data = {
        "username": "Timothy_Pearman",
        "password": "TPass"
    }
    res = client.post("/user/token", data=user_data)
    assert res.status_code == 200
    body = res.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"
#! failure path -  test token endpoint with correct username and incorrect password for existing civilian user
def test_token_invalid_password():
    user_data = {
        "username": "John_Smith",
        "password": "WrongPassword"
    }
    res = client.post("/user/token", data=user_data)
    assert res.status_code == 401
#! failure path -  test token endpoint with invalid credentials
def test_token_invalid():
    user_data = {
        "username": "IDontExist",
        "password": "WrongPassword"
    }
    res = client.post("/user/token", data=user_data)
    assert res.status_code == 401
#! failure path - test token endpoint with missing and empty fields
def test_token_missing_fields():
    user_data = {
        "username": ""
    }
    res = client.post("/user/token", data=user_data)
    assert res.status_code == 422

# happy path - test token refresh endpoint with valid token
def test_token_refresh_valid():
    user_data = {
        "username": "Timothy_Pearman",
        "password": "TPass"
    }
    res = client.post("/user/token", data=user_data)
    assert res.status_code == 200
    body = res.json()
    assert "access_token" in body
    token = body["access_token"]

    refresh_res = client.put("/user/token", headers={"Authorization": f"Bearer {token}"})
    assert refresh_res.status_code == 200
    refresh_body = refresh_res.json()
    assert "access_token" in refresh_body  
#! failure path - test token refresh endpoint with invalid token
def test_token_refresh_invalid():
    refresh_res = client.put("/user/token", headers={"Authorization": "Bearer InvalidToken"})
    assert refresh_res.status_code == 401

# happy path - test token delete endpoint with valid token
def test_token_delete_valid():
    user_data = {
        "username": "John_Smith",
        "password": "JPass"
    }
    res = client.post("/user/token", data=user_data)
    assert res.status_code == 200
    body = res.json()
    assert "access_token" in body
    token = body["access_token"]

    delete_res = client.delete("/user/token", headers={"Authorization": f"Bearer {token}"})
    assert delete_res.status_code == 200
    delete_body = delete_res.json()
    assert delete_body["message"] == "Token revoked successfully"

# happy path - test get user endpoint with valid token
def test_get_user_valid():
    user_data = {
        "username": "John_Smith",
        "password": "JPass"
    }
    res = client.post("/user/token", data=user_data)
    assert res.status_code == 200
    body = res.json()
    assert "access_token" in body
    token = body["access_token"]

    get_res = client.get("/user/get", headers={"Authorization": f"Bearer {token}"})
    assert get_res.status_code == 200
    get_body = get_res.json()
    assert get_body["Username"] == "John_Smith"
    assert get_body["Clearance"] == "Civilian"
#! failure path - test get user endpoint with invalid token
def test_get_user_invalid_token():
    get_res = client.get("/user/get", headers={"Authorization": "Bearer InvalidToken"})
    assert get_res.status_code == 401

# happy path - test get clearance endpoint with valid credentials
def test_get_clearance_valid():
    user_data = {
        "username": "John_Smith",
        "password": "JPass"
    }
    res = client.post("/user/clearance", data=user_data)
    assert res.status_code == 200
    body = res.json()
    assert body["clearance"] == "Civilian"
#! failure path - test get clearance endpoint with invalid credentials
def test_get_clearance_invalid():
    user_data = {
        "username": "John_Smith",
        "password": "WrongPassword"
    }
    res = client.post("/user/clearance", data=user_data)
    assert res.status_code == 401

"""
# happy path - test create user endpoint with valid data
def test_create_user_valid():
    user_data = {
        "username": "TestUser",
        "password": "TestPassword123",
        "clearance": "Civilian",
        "fullName": "",
        "dateOfBirth": "",
        "currentAddress": "",
        "driverLicenseNumber": "",
        "postcode": "",
        "nationalInsurance": "",
        "vehicleRegNumber": "",
        "email": "",
        "phone": ""
    }

    res = client.post("/user/create", data=user_data)  # <-- FIXED
    assert res.status_code == 200
"""
#! failure path - test create user endpoint with existing username
def test_create_user_existing_username():
    user_data = {
        "username": "John_Smith",
        "password": "AnotherPassword123",
        "clearance": "Civilian"
    }
    res = client.post("/user/create", data=user_data)
    assert res.status_code == 409
#! failure path - test create user endpoint with invalid clearance
def test_create_user_invalid_clearance():
    user_data = {
        "username": "testuser1",
        "password": "TestPassword123",
        "clearance": "InvalidClearance"
    }
    res = client.post("/user/create", data=user_data)
    assert res.status_code == 400
#! failure path - test create user endpoint with invalid password 
def test_create_user_invalid_password():
    user_data = {
        "username": "testuser",
        "password": "",
        "clearance": "Civilian"
    }
    res = client.post("/user/create", data=user_data)
    assert res.status_code == 422

# happy path - test update user endpoint with valid data
def test_update_user_valid():
    user_data = {
        "username": "John_Smith",
        "password": "JPass"
    }
    res = client.post("/user/token", data=user_data)
    assert res.status_code == 200
    body = res.json()
    assert "access_token" in body
    token = body["access_token"]

    update_data = {
        "fullName": "John Smith",
        "dateOfBirth": "1990-01-01",
        "currentAddress": "123 Main St",
        "driverLicenseNumber": "D1234567",
        "postcode": "12345",
        "nationalInsurance": "AB123456C",
        "vehicleRegNumber": "ABC123",
        "email": "john.smith@example.com",
        "phone": "555-1234"
    }
    update_res = client.put("/user/update", headers={"Authorization": f"Bearer {token}"}, data=update_data)
    assert update_res.status_code == 200
#! failure path - test update user endpoint with invalid token
def test_update_user_invalid_token():
    update_data = {
        "fullName": "John Smith",
        "dateOfBirth": "1990-01-01",
        "currentAddress": "123 Main St",
        "driverLicenseNumber": "D1234567",
        "postcode": "12345",
        "nationalInsurance": "AB123456C",
        "vehicleRegNumber": "ABC123",
        "email": "john.smith@example.com",
        "phone": "555-1234"
    }
    update_res = client.put("/user/update", headers={"Authorization": "Bearer InvalidToken"}, data=update_data)
    assert update_res.status_code == 401

# happy path - test get notice endpoint with valid token and existing notice
def test_get_notice_valid():
    user_data = {
        "username": "John_Smith",
        "password": "JPass",
        "grant_type": ""
    }

    # Authenticate
    res = client.post("/user/token", data=user_data)
    assert res.status_code == 200
    token = res.json()["access_token"]

    # Fetch notices
    get_res = client.get("/notices/me", headers={"Authorization": f"Bearer {token}"})
    assert get_res.status_code == 200

    notices = get_res.json()
    assert isinstance(notices, list)
    assert len(notices) > 0
    assert notices[0]["NoticeID"] == 2
#! failure path - test get notice endpoint with invalid token
def test_get_notice_invalid_token():
    get_res = client.get("/notices/me", headers={"Authorization": "Bearer InvalidToken"})
    assert get_res.status_code == 401


# happy path - test get notice by id endpoint with valid token and existing notice
def test_get_notice_by_id_valid():
    user_data = {
        "username": "Timothy_Pearman",
        "password": "TPass",
    }

    # Authenticate
    res = client.post("/user/token", data=user_data)
    assert res.status_code == 200
    token = res.json()["access_token"]

    # Fetch notice by ID
    get_res = client.get("/notices/2", headers={"Authorization": f"Bearer {token}"})
    assert get_res.status_code == 200

    notice = get_res.json()
    assert notice["NoticeID"] == 2
#! failure path - test get notice by id endpoint with invalid token
def test_get_notice_by_id_invalid_token():
    get_res = client.get("/notices/2", headers={"Authorization": "Bearer InvalidToken"})
    assert get_res.status_code == 401
#! failure path - test get notice by id endpoint with valid token but non-existent notice
def test_get_notice_by_id_nonexistent():
    user_data = {
        "username": "Timothy_Pearman",
        "password": "TPass",
    }

    # Authenticate
    res = client.post("/user/token", data=user_data)
    assert res.status_code == 200
    token = res.json()["access_token"]

    # Fetch non-existent notice by ID
    get_res = client.get("/notices/9999", headers={"Authorization": f"Bearer {token}"})
    assert get_res.status_code == 404


# happy path - test update notice endpoint with valid token, existing notice, and valid data
def test_update_notice_valid():
    user_data = {
        "username": "Timothy_Pearman",
        "password": "TPass",
    }

    # Authenticate
    res = client.post("/user/token", data=user_data)
    assert res.status_code == 200
    token = res.json()["access_token"]

    # Update notice
    update_data = {
        "FirstName": "a",
        "LastName": "a",
        "IndividualAddress": "a",
        "City": "a",
        "ResidenceState": 1,
        "ZipCode": "a",
        "DriversLicense": "a",
        "IssuedState": 1,
        "BirthDate": "2026-05-10T22:20:39.007Z",
        "Height": "a",
        "Weight": 1,
        "Eyes": "a",
        "VehicleLicense": "a",
        "RegisteredState": 1,
        "Colour": "a",
        "Year": 1,
        "Make": "a",
        "Type": "a",
        "VIN": 1,
        "RegisteredOwner": "a",
        "VehicleAddress": "a",
        "ViolationDate": "2026-05-10T22:20:39.007Z",
        "District": 1,
        "Detachment": 1,
        "Miles": 1,
        "Direction": "a",
        "Town": "a",
        "Road": "a",
        "Violation": "a",
        "OfficersSignature": "a",
        "PersonnelNumber": 1,
        "ActionSelection": 1,
        "DriversSignature": "a"
    }
    update_res = client.put("/notices/1", headers={"Authorization": f"Bearer {token}"}, json=update_data)
    assert update_res.status_code == 200
#! failure path - test update notice endpoint with valid token, existing notice, but invalid data
def test_update_notice_invalid_data():
    user_data = {
        "username": "Timothy_Pearman",
        "password": "TPass",
    }

    # Authenticate
    res = client.post("/user/token", data=user_data)
    assert res.status_code == 200
    token = res.json()["access_token"]

    # Update notice with invalid data
    update_data = {
        "FirstName": "a",
        "LastName": "a",
        "IndividualAddress": "a",
        "City": "a",
        "ResidenceState": "a",
        "ZipCode": "a",
        "DriversLicense": "a",
        "IssuedState": "a",
        "BirthDate": "a",
        "Height": "a",
        "Weight": "a",
        "Eyes": "a",
        "VehicleLicense": "a",
        "RegisteredState": "a",
        "Colour": "a",
        "Year": "a",
        "Make": "a",
        "Type": "a",
        "VIN": "a",
        "RegisteredOwner": "a",
        "VehicleAddress": "a",
        "ViolationDate": "2026-05-10T22:20:39.007Z",
        "District": "a",
        "Detachment": "a",
        "Miles": "a",
        "Direction": "a",
        "Town": "a",
        "Road": "a",
        "Violation": "a",
        "OfficersSignature": "a",
        "PersonnelNumber": "a",
        "ActionSelection": "a",
        "DriversSignature": "a"
    }
    update_res = client.put("/notices/2", headers={"Authorization": f"Bearer {token}"}, json=update_data)
    assert update_res.status_code == 422
#! failure path - test update notice endpoint with invalid token
def test_update_notice_invalid_token():
    update_data = {
        "FirstName": "a",
        "LastName": "a",
        "IndividualAddress": "a",
        "City": "a",
        "ResidenceState": 1,
        "ZipCode": "a",
        "DriversLicense": "a",
        "IssuedState": 1,
        "BirthDate": "2026-05-10T22:20:39.007Z",
        "Height": "a",
        "Weight": 1,
        "Eyes": "a",
        "VehicleLicense": "a",
        "RegisteredState": 1,
        "Colour": "a",
        "Year": 1,
        "Make": "a",
        "Type": "a",
        "VIN": 1,
        "RegisteredOwner": "a",
        "VehicleAddress": "a",
        "ViolationDate": "2026-05-10T22:20:39.007Z",
        "District": 1,
        "Detachment": 1,
        "Miles": 1,
        "Direction": "a",
        "Town": "a",
        "Road": "a",
        "Violation": "a",
        "OfficersSignature": "a",
        "PersonnelNumber": 1,
        "ActionSelection": 1,
        "DriversSignature": "a"
    }
    update_res = client.put("/notices/2", headers={"Authorization": "Bearer InvalidToken"}, json=update_data)
    assert update_res.status_code == 401
#! failure path - test update notice endpoint with valid token but non-existent notice
def test_update_notice_nonexistent():
    user_data = {
        "username": "Timothy_Pearman",
        "password": "TPass",
    }

    # Authenticate
    res = client.post("/user/token", data=user_data)
    assert res.status_code == 200
    token = res.json()["access_token"]

    # Update non-existent notice
    update_data = {
        "FirstName": "a",
        "LastName": "a",
        "IndividualAddress": "a",
        "City": "a",
        "ResidenceState": 1,
        "ZipCode": "a",
        "DriversLicense": "a",
        "IssuedState": 1,
        "BirthDate": "2026-05-10T22:20:39.007Z",
        "Height": "a",
        "Weight": 1,
        "Eyes": "a",
        "VehicleLicense": "a",
        "RegisteredState": 1,
        "Colour": "a",
        "Year": 1,
        "Make": "a",
        "Type": "a",
        "VIN": 1,
        "RegisteredOwner": "a",
        "VehicleAddress": "a",
        "ViolationDate": "2026-05-10T22:20:39.007Z",
        "District": 1,
        "Detachment": 1,
        "Miles": 1,
        "Direction": "a",
        "Town": "a",
        "Road": "a",
        "Violation": "a",
        "OfficersSignature": "a",
        "PersonnelNumber": 1,
        "ActionSelection": 1,
        "DriversSignature": "a"
    }
    update_res = client.put("/notices/9999", headers={"Authorization": f"Bearer {token}"}, json=update_data)
    assert update_res.status_code == 404

"""
# happy path - test delete notice endpoint with valid token and valid data
def test_delete_notice_valid():
    user_data = {
        "username": "Timothy_Pearman",
        "password": "TPass",
    }

    # Authenticate
    res = client.post("/user/token", data=user_data)
    assert res.status_code == 200
    token = res.json()["access_token"]

    # Delete notice
    delete_res = client.delete("/notices/1", headers={"Authorization": f"Bearer {token}"})
    assert delete_res.status_code == 200
#! failure path - test delete notice endpoint with invalid token
def test_delete_notice_invalid_token():
    delete_res = client.delete("/notices/2", headers={"Authorization    ": "Bearer InvalidToken"})
    assert delete_res.status_code == 401
#! failure path - test delete notice endpoint with valid token but non-existent notice
def test_delete_notice_nonexistent():
    user_data = {
        "username": "Timothy_Pearman",
        "password": "TPass",
    }

    # Authenticate
    res = client.post("/user/token", data=user_data)
    assert res.status_code == 200
    token = res.json()["access_token"]

    # Delete non-existent notice
    delete_res = client.delete("/notices/9999", headers={"Authorization": f"Bearer {token}"})
    assert delete_res.status_code == 404
"""

# happy path - test create notice endpoint with valid token and valid data
def test_create_notice_valid():
    user_data = {
        "username": "Timothy_Pearman",
        "password": "TPass",
    }

    # Authenticate
    res = client.post("/user/token", data=user_data)
    assert res.status_code == 200
    token = res.json()["access_token"]

    # Create notice
    notice_data = {
        "FirstName": "a",
        "LastName": "a",
        "IndividualAddress": "a",
        "City": "a",
        "ResidenceState": 1,
        "ZipCode": "a",
        "DriversLicense": "a",
        "IssuedState": 1,
        "BirthDate": "2026-05-10T22:20:39.007Z",
        "Height": "a",
        "Weight": 1,
        "Eyes": "a",
        "VehicleLicense": "a",
        "RegisteredState": 1,
        "Colour": "a",
        "Year": 1,
        "Make": "a",
        "Type": "a",
        "VIN": 1,
        "RegisteredOwner": "a",
        "VehicleAddress": "a",
        "ViolationDate": "2026-05-10T22:20:39.007Z",
        "District": 1,
        "Detachment": 1,
        "Miles": 1,
        "Direction": "a",
        "Town": "a",
        "Road": "a",
        "Violation": "a",
        "OfficersSignature": "a",
        "PersonnelNumber": 1,
        "ActionSelection": 1,
        "DriversSignature": ""
    }
    create_res = client.post("/notices/create", headers={"Authorization": f"Bearer {token}"}, json=notice_data)
    assert create_res.status_code == 201
#! failure path - test create notice endpoint with invalid token
def test_create_notice_invalid_token():
    notice_data = {
        "FirstName": "a",
        "LastName": "a",
        "IndividualAddress": "a",
        "City": "a",
        "ResidenceState": 1,
        "ZipCode": "a",
        "DriversLicense": "a",
        "IssuedState": 1,
        "BirthDate": "2026-05-10T22:20:39.007Z",
        "Height": "a",
        "Weight": 1,
        "Eyes": "a",
        "VehicleLicense": "a",
        "RegisteredState": 1,
        "Colour": "a",
        "Year": 1,
        "Make": "a",
        "Type": "a",
        "VIN": 1,
        "RegisteredOwner": "a",
        "VehicleAddress": "a",
        "ViolationDate": "2026-05-10T22:20:39.007Z",
        "District": 1,
        "Detachment": 1,
        "Miles": 1,
        "Direction": "a",
        "Town": "a",
        "Road": "a",
        "Violation": "a",
        "OfficersSignature": "a",
        "PersonnelNumber": 1,
        "ActionSelection": 1,
        "DriversSignature": ""
    }
    create_res = client.post("/notices/create", headers={"Authorization    ": f"Bearer InvalidToken"}, json=notice_data)
    assert create_res.status_code == 401
#! failure path - test create notice endpoint with valid token but invalid data
def test_create_notice_invalid_data():
    user_data = {
        "username": "Timothy_Pearman",
        "password": "TPass",
    }
    res = client.post("/user/token", data=user_data)
    assert res.status_code == 200
    token = res.json()["access_token"]

    # Create notice with invalid data
    notice_data = {
        "FirstName": "a",
        "LastName": "a",
        "IndividualAddress": "a",
        "City": "a",
        "ResidenceState": 1,
        "ZipCode": "a",
        "DriversLicense": "a",
        "IssuedState": 1,
        "BirthDate": "2026-05-10T22:20:39.007Z",
        "Height": "a",
        "Weight": 1,
        "Eyes": "a",
        "VehicleLicense": "a",
        "RegisteredState": 1,
        "Colour": "a",
        "Year": 1,
        "Make": "a",
        "Type": "a",
        "VIN": 1,
        "RegisteredOwner": "a",
        "VehicleAddress": "a",
        "ViolationDate": "2026-05-10T22:20:39.007Z",
        "District": 1,
        "Detachment": 1,
        "Miles": 1,
        "Direction": "a",
        # Invalid data - missing required fields
    }
    create_res = client.post("/notices/create", headers={"Authorization": f"Bearer {token}"}, json=notice_data)
    assert create_res.status_code == 422

# happy path - test get notice count endpoint with valid token
def test_get_notice_count_valid():
    user_data = {
        "username": "Timothy_Pearman",
        "password": "TPass",
    }
    res = client.post("/user/token", data=user_data)
    assert res.status_code == 200
    token = res.json()["access_token"]

    count_res = client.get("/notices/counts/total", headers={"Authorization": f"Bearer {token}"})
    assert count_res.status_code == 200
#! failure path - test get notice count endpoint with invalid token
def test_get_notice_count_invalid_token():
    count_res = client.get("/notices/counts/total", headers={"Authorization": "Bearer InvalidToken"})
    assert count_res.status_code == 401

# happy path - test get notice count by violation type endpoint with valid token and existing notice type
def test_get_notice_count_by_violation_type_valid():
    user_data = {
        "username": "Timothy_Pearman",
        "password": "TPass",
    }
    res = client.post("/user/token", data=user_data)
    assert res.status_code == 200
    token = res.json()["access_token"]

    count_res = client.get("/notices/counts/by-violation", headers={"Authorization": f"Bearer {token}"})
    assert count_res.status_code == 200

    body = count_res.json()
    assert isinstance(body, list)
    assert len(body) > 0
    assert "violation" in body[0]
    assert "count" in body[0]
#! failure path - test get notice count by violation type endpoint with invalid token
def test_get_notice_count_by_violation_type_invalid_token():
    count_res = client.get("/notices/counts/by-violation", headers={"Authorization": "Bearer InvalidToken"})
    assert count_res.status_code == 401

# happy path - test get notice count by district type endpoint with valid token
def test_get_notice_count_by_district_type_valid():
    user_data = {
        "username": "Timothy_Pearman",
        "password": "TPass",
    }
    res = client.post("/user/token", data=user_data)
    assert res.status_code == 200
    token = res.json()["access_token"]

    count_res = client.get("/notices/counts/by-district", headers={"Authorization": f"Bearer {token}"})
    assert count_res.status_code == 200

    body = count_res.json()
    assert isinstance(body, list)
    assert len(body) > 0
    assert "district" in body[0]
    assert "count" in body[0]
#! failure path - test get notice count by district type endpoint with invalid token
def test_get_notice_count_by_district_type_invalid_token():
    count_res = client.get("/notices/counts/by-district", headers={"Authorization": "Bearer InvalidToken"})
    assert count_res.status_code == 401

# happy path - test get notice count by detachment type endpoint with valid token
def test_get_notice_count_by_detachment_type_valid():
    user_data = {
        "username": "Timothy_Pearman",
        "password": "TPass",
    }
    res = client.post("/user/token", data=user_data)
    assert res.status_code == 200
    token = res.json()["access_token"]

    count_res = client.get("/notices/counts/by-detachment", headers={"Authorization": f"Bearer {token}"})
    assert count_res.status_code == 200

    body = count_res.json()
    assert isinstance(body, list)
    assert len(body) > 0
    assert "detachment" in body[0]
    assert "count" in body[0]
#! failure path - test get notice count by detachment type endpoint with invalid token
def test_get_notice_count_by_detachment_type_invalid_token():
    count_res = client.get("/notices/counts/by-detachment", headers={"Authorization": "Bearer InvalidToken"})
    assert count_res.status_code == 401