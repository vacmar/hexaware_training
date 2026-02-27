# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.base import Base
from app.database.session import engine

# Routers
from app.routers.auth_router import router as auth_router
from app.routers.admin_router import router as admin_router
from app.routers.employer_router import router as employer_router
from app.routers.candidate_router import router as candidate_router

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
    title="Enterprise Hiring Platform API",
    description="Role Based Hiring Platform Backend (Admin, Employer, Candidate)",
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
app.include_router(employer_router)
app.include_router(candidate_router)


# -------------------------------------------------
# Health Check Endpoint
# -------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "Enterprise Hiring Platform API is running",
        "status": "success"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }