from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class ApplicationStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    DISBURSED = "disbursed"
    CLOSED = "closed"


class LoanApplicationBase(BaseModel):
    user_id: int
    product_id: int
    requested_amount: float = Field(..., gt=0)


class LoanApplicationCreate(LoanApplicationBase):
    pass


class LoanApplicationStatusUpdate(BaseModel):
    status: ApplicationStatus
    approved_amount: Optional[float] = None


class LoanApplicationResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    requested_amount: float
    approved_amount: Optional[float]
    status: ApplicationStatus
    processed_by: Optional[int]
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
