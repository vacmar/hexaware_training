#job_schema.py
from pydantic import BaseModel
from typing import Optional

class JobBase(BaseModel):
    title: str
    description: str
    salary: int
    
class JobCreate(JobBase):
    company_id: int

class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    salary: Optional[int] = None

class JobResponse(JobBase):
    id: int
    company_id: int
    created_by: int

    class Config:
        from_attributes = True