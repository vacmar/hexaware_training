# app/routers/employer_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.dependencies.rbac import role_required
from app.controllers.employer_controller import EmployerController
from app.schemas.job_schema import JobCreate, JobUpdate
from app.core.pagination import paginate_params


router = APIRouter(prefix="/employer", tags=["Employer"])


# -----------------------------
# Create Job
# -----------------------------

@router.post("/jobs")
def create_job(
    job: JobCreate,
    db: Session = Depends(get_db),
    user=Depends(role_required("employer"))
):
    return EmployerController.create_job(db, job.dict(), user)


# -----------------------------
# Update Job
# -----------------------------

@router.put("/jobs/{job_id}")
def update_job(
    job_id: int,
    job: JobUpdate,
    db: Session = Depends(get_db),
    user=Depends(role_required("employer"))
):
    return EmployerController.update_job(db, job_id, job.dict(exclude_unset=True), user)


# -----------------------------
# Delete Job
# -----------------------------

@router.delete("/jobs/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required("employer"))
):
    return EmployerController.delete_job(db, job_id, user)


# -----------------------------
# View Applications
# -----------------------------

@router.get("/applications")
def view_applications(
    pagination: dict = Depends(paginate_params),
    db: Session = Depends(get_db),
    user=Depends(role_required("employer"))
):
    return EmployerController.get_applications(
        db,
        user,
        pagination["page"],
        pagination["size"]
    )