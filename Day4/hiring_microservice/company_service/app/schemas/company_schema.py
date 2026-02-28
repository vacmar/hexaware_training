from pydantic import BaseModel
from typing import Optional

class CompanyBase(BaseModel):
    name: str
    location: str

class CompanyCreate(CompanyBase):
    employer_id: int

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None

class CompanyResponse(CompanyBase):
    id: int
    employer_id: int

    class Config:
        from_attributes = True
