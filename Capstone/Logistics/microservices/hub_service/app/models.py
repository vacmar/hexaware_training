"""
Hub model
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, Text, Integer, DateTime
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from shared.database import Base
from shared.types import GUID


class Hub(Base):
    """Hub/Distribution center model"""
    __tablename__ = "hubs"
    
    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    hub_name = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False, index=True)
    address = Column(Text, nullable=True)
    contact_phone = Column(String(20), nullable=True)
    contact_email = Column(String(255), nullable=True)
    capacity = Column(Integer, nullable=True)  # Maximum shipments it can handle
    is_active = Column(Boolean, default=True, nullable=False)
    
    def __repr__(self):
        return f"<Hub(id={self.id}, hub_name={self.hub_name}, city={self.city})>"
