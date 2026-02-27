from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.department_repo import (
    create_department,
    get_department_by_id,
    get_department_by_name,
    get_all_departments,
    update_department,
    delete_department,
    get_department_by_manager
)
from app.repositories.user_repo import get_user_by_id


# -----------------------------
# Create Department (Admin)
# -----------------------------

def create_department_service(db: Session, department_data: dict):
    # Check if department name already exists
    existing = get_department_by_name(db, department_data["name"])
    if existing:
        raise HTTPException(status_code=400, detail="Department name already exists")
    
    # Validate manager if provided
    if department_data.get("manager_id"):
        manager = get_user_by_id(db, department_data["manager_id"])
        if not manager:
            raise HTTPException(status_code=404, detail="Manager not found")
        if manager.role != "MANAGER":
            raise HTTPException(status_code=400, detail="User is not a manager")
    
    return create_department(db, department_data)


# -----------------------------
# Get All Departments
# -----------------------------

def get_all_departments_service(db: Session):
    return get_all_departments(db)


# -----------------------------
# Get Department by ID
# -----------------------------

def get_department_by_id_service(db: Session, department_id: int):
    department = get_department_by_id(db, department_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department


# -----------------------------
# Update Department (Admin)
# -----------------------------

def update_department_service(db: Session, department_id: int, update_data: dict):
    department = get_department_by_id(db, department_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    
    # Check name uniqueness if updating name
    if update_data.get("name"):
        existing = get_department_by_name(db, update_data["name"])
        if existing and existing.id != department_id:
            raise HTTPException(status_code=400, detail="Department name already exists")
    
    # Validate manager if updating
    if update_data.get("manager_id"):
        manager = get_user_by_id(db, update_data["manager_id"])
        if not manager:
            raise HTTPException(status_code=404, detail="Manager not found")
        if manager.role != "MANAGER":
            raise HTTPException(status_code=400, detail="User is not a manager")
    
    return update_department(db, department, update_data)


# -----------------------------
# Assign Manager to Department (Admin)
# -----------------------------

def assign_manager_service(db: Session, department_id: int, manager_id: int):
    department = get_department_by_id(db, department_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    
    manager = get_user_by_id(db, manager_id)
    if not manager:
        raise HTTPException(status_code=404, detail="User not found")
    
    if manager.role != "MANAGER":
        raise HTTPException(status_code=400, detail="User is not a manager")
    
    # Check if manager already manages another department
    existing_dept = get_department_by_manager(db, manager_id)
    if existing_dept and existing_dept.id != department_id:
        raise HTTPException(status_code=400, detail="Manager already assigned to another department")
    
    return update_department(db, department, {"manager_id": manager_id})


# -----------------------------
# Delete Department (Admin)
# -----------------------------

def delete_department_service(db: Session, department_id: int):
    department = get_department_by_id(db, department_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    
    # Check if department has employees
    if department.employees:
        raise HTTPException(status_code=400, detail="Cannot delete department with employees")
    
    delete_department(db, department)
    return {"message": "Department deleted successfully"}
