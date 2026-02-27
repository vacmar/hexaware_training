from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from app.database.session import engine
from app.database.base import Base
from app.models import user, department, asset, asset_assignment, asset_request
from app.routers import auth_router, superadmin_router, itadmin_router, manager_router, employee_router
from app.middleware.logging import LoggingMiddleware
from app.middleware.exception_handler import validation_exception_handler, sqlalchemy_exception_handler, general_exception_handler

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Enterprise Asset Management API", version="1.0")

app.add_middleware(LoggingMiddleware)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

app.include_router(auth_router.router)
app.include_router(superadmin_router.router)
app.include_router(itadmin_router.router)
app.include_router(manager_router.router)
app.include_router(employee_router.router)

@app.get("/")
def root():
    return {"message": "Welcome to Enterprise Asset Management API"}
