# app/schemas/loan_schema.py

from pydantic import BaseModel, Field
from models.loan_model import LoanStatus

class LoanCreate(BaseModel):
    applicant_name: str
    income: float = Field(gt=0)
    loan_amount: float = Field(gt=0)

class LoanResponse(BaseModel):
    id: int
    applicant_name: str
    income: float
    loan_amount: float
    status: LoanStatus

class LoanStatusResponse(BaseModel):
    message: str
    status: LoanStatus