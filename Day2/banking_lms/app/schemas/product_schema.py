from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime


class LoanProductBase(BaseModel):
    product_name: str = Field(..., min_length=2, max_length=100)
    interest_rate: float = Field(..., gt=0, le=50)
    max_amount: float = Field(..., gt=0)
    tenure_months: int = Field(..., gt=0, le=360)
    description: Optional[str] = None


class LoanProductCreate(LoanProductBase):
    pass


class LoanProductUpdate(BaseModel):
    product_name: Optional[str] = None
    interest_rate: Optional[float] = None
    max_amount: Optional[float] = None
    tenure_months: Optional[int] = None
    description: Optional[str] = None


class LoanProductResponse(LoanProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
