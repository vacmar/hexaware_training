# Main application file for company service
from fastapi import FastAPI
from app.database.base import Base
from app.database.session import engine
from app.router.company_router import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Company Service")

app.include_router(router)
