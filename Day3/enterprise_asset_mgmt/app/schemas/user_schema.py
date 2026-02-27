from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str

class UserCreate(UserBase):
    password: str
    department_id: Optional[int] = None

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[str] = None
    department_id: Optional[int] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    department_id: Optional[int] = None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
