from sqlalchemy.orm import Session
from app.models.department import Department
from app.schemas.department_schema import DepartmentCreate, DepartmentUpdate
from typing import Optional, List

class DepartmentRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_department(self, dept_data: DepartmentCreate) -> Department:
        department = Department(**dept_data.model_dump())
        self.db.add(department)
        self.db.commit()
        self.db.refresh(department)
        return department
    
    def get_department_by_id(self, dept_id: int) -> Optional[Department]:
        return self.db.query(Department).filter(Department.id == dept_id).first()
    
    def get_department_by_name(self, name: str) -> Optional[Department]:
        return self.db.query(Department).filter(Department.name == name).first()
    
    def get_all_departments(self, skip: int = 0, limit: int = 10) -> tuple[List[Department], int]:
        query = self.db.query(Department)
        total = query.count()
        departments = query.offset(skip).limit(limit).all()
        return departments, total
    
    def update_department(self, dept_id: int, dept_data: DepartmentUpdate) -> Optional[Department]:
        department = self.get_department_by_id(dept_id)
        if department:
            for key, value in dept_data.model_dump(exclude_unset=True).items():
                setattr(department, key, value)
            self.db.commit()
            self.db.refresh(department)
        return department
    
    def delete_department(self, dept_id: int) -> bool:
        department = self.get_department_by_id(dept_id)
        if department:
            self.db.delete(department)
            self.db.commit()
            return True
        return False