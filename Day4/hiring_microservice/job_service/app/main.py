# Main application file for job service
from fastapi import FastAPI
from app.database.base import Base
from app.database.session import engine
from app.router.job_router import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Service")

app.include_router(router)
