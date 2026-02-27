from pydantic import BaseModel
from typing import Optional, List


class DepartmentBase(BaseModel):
    name: str


class DepartmentCreate(DepartmentBase):
    manager_id: Optional[int] = None


class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    manager_id: Optional[int] = None


class DepartmentResponse(DepartmentBase):
    id: int
    manager_id: Optional[int] = None

    class Config:
        from_attributes = True


class DepartmentWithManager(DepartmentResponse):
    manager_name: Optional[str] = None
    employee_count: int = 0
