from sqlalchemy.orm import Session
from app.models.application import Application


# -----------------------------
# Create Application
# -----------------------------

def create_application(db: Session, application_data: dict) -> Application:
    application = Application(**application_data)
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


# -----------------------------
# Get Application by ID
# -----------------------------

def get_application_by_id(db: Session, application_id: int) -> Application | None:
    return db.query(Application).filter(Application.id == application_id).first()


# -----------------------------
# Get Applications by Job
# -----------------------------

def get_applications_by_job(db: Session, job_id: int):
    return db.query(Application).filter(Application.job_id == job_id)


# -----------------------------
# Get Applications by Candidate
# -----------------------------

def get_applications_by_candidate(db: Session, candidate_id: int):
    return db.query(Application).filter(Application.candidate_id == candidate_id)


# -----------------------------
# Get All Applications
# -----------------------------

def get_all_applications(db: Session):
    return db.query(Application)


# -----------------------------
# Update Application
# -----------------------------

def update_application(db: Session, application: Application, update_data: dict):
    for key, value in update_data.items():
        setattr(application, key, value)

    db.commit()
    db.refresh(application)
    return application


# -----------------------------
# Delete Application
# -----------------------------

def delete_application(db: Session, application: Application):
    db.delete(application)
    db.commit()