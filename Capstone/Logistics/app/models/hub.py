"""
Hub model
"""
from sqlalchemy import Column, String, Boolean, Text, Integer
from .base import BaseModel


class Hub(BaseModel):
    """Hub/Distribution center model"""
    __tablename__ = "hubs"
    
    hub_name = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False, index=True)
    address = Column(Text, nullable=True)
    contact_phone = Column(String(20), nullable=True)
    contact_email = Column(String(255), nullable=True)
    capacity = Column(Integer, nullable=True)  # Maximum shipments it can handle
    is_active = Column(Boolean, default=True, nullable=False)
    
    def __repr__(self):
        return f"<Hub(id={self.id}, hub_name={self.hub_name}, city={self.city})>"
