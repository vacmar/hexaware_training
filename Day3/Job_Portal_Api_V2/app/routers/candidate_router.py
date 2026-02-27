# app/routers/candidate_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.dependencies.rbac import role_required
from app.controllers.candidate_controller import CandidateController
from app.core.pagination import paginate_params


router = APIRouter(prefix="/candidate", tags=["Candidate"])


# -----------------------------
# View Jobs
# -----------------------------

@router.get("/jobs")
def get_jobs(
    pagination: dict = Depends(paginate_params),
    db: Session = Depends(get_db),
    user=Depends(role_required("candidate"))
):
    return CandidateController.get_jobs(
        db,
        pagination["page"],
        pagination["size"]
    )


# -----------------------------
# Apply Job
# -----------------------------

@router.post("/apply/{job_id}")
def apply_job(
    job_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required("candidate"))
):
    return CandidateController.apply_job(db, job_id, user)


# -----------------------------
# My Applications
# -----------------------------

@router.get("/applications")
def my_applications(
    pagination: dict = Depends(paginate_params),
    db: Session = Depends(get_db),
    user=Depends(role_required("candidate"))
):
    return CandidateController.my_applications(
        db,
        user,
        pagination["page"],
        pagination["size"]
    )