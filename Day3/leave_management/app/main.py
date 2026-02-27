# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.base import Base
from app.database.session import engine

# Routers
from app.routers.auth_router import router as auth_router
from app.routers.admin_router import router as admin_router
from app.routers.manager_router import router as manager_router
from app.routers.employee_router import router as employee_router

# Middleware
from app.middleware.logging import logging_middleware
from app.middleware.exception_handler import (
    http_exception_handler,
    validation_exception_handler,
    global_exception_handler,
)

from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError


# -------------------------------------------------
# Create FastAPI App
# -------------------------------------------------

app = FastAPI(
    title="Enterprise Leave Management System (ELMS)",
    description="Role-Based Leave Management Backend (Admin, Manager, Employee)",
    version="1.0.0"
)


# -------------------------------------------------
# Create Database Tables
# -------------------------------------------------

Base.metadata.create_all(bind=engine)


# -------------------------------------------------
# Register Middleware
# -------------------------------------------------

# Logging Middleware
app.middleware("http")(logging_middleware)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------------------------
# Register Exception Handlers
# -------------------------------------------------

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)


# -------------------------------------------------
# Include Routers
# -------------------------------------------------

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(manager_router)
app.include_router(employee_router)


# -------------------------------------------------
# Root Endpoint
# -------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "Welcome to Enterprise Leave Management System (ELMS)",
        "docs": "/docs",
        "version": "1.0.0"
    }


# -------------------------------------------------
# Health Check
# -------------------------------------------------

@app.get("/health")
def health_check():
    return {"status": "healthy"}
