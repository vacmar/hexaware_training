"""
Hub Service - Main Application Entry Point
"""
import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add shared module to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from shared.database import engine, Base
from .routes import hub_router
from .models import Hub

# Create database tables
try:
    Base.metadata.create_all(bind=engine)
except Exception:
    pass

# Create FastAPI application
app = FastAPI(
    title="Hub Service",
    version="1.0.0",
    description="Hub/Distribution Center Management Microservice",
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
app.include_router(hub_router, prefix="/hubs", tags=["Hubs"])


@app.get("/", tags=["Health"])
def root():
    """Root endpoint - service info"""
    return {
        "service": "Hub Service",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "hub-service"}
