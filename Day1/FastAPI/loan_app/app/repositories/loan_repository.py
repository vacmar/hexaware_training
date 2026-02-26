# app/repositories/loan_repository.py

from typing import List, Optional
from models.loan_model import LoanStatus

class LoanRepository:

    def __init__(self):
        self.loans: List[dict] = []
        self.counter = 1

    def create_loan(self, applicant_name, income, loan_amount) -> dict:
        loan = {
            "id": self.counter,
            "applicant_name": applicant_name,
            "income": income,
            "loan_amount": loan_amount,
            "status": LoanStatus.PENDING
        }
        self.loans.append(loan)
        self.counter += 1
        return loan

    def get_loan_by_id(self, loan_id: int) -> Optional[dict]:
        return next((loan for loan in self.loans if loan["id"] == loan_id), None)

    def get_all_loans(self) -> List[dict]:
        return self.loans

    def update_status(self, loan: dict, status: LoanStatus):
        loan["status"] = status
        return loan