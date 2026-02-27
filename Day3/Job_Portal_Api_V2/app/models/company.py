#company.py
from sqlalchemy import Column, Integer, String
from app.database.base import Base
from sqlalchemy.orm import relationship

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    employees = relationship("User", back_populates="company")

    jobs = relationship("Job", back_populates="company")