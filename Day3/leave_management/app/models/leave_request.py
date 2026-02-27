# leave_request.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from app.database.base import Base
from sqlalchemy.orm import relationship


class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    reason = Column(String, nullable=False)
    status = Column(String, default="PENDING")  # PENDING / APPROVED / REJECTED
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Relationships
    employee = relationship("User", back_populates="leave_requests", foreign_keys=[employee_id])
    approver = relationship("User", foreign_keys=[approved_by])
