from sqlalchemy.orm import Session
from app.models.job import Job
from typing import Optional, List

class JobRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_job(self, job_data: dict) -> Job:
        new_job = Job(**job_data)
        self.db.add(new_job)
        self.db.commit()
        self.db.refresh(new_job)
        return new_job

    def get_job_by_id(self, job_id: int) -> Optional[Job]:
        return self.db.query(Job).filter(Job.id == job_id).first()

    def get_all_jobs(self, skip: int = 0, limit: int = 10) -> List[Job]:
        return self.db.query(Job).offset(skip).limit(limit).all()

    def update_job(self, job_id: int, job_data: dict) -> Optional[Job]:
        job = self.get_job_by_id(job_id)
        if job:
            for key, value in job_data.items():
                if value is not None:
                    setattr(job, key, value)
            self.db.commit()
            self.db.refresh(job)
        return job

    def delete_job(self, job_id: int) -> bool:
        job = self.get_job_by_id(job_id)
        if job:
            self.db.delete(job)
            self.db.commit()
            return True
        return False
