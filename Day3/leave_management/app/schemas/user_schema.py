from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str  # ADMIN / MANAGER / EMPLOYEE


class UserCreate(UserBase):
    password: str
    department_id: Optional[int] = None


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    department_id: Optional[int] = None


class UserResponse(UserBase):
    id: int
    department_id: Optional[int] = None

    class Config:
        from_attributes = True


class UserWithDepartment(UserResponse):
    department_name: Optional[str] = None
