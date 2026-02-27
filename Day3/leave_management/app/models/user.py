# user.py
from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.base import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # ADMIN / MANAGER / EMPLOYEE

    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    department = relationship("Department", back_populates="employees", foreign_keys=[department_id])

    # Leave requests created by this user
    leave_requests = relationship("LeaveRequest", back_populates="employee", foreign_keys="LeaveRequest.employee_id")

    # Department managed by this user (if manager)
    managed_department = relationship("Department", back_populates="manager", foreign_keys="Department.manager_id", uselist=False)
