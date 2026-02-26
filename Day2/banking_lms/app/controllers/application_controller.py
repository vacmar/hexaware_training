from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.services.application_service import ApplicationService
from app.schemas.application_schema import (
    LoanApplicationCreate,
    LoanApplicationResponse,
    LoanApplicationStatusUpdate
)

router = APIRouter(prefix="/loan-applications", tags=["Loan Applications"])


@router.post("/", response_model=LoanApplicationResponse, status_code=201)
def create_application(app_data: LoanApplicationCreate, db: Session = Depends(get_db)):
    service = ApplicationService(db)
    return service.create_application(app_data.model_dump())


@router.get("/", response_model=List[LoanApplicationResponse])
def list_applications(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    service = ApplicationService(db)
    return service.list_applications(skip, limit)


@router.get("/{application_id}", response_model=LoanApplicationResponse)
def get_application(application_id: int, db: Session = Depends(get_db)):
    service = ApplicationService(db)
    return service.get_application(application_id)


@router.put("/{application_id}/status", response_model=LoanApplicationResponse)
def update_application_status(
    application_id: int,
    status_data: LoanApplicationStatusUpdate,
    processed_by: int = None,
    db: Session = Depends(get_db)
):
    service = ApplicationService(db)
    return service.update_status(
        application_id,
        status_data.status,
        status_data.approved_amount,
        processed_by
    )


@router.get("/user/{user_id}", response_model=List[LoanApplicationResponse])
def get_user_applications(user_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    service = ApplicationService(db)
    return service.get_customer_applications(user_id, skip, limit)
