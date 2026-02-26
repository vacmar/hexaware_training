# app/services/loan_service.py

from fastapi import HTTPException
from models.loan_model import LoanStatus
from repositories.loan_repository import LoanRepository

class LoanService:

    def __init__(self, repository: LoanRepository):
        self.repository = repository

    def create_loan(self, applicant_name, income, loan_amount):

        # Business Rule: eligibility check
        max_eligible = income * 10

        if loan_amount > max_eligible:
            raise HTTPException(
                status_code=400,
                detail="Loan amount exceeds eligibility limit"
            )

        return self.repository.create_loan(applicant_name, income, loan_amount)

    def get_loan(self, loan_id: int):
        loan = self.repository.get_loan_by_id(loan_id)
        if not loan:
            raise HTTPException(status_code=404, detail="Loan application not found")
        return loan

    def get_all_loans(self):
        return self.repository.get_all_loans()

    def approve_loan(self, loan_id: int):
        loan = self.get_loan(loan_id)

        if loan["status"] != LoanStatus.PENDING:
            raise HTTPException(
                status_code=400,
                detail="Only pending loans can be approved"
            )

        return self.repository.update_status(loan, LoanStatus.APPROVED)

    def reject_loan(self, loan_id: int):
        loan = self.get_loan(loan_id)

        if loan["status"] != LoanStatus.PENDING:
            raise HTTPException(
                status_code=400,
                detail="Only pending loans can be rejected"
            )

        return self.repository.update_status(loan, LoanStatus.REJECTED)