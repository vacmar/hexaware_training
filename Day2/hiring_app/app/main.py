from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.core.database import engine, Base
from app.core.logger import logger

from app.middleware.cors import setup_cors
from app.middleware.logging import LoggingMiddleware
from app.exceptions.exception_handlers import GlobalExceptionMiddleware, register_exception_handlers

from app.controllers import (
    user_controller,
    job_controller,
    application_controller
)

# Create FastAPI application
app = FastAPI(
    title="Hiring Application API",
    description="Enterprise backend system for managing job postings, users, and applications",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Create database tables
logger.info("Creating database tables...")
Base.metadata.create_all(bind=engine)
logger.info("Database tables created successfully")

# Setup CORS middleware
setup_cors(app)

# Register middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(GlobalExceptionMiddleware)

# Register exception handlers
register_exception_handlers(app)

# Register routers
app.include_router(user_controller.router)
app.include_router(job_controller.router)
app.include_router(application_controller.router)

# Root endpoint
@app.get("/")
def read_root():
    """
    Root endpoint - Health check
    """
    return {
        "message": "Welcome to Hiring Application API",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs"
    }

# Health check endpoint
@app.get("/health")
def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "database": "connected"
    }

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Hiring Application API...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
