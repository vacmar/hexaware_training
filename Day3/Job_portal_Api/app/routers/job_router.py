from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.job import Job
from schemas.job_schema import JobCreate
from dependencies.role_checker import get_current_user, require_role as RoleChecker

router = APIRouter(prefix="/jobs", tags=["Jobs"])

#Anyone logged in can view jobs
@router.get("/")
def view_jobs(db: Session = Depends(get_db)):
    jobs = db.query(Job).all()
    return jobs

#Only employers can post jobs
@router.post("/", dependencies=[Depends(RoleChecker("employer"))])
def post_job(job: JobCreate, db: Session = Depends(get_db)):
    new_job = Job(
        title=job.title,
        description=job.description,
        company=job.company,
        location=job.location,
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return {"message": "Job posted successfully", "job_id": new_job.id}

#Only admin can delete jobs
@router.delete("/{job_id}", dependencies=[Depends(RoleChecker("admin"))])
def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    db.delete(job)
    db.commit()
    return {"message": "Job deleted successfully"}