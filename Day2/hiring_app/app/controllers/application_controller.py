from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.services.application_service import ApplicationService
from app.schemas.application_schema import (
    ApplicationCreate, 
    ApplicationResponse, 
    ApplicationUpdate,
    ApplicationDetailResponse
)

router = APIRouter(prefix="/applications", tags=["Applications"])

@router.post("/", response_model=ApplicationResponse, status_code=201)
def create_application(application_data: ApplicationCreate, db: Session = Depends(get_db)):
    """
    Apply for a job.
    
    - **user_id**: ID of the user applying
    - **job_id**: ID of the job being applied to
    """
    service = ApplicationService(db)
    return service.create_application(application_data.dict())

@router.get("/", response_model=List[ApplicationDetailResponse])
def list_applications(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
):
    """
    Get a list of all applications with pagination.
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum records to return (default: 10, max: 100)
    """
    service = ApplicationService(db)
    return service.list_applications(skip, limit)

@router.get("/{application_id}", response_model=ApplicationDetailResponse)
def get_application(application_id: int, db: Session = Depends(get_db)):
    """
    Get a specific application by ID.
    
    - **application_id**: The ID of the application to retrieve
    """
    service = ApplicationService(db)
    return service.get_application(application_id)

@router.get("/user/{user_id}", response_model=List[ApplicationDetailResponse])
def get_user_applications(user_id: int, db: Session = Depends(get_db)):
    """
    Get all applications submitted by a specific user (nested query).
    
    - **user_id**: The ID of the user
    """
    service = ApplicationService(db)
    return service.get_user_applications(user_id)

@router.get("/job/{job_id}", response_model=List[ApplicationDetailResponse])
def get_job_applications(job_id: int, db: Session = Depends(get_db)):
    """
    Get all applications for a specific job (nested query).
    
    - **job_id**: The ID of the job
    """
    service = ApplicationService(db)
    return service.get_job_applications(job_id)

@router.patch("/{application_id}/status", response_model=ApplicationResponse)
def update_application_status(
    application_id: int, 
    status_data: ApplicationUpdate, 
    db: Session = Depends(get_db)
):
    """
    Update the status of an application.
    
    - **application_id**: The ID of the application
    - **status**: New status (applied, shortlisted, rejected)
    """
    service = ApplicationService(db)
    return service.update_application_status(application_id, status_data.status)

@router.delete("/{application_id}")
def delete_application(application_id: int, db: Session = Depends(get_db)):
    """
    Delete an application.
    
    - **application_id**: The ID of the application to delete
    """
    service = ApplicationService(db)
    return service.delete_application(application_id)
