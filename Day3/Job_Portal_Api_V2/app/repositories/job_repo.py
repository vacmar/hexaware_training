from sqlalchemy.orm import Session
from app.models.job import Job


# -----------------------------
# Create Job
# -----------------------------

def create_job(db: Session, job_data: dict) -> Job:
    job = Job(**job_data)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


# -----------------------------
# Get Job by ID
# -----------------------------

def get_job_by_id(db: Session, job_id: int) -> Job | None:
    return db.query(Job).filter(Job.id == job_id).first()


# -----------------------------
# Get All Jobs
# -----------------------------

def get_all_jobs(db: Session):
    return db.query(Job)


# -----------------------------
# Get Jobs by Employer
# -----------------------------

def get_jobs_by_employer(db: Session, employer_id: int):
    return db.query(Job).filter(Job.created_by == employer_id)


# -----------------------------
# Update Job
# -----------------------------

def update_job(db: Session, job: Job, update_data: dict) -> Job:
    for key, value in update_data.items():
        setattr(job, key, value)

    db.commit()
    db.refresh(job)
    return job


# -----------------------------
# Delete Job
# -----------------------------

def delete_job(db: Session, job: Job):
    db.delete(job)
    db.commit()