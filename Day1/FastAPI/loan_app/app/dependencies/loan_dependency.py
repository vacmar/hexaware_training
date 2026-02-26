# app/dependencies/loan_dependency.py

from repositories.loan_repository import LoanRepository
from services.loan_service import LoanService

repository = LoanRepository()

def get_loan_service():
    return LoanService(repository)