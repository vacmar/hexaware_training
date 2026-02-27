from sqlalchemy.orm import Session
from app.services.job_service import (
    list_jobs_service
)
from app.services.application_service import (
    apply_job_service,
    get_candidate_applications_service
)


class CandidateController:

    # -----------------------------
    # View Jobs
    # -----------------------------

    @staticmethod
    def get_jobs(db: Session, page: int, size: int):
        return list_jobs_service(db, page, size)

    # -----------------------------
    # Apply Job
    # -----------------------------

    @staticmethod
    def apply_job(db: Session, job_id: int, user):
        return apply_job_service(db, job_id, user)

    # -----------------------------
    # My Applications
    # -----------------------------

    @staticmethod
    def my_applications(db: Session, user, page: int, size: int):
        return get_candidate_applications_service(db, user, page, size)