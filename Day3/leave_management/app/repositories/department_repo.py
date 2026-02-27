# department_repo.py

from sqlalchemy.orm import Session
from app.models.department import Department


# Create Department
def create_department(db: Session, department_data: dict) -> Department:
    db_department = Department(**department_data)
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department


# Get Department by ID
def get_department_by_id(db: Session, department_id: int) -> Department:
    return db.query(Department).filter(Department.id == department_id).first()


# Get Department by Name
def get_department_by_name(db: Session, name: str) -> Department:
    return db.query(Department).filter(Department.name == name).first()


# Get All Departments
def get_all_departments(db: Session) -> list[Department]:
    return db.query(Department).all()


# Get Department by Manager ID
def get_department_by_manager(db: Session, manager_id: int) -> Department:
    return db.query(Department).filter(Department.manager_id == manager_id).first()


# Update Department
def update_department(db: Session, department: Department, update_data: dict) -> Department:
    for key, value in update_data.items():
        if value is not None:
            setattr(department, key, value)
    db.commit()
    db.refresh(department)
    return department


# Delete Department
def delete_department(db: Session, department: Department):
    db.delete(department)
    db.commit()
