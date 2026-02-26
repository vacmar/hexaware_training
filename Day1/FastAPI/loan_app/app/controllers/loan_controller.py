# app/controllers/loan_controller.py

from fastapi import APIRouter, Depends, status
from schemas.loan_schema import (
    LoanCreate,
    LoanResponse,
    LoanStatusResponse
)
from dependencies.loan_dependency import get_loan_service
from services.loan_service import LoanService

router = APIRouter()


@router.post("/loans", response_model=LoanResponse, status_code=status.HTTP_201_CREATED)
def create_loan(
    loan_data: LoanCreate,
    service: LoanService = Depends(get_loan_service)
):
    return service.create_loan(
        loan_data.applicant_name,
        loan_data.income,
        loan_data.loan_amount
    )


@router.get("/loans/{loan_id}", response_model=LoanResponse)
def get_loan(
    loan_id: int,
    service: LoanService = Depends(get_loan_service)
):
    return service.get_loan(loan_id)


@router.get("/loans", response_model=list[LoanResponse])
def get_all_loans(
    service: LoanService = Depends(get_loan_service)
):
    return service.get_all_loans()


@router.put("/loans/{loan_id}/approve", response_model=LoanStatusResponse)
def approve_loan(
    loan_id: int,
    service: LoanService = Depends(get_loan_service)
):
    loan = service.approve_loan(loan_id)
    return {"message": "Loan approved successfully", "status": loan["status"]}


@router.put("/loans/{loan_id}/reject", response_model=LoanStatusResponse)
def reject_loan(
    loan_id: int,
    service: LoanService = Depends(get_loan_service)
):
    loan = service.reject_loan(loan_id)
    return {"message": "Loan rejected", "status": loan["status"]}