from fastapi import FastAPI
app = FastAPI()
from db_raw import add_data, fetch_data

from pydantic import BaseModel # this import should already exist above; shown here for context
from typing import Optional # add this if you have not already imported Optional

"""
root GET endpoint displaying default message
"""
@app.get("/")
def root():
    return {"message": "this is the root endpoint message"}

"""
GET endpoint that retrieves data from the test_table table, uses the fetch_data function from db_raw.py
"""
@app.get("/test-db", status_code=200)
async def get_db_record(id: Optional[int] = None):
    if id is not None:
        row = fetch_data(id)
        return {"test_var": row[1], "test_var2": row[2]}
    else:
        rows = fetch_data()
        return {"test_var": rows[-1][1], "test_var2": rows[-1][2]}

"""
pydantic model to define the structure of the db for use in post endpoints
"""
class TestData(BaseModel):                                   # just the structure of the db
    test_var: int
    test_var2: int

"""
POST endpoint that creates a new record in the test_table table, uses the add_data function from db_raw.py
modifies: test_var and test_var2 fields
returns: newly created record with its assigned id
"""
@app.post("/test2-db", status_code=201)                     # path and status code
async def create_db_record(record: TestData):               # function to handle post request, asynchronous to allow for slow response from database
    new_id = add_data(                                      # adds new records to db using add_data function from db_raw.py
        test_var=record.test_var,                           # the records being added
        test_var2=record.test_var2,                         # ^ 
    )
    row = fetch_data(new_id)                                # fetches newly added records by id
    created = {
        "id": new_id,
        "test_var": row[1],
        "test_var2": row[2]
    }
    return created                                          # returns fetched records
