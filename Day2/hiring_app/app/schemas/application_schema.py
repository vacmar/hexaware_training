from pydantic import BaseModel
from typing import Optional
from app.models.application import ApplicationStatus
from app.schemas.user_schema import UserResponse
from app.schemas.job_schema import JobResponse

class ApplicationBase(BaseModel):
    user_id: int
    job_id: int

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationUpdate(BaseModel):
    status: ApplicationStatus

class ApplicationResponse(ApplicationBase):
    id: int
    status: ApplicationStatus

    class Config:
        from_attributes = True

class ApplicationDetailResponse(BaseModel):
    id: int
    status: ApplicationStatus
    user: UserResponse
    job: JobResponse

    class Config:
        from_attributes = True
