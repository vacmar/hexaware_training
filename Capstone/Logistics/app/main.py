"""
Main application entry point
"""
import os
from fastapi import FastAPI
from .core.config import settings
from .core.database import engine, Base
from .api.router import api_router
from .middleware.cors import setup_cors
from .middleware.logging_middleware import LoggingMiddleware
from .exceptions.exception_handlers import setup_exception_handlers

# Create database tables only if not in test mode
# In production, use Alembic migrations instead
if os.getenv("TESTING") != "true":
    try:
        Base.metadata.create_all(bind=engine)
    except Exception:
        pass  # Database might not be available during import

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    Logistics & Shipment Tracking API
    
    This API provides endpoints for:
    - Customer shipment creation and tracking
    - Delivery agent status updates
    - Admin hub management and reporting
    
    ## Authentication
    
    Use the `/auth/register` endpoint to create an account.
    Use the `/auth/login` endpoint to get a JWT token.
    Include the token in the Authorization header: `Bearer <token>`
    
    ## Roles
    
    - **Customer**: Create and track shipments
    - **Agent**: Update shipment status
    - **Admin**: Manage hubs, users, and view reports
    """,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Setup middleware
setup_cors(app)
app.add_middleware(LoggingMiddleware)

# Setup exception handlers
setup_exception_handlers(app)

# Include API routes
app.include_router(api_router)


@app.get("/", tags=["Root"])
def root():
    """Root endpoint - health check"""
    return {
        "message": "Welcome to Logistics & Shipment Tracking API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
