import MySQLdb

"""
method to establish and return a connection to the MySQL database
"""
def get_connection():
    conn = MySQLdb.connect(                                 # predefined parameters for connecting to the database
        host="localhost",
        port=3306,
        user="root",                                        # the MySQL user
        passwd="",
        db="test_db",                                       # database name
        charset="utf8mb4"
        )
    return conn

"""
method to fetch data from a database table (specifically the test_table table rn for...testing...what did you expect, why are you reading this)
"""
def fetch_data(id: int = None):
    conn = get_connection()                                 # establish connection to database
    cursor = conn.cursor()                                  # create a cursor object to interact with the database
    if id is not None:                                      # if an id is provided, fetch the specific row
        query = "SELECT * from test_table WHERE id = %s"    # predefined sql query to fetch a specific row by id
        cursor.execute(query, (id,))                        # execute the query with the provided id parameter
        row = cursor.fetchone()                             # fetch the single row result#
    else:                                                   # else, do the same shit but for all rows since no id was specified
        query = "SELECT * from test_table"
        cursor.execute(query)
        row = cursor.fetchall()
    cursor.close()                                          # close the cursor object
    conn.close()                                            # close the database connection
    
    return row                                              # return fetched data :D

"""
method to add data to a database table (again, the test_table table for testing purposes)
"""
def add_data(test_var: int, test_var2: int):
    conn = get_connection()                                 # ^ same as above method
    cursor = conn.cursor()                                  # ^
    query = """ 
        INSERT INTO test_table (test_var, test_var2) 
        VALUES (%s, %s);
    """                                                     # ^
    cursor.execute(query, (test_var, test_var2))            # ^
    conn.commit()                                           # commit the transaction to save changes to the database
    new_id = cursor.lastrowid                               # get the id of the newly inserted row
    cursor.close()                                          # ^
    conn.close()                                            # ^
    return new_id                                           # ^