from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: str


class UserCreate(UserBase):
    password: str
    company_id: Optional[int] = None


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    id: int
    company_id: Optional[int] = None

    class Config:
        from_attributes = True