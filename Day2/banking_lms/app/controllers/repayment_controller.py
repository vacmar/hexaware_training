from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.services.repayment_service import RepaymentService
from app.schemas.repayment_schema import RepaymentCreate, RepaymentResponse

router = APIRouter(prefix="/repayments", tags=["Repayments"])


@router.post("/", response_model=RepaymentResponse, status_code=201)
def create_repayment(repayment_data: RepaymentCreate, db: Session = Depends(get_db)):
    service = RepaymentService(db)
    return service.create_repayment(repayment_data.model_dump())


@router.get("/{repayment_id}", response_model=RepaymentResponse)
def get_repayment(repayment_id: int, db: Session = Depends(get_db)):
    service = RepaymentService(db)
    return service.get_repayment(repayment_id)


@router.get("/application/{application_id}", response_model=List[RepaymentResponse])
def get_application_repayments(
    application_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    service = RepaymentService(db)
    return service.get_application_repayments(application_id, skip, limit)


@router.get("/application/{application_id}/balance")
def get_outstanding_balance(application_id: int, db: Session = Depends(get_db)):
    service = RepaymentService(db)
    balance = service.get_outstanding_balance(application_id)
    return {"application_id": application_id, "outstanding_balance": balance}
