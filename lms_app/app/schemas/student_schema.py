from pydantic import BaseModel, EmailStr

class StudentCreate(BaseModel):
    name: str
    email: EmailStr

class StudentResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True