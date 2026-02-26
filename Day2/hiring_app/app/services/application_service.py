from sqlalchemy.orm import Session
from app.repositories.application_repository import ApplicationRepository
from app.repositories.user_repository import UserRepository
from app.repositories.job_repository import JobRepository
from fastapi import HTTPException
from app.models.application import ApplicationStatus
from typing import List

class ApplicationService:
    def __init__(self, db: Session):
        self.application_repository = ApplicationRepository(db)
        self.user_repository = UserRepository(db)
        self.job_repository = JobRepository(db)
        self.db = db

    def create_application(self, application_data: dict):
        try:
            user_id = application_data.get('user_id')
            job_id = application_data.get('job_id')
            
            user = self.user_repository.get_user_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            job = self.job_repository.get_job_by_id(job_id)
            if not job:
                raise HTTPException(status_code=404, detail="Job not found")
            
            existing_application = self.application_repository.check_existing_application(user_id, job_id)
            if existing_application:
                raise HTTPException(status_code=400, detail="User has already applied for this job")
            
            return self.application_repository.create_application(application_data)
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Error creating application: {str(e)}")

    def get_application(self, application_id: int):
        application = self.application_repository.get_application_by_id(application_id)
        if not application:
            raise HTTPException(status_code=404, detail="Application not found")
        return application

    def list_applications(self, skip: int = 0, limit: int = 10) -> List:
        return self.application_repository.get_all_applications(skip, limit)

    def get_user_applications(self, user_id: int) -> List:
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return self.application_repository.get_applications_by_user(user_id)

    def get_job_applications(self, job_id: int) -> List:
        job = self.job_repository.get_job_by_id(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return self.application_repository.get_applications_by_job(job_id)

    def update_application_status(self, application_id: int, status: ApplicationStatus):
        try:
            application = self.application_repository.get_application_by_id(application_id)
            if not application:
                raise HTTPException(status_code=404, detail="Application not found")
            
            if application.status == ApplicationStatus.REJECTED and status == ApplicationStatus.APPLIED:
                raise HTTPException(status_code=400, detail="Cannot revert rejected application to applied")
            
            updated_application = self.application_repository.update_application_status(application_id, status)
            return updated_application
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Error updating application: {str(e)}")

    def delete_application(self, application_id: int):
        try:
            if not self.application_repository.delete_application(application_id):
                raise HTTPException(status_code=404, detail="Application not found")
            return {"message": "Application deleted successfully"}
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Error deleting application: {str(e)}")
