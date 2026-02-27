# app/routers/admin_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.dependencies.rbac import role_required
from app.controllers.admin_controller import AdminController
from app.schemas.company_schema import CompanyCreate, CompanyResponse
from app.core.pagination import paginate_params


router = APIRouter(prefix="/admin", tags=["Admin"])


# -----------------------------
# Company Management
# -----------------------------

@router.post("/companies", response_model=CompanyResponse)
def create_company(
    company: CompanyCreate,
    db: Session = Depends(get_db),
    user=Depends(role_required("admin"))
):
    return AdminController.create_company(db, company.dict())


@router.get("/companies")
def list_companies(
    db: Session = Depends(get_db),
    user=Depends(role_required("admin"))
):
    return AdminController.get_companies(db)


# -----------------------------
# Jobs
# -----------------------------

@router.get("/jobs")
def get_all_jobs(
    pagination: dict = Depends(paginate_params),
    db: Session = Depends(get_db),
    user=Depends(role_required("admin"))
):
    return AdminController.get_all_jobs(
        db,
        pagination["page"],
        pagination["size"]
    )


@router.delete("/jobs/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    user=Depends(role_required("admin"))
):
    return AdminController.delete_job(db, job_id, user)


# -----------------------------
# Applications
# -----------------------------

@router.get("/applications")
def get_all_applications(
    pagination: dict = Depends(paginate_params),
    db: Session = Depends(get_db),
    user=Depends(role_required("admin"))
):
    return AdminController.get_all_applications(
        db,
        pagination["page"],
        pagination["size"]
    )