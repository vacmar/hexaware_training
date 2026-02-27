from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database.base import Base
from datetime import datetime

class AssetRequest(Base):
    __tablename__ = "asset_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    asset_type = Column(String, nullable=False)
    reason = Column(String)
    status = Column(String, default="PENDING")
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    employee = relationship("User", back_populates="asset_requests", foreign_keys=[employee_id])
    approver = relationship("User", foreign_keys=[approved_by])
