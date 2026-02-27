#application_schema.py

from pydantic import BaseModel
from typing import Optional

class ApplicationBase(BaseModel):
    job_id: int

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationUpdate(BaseModel):
    status: Optional[str] = None

class ApplicationResponse(ApplicationBase):
    id: int
    status: str
    job_id: int
    candidate_id: int

    class Config:
        from_attributes = True