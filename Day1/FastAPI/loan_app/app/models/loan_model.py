# app/models/loan_model.py

from enum import Enum
from dataclasses import dataclass

class LoanStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

@dataclass
class LoanApplication:
    id: int
    applicant_name: str
    income: float
    loan_amount: float
    status: LoanStatus