from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.database.base import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    department = relationship("Department", back_populates="users", foreign_keys=[department_id])
    asset_assignments = relationship("AssetAssignment", back_populates="user")
    asset_requests = relationship("AssetRequest", back_populates="employee")
    managed_department = relationship("Department", back_populates="manager", foreign_keys="Department.manager_id")
