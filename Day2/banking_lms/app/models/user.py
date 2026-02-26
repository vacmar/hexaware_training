from sqlalchemy import Column, Integer, String, DateTime, Enum
from app.core.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    LOAN_OFFICER = "loan_officer"
    CUSTOMER = "customer"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    loan_applications = relationship("LoanApplication", back_populates="customer", foreign_keys="LoanApplication.user_id")
    processed_applications = relationship("LoanApplication", back_populates="loan_officer", foreign_keys="LoanApplication.processed_by")
