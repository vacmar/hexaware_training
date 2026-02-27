from sqlalchemy.orm import Session
from app.services.job_service import (
    create_job_service,
    update_job_service,
    delete_job_service,
)
from app.services.application_service import (
    get_employer_applications_service
)


class EmployerController:

    # -----------------------------
    # Job Management
    # -----------------------------

    @staticmethod
    def create_job(db: Session, data: dict, user):
        return create_job_service(db, data, user)

    @staticmethod
    def update_job(db: Session, job_id: int, data: dict, user):
        return update_job_service(db, job_id, data, user)

    @staticmethod
    def delete_job(db: Session, job_id: int, user):
        return delete_job_service(db, job_id, user)

    # -----------------------------
    # Applications
    # -----------------------------

    @staticmethod
    def get_applications(db: Session, user, page: int, size: int):
        return get_employer_applications_service(db, user, page, size)