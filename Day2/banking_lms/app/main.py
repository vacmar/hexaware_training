from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.core.database import engine, Base
from app.middleware.validation_handler import validation_exception_handler
from app.middleware.exception import GlobalExceptionMiddleware, LoggingMiddleware
from app.middleware.cors import setup_cors

from app.controllers import (
    user_controller,
    product_controller,
    application_controller,
    repayment_controller
)

app = FastAPI(
    title="Banking Loan Management System (LMS)",
    description="Enterprise Banking LMS with Loan Processing, Approvals, and Repayment Tracking",
    version="1.0.0"
)

# Create tables automatically
Base.metadata.create_all(bind=engine)

# Setup CORS
setup_cors(app)

# Register middleware
app.add_middleware(GlobalExceptionMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Register routers
app.include_router(user_controller.router)
app.include_router(product_controller.router)
app.include_router(application_controller.router)
app.include_router(repayment_controller.router)


@app.get("/", tags=["Health"])
def read_root():
    return {
        "message": "Banking Loan Management System API",
        "version": "1.0.0",
        "endpoints": {
            "users": "/users",
            "loan_products": "/loan-products",
            "loan_applications": "/loan-applications",
            "repayments": "/repayments"
        }
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}
