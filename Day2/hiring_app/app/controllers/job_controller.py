from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.services.job_service import JobService
from app.schemas.job_schema import JobCreate, JobResponse, JobUpdate

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.post("/", response_model=JobResponse, status_code=201)
def create_job(job_data: JobCreate, db: Session = Depends(get_db)):
    """
    Create a new job posting.
    
    - **title**: Job title
    - **description**: Job description
    - **salary**: Salary offered (must be positive)
    - **company_id**: ID of the company posting the job
    """
    service = JobService(db)
    return service.create_job(job_data.dict())

@router.get("/", response_model=List[JobResponse])
def list_jobs(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
):
    """
    Get a list of all jobs with pagination.
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum records to return (default: 10, max: 100)
    """
    service = JobService(db)
    return service.list_jobs(skip, limit)

@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    """
    Get a specific job by ID.
    
    - **job_id**: The ID of the job to retrieve
    """
    service = JobService(db)
    return service.get_job(job_id)

@router.put("/{job_id}", response_model=JobResponse)
def update_job(job_id: int, job_data: JobUpdate, db: Session = Depends(get_db)):
    """
    Update a job posting.
    
    - **job_id**: The ID of the job to update
    - All fields are optional
    """
    service = JobService(db)
    return service.update_job(job_id, job_data.dict(exclude_unset=True))

@router.delete("/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    """
    Delete a job posting.
    
    - **job_id**: The ID of the job to delete
    """
    service = JobService(db)
    return service.delete_job(job_id)
