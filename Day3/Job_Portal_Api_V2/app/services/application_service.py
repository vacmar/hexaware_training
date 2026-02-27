from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.application_repo import (
    create_application,
    get_application_by_id,
    get_applications_by_job,
    get_applications_by_candidate,
    get_all_applications,
    update_application
)
from app.repositories.job_repo import get_job_by_id
from app.core.pagination import paginate_query


# -----------------------------
# Apply for Job (Candidate)
# -----------------------------

def apply_job_service(db: Session, job_id: int, user):

    job = get_job_by_id(db, job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    application_data = {
        "job_id": job_id,
        "candidate_id": user.id,
        "status": "applied"
    }

    return create_application(db, application_data)


# -----------------------------
# Get Candidate Applications
# -----------------------------

def get_candidate_applications_service(db: Session, user, page: int, size: int):
    query = get_applications_by_candidate(db, user.id)
    return paginate_query(query, page, size)


# -----------------------------
# Get Employer Applications
# -----------------------------

def get_employer_applications_service(db: Session, user, page: int, size: int):
    # Applications for jobs created by employer
    from app.models.job import Job
    from app.models.application import Application

    query = (
        db.query(Application)
        .join(Job)
        .filter(Job.created_by == user.id)
    )

    return paginate_query(query, page, size)


# -----------------------------
# Admin View All Applications
# -----------------------------

def list_all_applications_service(db: Session, page: int, size: int):
    query = get_all_applications(db)
    return paginate_query(query, page, size)


# -----------------------------
# Update Application Status
# -----------------------------

def update_application_status_service(db: Session, app_id: int, data: dict):

    application = get_application_by_id(db, app_id)

    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    return update_application(db, application, data)