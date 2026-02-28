"""
User model - Admin, Agent, Customer
"""
import enum
from sqlalchemy import Column, String, Boolean, Enum
from .base import BaseModel


class UserRole(str, enum.Enum):
    """User role enumeration"""
    CUSTOMER = "customer"
    AGENT = "agent"
    ADMIN = "admin"


class User(BaseModel):
    """User model for authentication and authorization"""
    __tablename__ = "users"
    
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
