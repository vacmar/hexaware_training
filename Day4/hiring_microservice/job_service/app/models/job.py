from sqlalchemy import Column, Integer, String
from app.database.base import Base

class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    location = Column(String)
    company_id = Column(Integer)  # Links to company_service
    employer_id = Column(Integer)  # Links to user_service
