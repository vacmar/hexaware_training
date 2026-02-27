from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.job_repo import (
    create_job,
    get_job_by_id,
    get_all_jobs,
    get_jobs_by_employer,
    update_job,
    delete_job
)
from app.core.pagination import paginate_query


# -----------------------------
# Create Job (Employer)
# -----------------------------

def create_job_service(db: Session, data: dict, user):

    data["created_by"] = user.id

    return create_job(db, data)


# -----------------------------
# List All Jobs (Admin/Candidate)
# -----------------------------

def list_jobs_service(db: Session, page: int, size: int):
    query = get_all_jobs(db)
    return paginate_query(query, page, size)


# -----------------------------
# Update Job (Employer Only Own)
# -----------------------------

def update_job_service(db: Session, job_id: int, data: dict, user):

    job = get_job_by_id(db, job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if job.created_by != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return update_job(db, job, data)


# -----------------------------
# Delete Job
# -----------------------------

def delete_job_service(db: Session, job_id: int, user):

    job = get_job_by_id(db, job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if user.role != "admin" and job.created_by != user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    delete_job(db, job)

    return {"message": "Job deleted successfully"}