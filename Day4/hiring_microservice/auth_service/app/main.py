from fastapi import FastAPI
from app.database.base import Base
from app.database.session import engine
from app.router.auth_router import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth Service")

app.include_router(router)