#user.py
from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.base import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String) #candidate / employer / admin

    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True) # Only for employers
    company = relationship("Company", back_populates="employees")
