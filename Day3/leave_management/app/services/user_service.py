from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.user_repo import (
    get_user_by_id,
    get_all_users,
    get_users_by_department,
    update_user,
    delete_user,
    get_user_by_email
)
from app.repositories.department_repo import get_department_by_id
from app.core.security import hash_password


# -----------------------------
# Get All Users (Admin)
# -----------------------------

def get_all_users_service(db: Session):
    return get_all_users(db)


# -----------------------------
# Get User by ID
# -----------------------------

def get_user_by_id_service(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# -----------------------------
# Get Department Employees (Manager)
# -----------------------------

def get_department_employees_service(db: Session, department_id: int):
    department = get_department_by_id(db, department_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return get_users_by_department(db, department_id)


# -----------------------------
# Update User
# -----------------------------

def update_user_service(db: Session, user_id: int, update_data: dict):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check email uniqueness if updating email
    if update_data.get("email"):
        existing = get_user_by_email(db, update_data["email"])
        if existing and existing.id != user_id:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash password if updating
    if update_data.get("password"):
        update_data["password"] = hash_password(update_data["password"])
    
    return update_user(db, user, update_data)


# -----------------------------
# Delete User (Admin)
# -----------------------------

def delete_user_service(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    delete_user(db, user)
    return {"message": "User deleted successfully"}


# -----------------------------
# Assign User to Department (Admin)
# -----------------------------

def assign_user_to_department_service(db: Session, user_id: int, department_id: int):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    department = get_department_by_id(db, department_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    
    return update_user(db, user, {"department_id": department_id})
