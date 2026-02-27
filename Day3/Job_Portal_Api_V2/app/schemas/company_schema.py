#company_schema.py
from pydantic import BaseModel
from typing import Optional

class CompanyBase(BaseModel):
    name: str
    description: Optional[str] = None
   
class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(CompanyBase):
    name: Optional[str] = None
    description: Optional[str] = None

class CompanyResponse(CompanyBase):
    id: int

    class Config:
        from_attributes = True