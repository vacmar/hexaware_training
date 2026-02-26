from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"


class RepaymentBase(BaseModel):
    loan_application_id: int
    amount_paid: float = Field(..., gt=0)
    payment_status: PaymentStatus = PaymentStatus.PENDING


class RepaymentCreate(RepaymentBase):
    pass


class RepaymentResponse(RepaymentBase):
    id: int
    payment_date: datetime
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
