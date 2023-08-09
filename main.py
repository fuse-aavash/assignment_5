from fastapi import FastAPI, HTTPException
from typing import List

from models import Employee
import database as database

app = FastAPI()

@app.on_event("startup")
def startup_event():
    """
    Event handler that runs when the FastAPI application starts.

    This function calls the 'create_table' function from the 'database' module to create the 'employees' table if it doesn't exist.
    """
    database.create_table()

@app.get("/employees/", response_model=List[Employee])
def read_employees(skip: int = 0, limit: int = 10):
    """
    Retrieve a list of Employee objects from the 'employees' table.

    Parameters:
    - skip: int (optional): The number of rows to skip from the beginning of the table.
    - limit: int (optional): The maximum number of rows to retrieve.

    Returns:
    - List[Employee]: A list of Employee objects retrieved from the database.
    """
    return database.get_employees(skip, limit)

@app.get("/employees/{employee_id}", response_model=Employee)
def read_employee(employee_id: int):
    """
    Retrieve a single Employee object from the 'employees' table based on the given employee_id.

    Parameters:
    - employee_id: int: The ID of the employee to retrieve.

    Returns:
    - Employee: An Employee object if the employee_id exists in the database, otherwise raises HTTPException with status_code 404 and detail "Employee not found".
    """
    employee = database.get_employee(employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@app.post("/employees/", response_model=Employee)
def create_employee(employee: Employee):
    """
    Insert a new Employee object into the 'employees' table.

    Parameters:
    - employee: Employee: The Employee object to be inserted into the database.

    Returns:
    - Employee: The newly created Employee object with the assigned ID from the database.
    """
    return database.insert_employee(employee)

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    """
    Delete an Employee record from the 'employees' table based on the given employee_id.

    Parameters:
    - employee_id: int: The ID of the employee to delete.

    Returns:
    - dict: A dictionary with a "message" key indicating the status of the operation. Raises HTTPException with status_code 404 and detail "Employee not found" if the employee does not exist.
    """
    if not database.delete_employee(employee_id):
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted"}

@app.put("/employees/{employee_id}/{column}/{new_value}")
def update_employee(employee_id: int, column: str, new_value: str):
    """
    Update the value of a specific column for a given employee in the 'employees' table.

    Parameters:
    - employee_id: int: The ID of the employee to update.
    - column: str: The name of the column to update ('name' or 'department').
    - new_value: str: The new value to be set for the specified column.

    Returns:
    - dict: A dictionary with a "message" key indicating the status of the operation. Raises HTTPException with status_code 404 and detail "Employee not found" if the employee does not exist.
    """
    if not database.update_employee(employee_id, column, new_value):
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee updated"}
