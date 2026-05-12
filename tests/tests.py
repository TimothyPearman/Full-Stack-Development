from fastapi.testclient import TestClient
from backend.app.core import token
from backend.main import app
from playwright.sync_api import sync_playwright
import uuid


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

    res = client.post("/user/create", data=user_data)
    assert res.status_code == 200
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


# user jouney test - driver/vehicle owner register
# registers account and logs in
def test_user_journey_civilian_register():
    # open browser
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # check info page
        page.goto("http://127.0.0.1:5500/index.html#info")
        assert "info" in page.url.lower()
        assert page.locator("body").is_visible()

        # check register page
        page.goto("http://127.0.0.1:5500/index.html#register")
        assert "register" in page.url.lower()
        assert page.locator("body").is_visible()

        page.route("**/user/create", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body='{"message":"created"}'
        ))

        # register
        register_username = f"journey_user_{uuid.uuid4().hex[:8]}"
        register_password = "Journey123"
        page.locator("#register-username").fill(register_username)
        page.locator("#register-password").fill(register_password)
        page.locator("#register-password-confirm").fill(register_password)
        page.locator("#register-full-name").fill("Journey User")
        page.locator("#register-dob").fill("1995-01-01")
        page.locator("#register-address").fill("1 Test Street")
        page.locator("#register-license-number").fill("JRN123456")
        page.locator("#register-license-postcode").fill("AB12 3CD")
        page.locator("#register-ni-number").fill("AB123456C")
        page.locator("#register-vehicle-registration").fill("JRN123")
        page.locator("#register-email").fill("journey.user@example.com")
        page.locator("#register-phone").fill("111-2222")
        page.locator("#user-register-btn").click()
        page.wait_for_function("window.location.hash === '#login'") # Wait for the URL hash to change to #login
        assert "#login" in page.url.lower()
        assert page.locator("#view-login").is_visible()

        browser.close()

# user jouney test - driver/vehicle owner login
# logs in, checks dashboard, updates contact info, logs out
def test_user_journey_civilian_login():
    # open browser
    with sync_playwright() as p: 
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # check info page
        page.goto("http://127.0.0.1:5500/index.html#info")
        assert "info" in page.url.lower()
        assert page.locator("body").is_visible()

        # check login page
        page.goto("http://127.0.0.1:5500/index.html#login")
        assert "login" in page.url.lower()
        assert page.locator("body").is_visible()

        # check user login page
        page.goto("http://127.0.0.1:5500/index.html#user-login")
        assert "user-login" in page.url.lower()
        assert page.locator("body").is_visible()

        # log in
        username_field = page.locator("#view-user-login #login-username")
        password_field = page.locator("#view-user-login #login-password")
        sign_in_button = page.locator("#user-login-btn")
        username_field.fill("John_Smith")
        password_field.fill("JPass")
        sign_in_button.click()
        page.wait_for_url("**/index.html#user-dash")  # Wait for redirect to dashboard
        assert "user-dash" in page.url.lower()
        assert page.locator("body").is_visible()


        # check dashboard
        page.goto("http://127.0.0.1:5500/index.html#user-dash")
        assert "user-dash" in page.url.lower()
        assert page.locator("body").is_visible()

        # check profile
        page.goto("http://127.0.0.1:5500/index.html#user-profile")
        assert "user-profile" in page.url.lower()
        assert page.locator("body").is_visible()

        # update contact info
        email_field = page.locator("#profile-email-input")
        phone_field = page.locator("#profile-phone-input")
        save_button = page.locator("#profile-update-btn")
        email_field.fill("userjourney.test@example.com")
        phone_field.fill("111-1111")
        save_button.click()
        page.wait_for_timeout(500)  # Wait a moment for the update to complete
        # Verify the updated contact info is displayed on the profile page
        assert page.locator("#profile-email").text_content() == "userjourney.test@example.com"
        assert page.locator("#profile-phone").text_content() == "111-1111"

        # logout
        logout_button = page.locator("#user-logout-btn")
        page.once("dialog", lambda dialog: dialog.accept())  # Accept the confirmation dialog
        logout_button.click()
        page.wait_for_timeout(500)  # Wait a moment for the logout to complete
        assert "#info" in page.url

        browser.close()

