from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from app.core.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum


class ApplicationStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    DISBURSED = "disbursed"
    CLOSED = "closed"


class LoanApplication(Base):
    __tablename__ = "loan_applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("loan_products.id"), nullable=False)
    requested_amount = Column(Float, nullable=False)
    approved_amount = Column(Float, nullable=True)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.PENDING, nullable=False)
    processed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    customer = relationship("User", back_populates="loan_applications", foreign_keys=[user_id])
    loan_officer = relationship("User", back_populates="processed_applications", foreign_keys=[processed_by])
    loan_product = relationship("LoanProduct", back_populates="loan_applications")
    repayments = relationship("Repayment", back_populates="loan_application")
