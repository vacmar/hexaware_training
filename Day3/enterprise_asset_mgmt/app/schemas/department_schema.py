from pydantic import BaseModel, ConfigDict
from typing import Optional

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

    model_config = ConfigDict(from_attributes=True)
