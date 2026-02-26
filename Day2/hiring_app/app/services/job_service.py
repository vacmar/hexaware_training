from sqlalchemy.orm import Session
from app.repositories.job_repository import JobRepository
from fastapi import HTTPException
from typing import List

class JobService:
    def __init__(self, db: Session):
        self.job_repository = JobRepository(db)
        self.db = db

    def create_job(self, job_data: dict):
        try:
            if job_data.get('salary', 0) <= 0:
                raise HTTPException(status_code=400, detail="Salary must be positive")
            return self.job_repository.create_job(job_data)
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Error creating job: {str(e)}")

    def get_job(self, job_id: int):
        job = self.job_repository.get_job_by_id(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return job

    def list_jobs(self, skip: int = 0, limit: int = 10) -> List:
        if limit > 100:
            raise HTTPException(status_code=400, detail="Limit cannot exceed 100")
        return self.job_repository.get_all_jobs(skip, limit)

    def update_job(self, job_id: int, job_data: dict):
        try:
            existing_job = self.job_repository.get_job_by_id(job_id)
            if not existing_job:
                raise HTTPException(status_code=404, detail="Job not found")
            
            if 'salary' in job_data and job_data['salary'] is not None:
                if job_data['salary'] <= 0:
                    raise HTTPException(status_code=400, detail="Salary must be positive")
            
            updated_job = self.job_repository.update_job(job_id, job_data)
            return updated_job
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Error updating job: {str(e)}")

    def delete_job(self, job_id: int):
        try:
            if not self.job_repository.delete_job(job_id):
                raise HTTPException(status_code=404, detail="Job not found")
            return {"message": "Job deleted successfully"}
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Error deleting job: {str(e)}")
