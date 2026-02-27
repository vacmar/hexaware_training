# department.py
from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.base import Base
from sqlalchemy.orm import relationship


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    manager = relationship("User", back_populates="managed_department", foreign_keys=[manager_id])

    # Employees in this department
    employees = relationship("User", back_populates="department", foreign_keys="User.department_id")
