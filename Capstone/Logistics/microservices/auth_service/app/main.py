"""
Auth Service - Main Application Entry Point
"""
import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add shared module to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from shared.config import settings
from shared.database import engine, Base
from .routes import auth_router, user_router
from .models import User

# Create database tables
try:
    Base.metadata.create_all(bind=engine)
except Exception:
    pass

# Create FastAPI application
app = FastAPI(
    title="Auth Service",
    version="1.0.0",
    description="Authentication and User Management Microservice",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(user_router, prefix="/users", tags=["Users"])


@app.get("/", tags=["Health"])
def root():
    """Root endpoint - service info"""
    return {
        "service": "Auth Service",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "auth-service"}
