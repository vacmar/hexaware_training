"""
Central router - includes all route modules
"""
from fastapi import APIRouter
from .routes import auth, shipments, tracking, hubs, admin

# Create main API router
api_router = APIRouter()

# Include all route modules
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(shipments.router, prefix="/shipments", tags=["Shipments"])
api_router.include_router(tracking.router, prefix="/tracking", tags=["Tracking"])
api_router.include_router(hubs.router, prefix="/hubs", tags=["Hubs"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
