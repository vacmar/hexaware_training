# Main application file for user service
from fastapi import FastAPI
from app.database.base import Base
from app.database.session import engine
from app.router.user_router import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Service")

app.include_router(router)