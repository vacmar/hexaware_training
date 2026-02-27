from sqlalchemy.orm import Session
from app.services.company_service import (
    create_company_service,
    list_companies,
    delete_company_service
)
from app.services.job_service import (
    list_jobs_service,
    delete_job_service
)
from app.services.application_service import (
    list_all_applications_service
)


class AdminController:

    # -----------------------------
    # Company Management
    # -----------------------------

    @staticmethod
    def create_company(db: Session, data: dict):
        return create_company_service(db, data)

    @staticmethod
    def get_companies(db: Session):
        return list_companies(db)

    @staticmethod
    def delete_company(db: Session, company_id: int):
        return delete_company_service(db, company_id)

    # -----------------------------
    # Job Management
    # -----------------------------

    @staticmethod
    def get_all_jobs(db: Session, page: int, size: int):
        return list_jobs_service(db, page, size)

    @staticmethod
    def delete_job(db: Session, job_id: int, user):
        return delete_job_service(db, job_id, user)

    # -----------------------------
    # Applications
    # -----------------------------

    @staticmethod
    def get_all_applications(db: Session, page: int, size: int):
        return list_all_applications_service(db, page, size)