# user jouney test - admin login
# logs in, checks dashboard, creates notice, views notice, updates notice, deletes notice, logs out
def test_user_journey_admin_login():
    # open browser
    with sync_playwright() as p: 
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # check info page
        page.goto("http://127.0.0.1:5500/index.html#info")
        assert "info" in page.url.lower()
        assert page.locator("body").is_visible()

        # check login page
        page.goto("http://127.0.0.1:5500/index.html#login")
        assert "login" in page.url.lower()
        assert page.locator("body").is_visible()

        # check admin login page
        page.goto("http://127.0.0.1:5500/index.html#admin-login")
        assert "admin-login" in page.url.lower()
        assert page.locator("body").is_visible()

        # log in
        username_field = page.locator("#view-admin-login #login-username")
        password_field = page.locator("#view-admin-login #login-password")
        sign_in_button = page.locator("#admin-login-btn")
        username_field.fill("Timothy_Pearman")
        password_field.fill("TPass")
        sign_in_button.click()
        page.wait_for_url("**/index.html#admin-dash")  # Wait for redirect to dashboard
        assert "admin-dash" in page.url.lower()
        assert page.locator("body").is_visible()

        # check dashboard
        page.goto("http://127.0.0.1:5500/index.html#admin-dash")
        assert "admin-dash" in page.url.lower()
        assert page.locator("body").is_visible()

        # check management page
        page.goto("http://127.0.0.1:5500/index.html#admin-management")
        assert "admin-management" in page.url.lower()
        assert page.locator("body").is_visible()

        # check create page
        page.goto("http://127.0.0.1:5500/index.html#admin-management-create")
        assert "admin-management-create" in page.url.lower()
        assert page.locator("body").is_visible()

        # create
        page.locator("#create-first-name").fill("TestJourney")
        page.locator("#create-last-name").fill("Notice")
        page.locator("#create-individual-address").fill("1 Test Street")
        page.locator("#create-city").fill("Testville")
        page.locator("#create-residence-state").fill("1")
        page.locator("#create-zip-code").fill("12345")
        page.locator("#create-drivers-license").fill("D1234567")
        page.locator("#create-issued-state").fill("1")
        page.locator("#create-birth-date").fill("1990-01-01T00:00")
        page.locator("#create-height").fill("5'10\"")
        page.locator("#create-weight").fill("180")
        page.locator("#create-eyes").fill("Blue")
        page.locator("#create-vehicle-license").fill("ABC123")
        page.locator("#create-registered-state").fill("1")
        page.locator("#create-colour").fill("Black")
        page.locator("#create-year").fill("2020")
        page.locator("#create-make").fill("Honda")
        page.locator("#create-type").fill("Sedan")
        page.locator("#create-vin").fill("12345")
        page.locator("#create-registered-owner").fill("Test Owner")
        page.locator("#create-vehicle-address").fill("1 Test Street")
        page.locator("#create-violation-date").fill("2026-05-01T00:00")
        page.locator("#create-district").fill("1")
        page.locator("#create-detachment").fill("1")
        page.locator("#create-miles").fill("100")
        page.locator("#create-direction").fill("North")
        page.locator("#create-town").fill("Testville")
        page.locator("#create-road").fill("Main St")
        page.locator("#create-violation").fill("Speed")
        page.locator("#create-officers-signature").fill("TP")
        page.locator("#create-personnel-number").fill("1")
        page.locator("#create-action-selection").fill("1")
        page.locator("#admin-create-citation-btn").click()
        page.wait_for_timeout(500)  # Wait for create to complete
        assert page.locator("#view-admin-management-create").is_visible()

        # check view page
        page.goto("http://127.0.0.1:5500/index.html#admin-management-view")
        assert "admin-management-view" in page.url.lower()
        assert page.locator("body").is_visible()

        # view
        page.locator("#admin-view-citation-id").fill("1")
        page.locator("#admin-view-citation-record-btn").click()
        page.wait_for_timeout(500)
        assert page.locator("#view-admin-management-view").is_visible()

        # check update page
        page.goto("http://127.0.0.1:5500/index.html#admin-management-update")
        assert "admin-management-update" in page.url.lower()

        #update
        assert page.locator("body").is_visible()
        page.locator("#update-citation-id").fill("1")
        page.locator("#update-first-name").fill("Updated")
        page.locator("#update-violation").fill("Reckless")
        page.locator("#admin-update-citation-btn").click()
        page.wait_for_timeout(500)
        assert page.locator("#view-admin-management-update").is_visible()

        # check delete page
        page.goto("http://127.0.0.1:5500/index.html#admin-management-delete")
        assert "admin-management-delete" in page.url.lower()
        assert page.locator("body").is_visible()

        #delete
        page.locator("#admin-delete-citation-id").fill("1")
        page.locator("#admin-delete-citation-record-btn").click()
        page.wait_for_timeout(500)
        assert page.locator("#view-admin-management-delete").is_visible()

        # logout
        logout_button = page.locator("#admin-logout-btn")
        page.once("dialog", lambda dialog: dialog.accept())  # Accept the confirmation dialog
        logout_button.click()
        page.wait_for_timeout(500)  # Wait a moment for the logout to complete
        assert "#info" in page.url

        browser.close()