from pydantic import BaseModel
from typing import Optional

class JobBase(BaseModel):
    title: str
    description: str
    location: str

class JobCreate(JobBase):
    company_id: int
    employer_id: int

class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None

class JobResponse(JobBase):
    id: int
    company_id: int
    employer_id: int

    class Config:
        from_attributes = True
