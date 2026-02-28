"""
API Gateway - Main Entry Point for Logistics Microservices
"""
import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
from .config import settings
from .routes import gateway_router

# Create FastAPI application
app = FastAPI(
    title="Logistics API Gateway",
    version="1.0.0",
    description="""
    API Gateway for Logistics & Shipment Tracking Microservices
    
    This gateway routes requests to the appropriate microservices:
    - **Auth Service**: User authentication and management
    - **Hub Service**: Distribution hub management
    - **Shipment Service**: Shipment creation and management
    - **Tracking Service**: Shipment tracking updates
    
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

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include gateway routes
app.include_router(gateway_router)


@app.get("/", tags=["Root"])
def root():
    """Root endpoint - API Gateway info"""
    return {
        "message": "Welcome to Logistics API Gateway",
        "version": "1.0.0",
        "docs": "/docs",
        "services": {
            "auth": settings.AUTH_SERVICE_URL,
            "hub": settings.HUB_SERVICE_URL,
            "shipment": settings.SHIPMENT_SERVICE_URL,
            "tracking": settings.TRACKING_SERVICE_URL
        }
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint - checks all services"""
    services_status = {}
    
    async with httpx.AsyncClient(timeout=5.0) as client:
        for service_name, service_url in [
            ("auth", settings.AUTH_SERVICE_URL),
            ("hub", settings.HUB_SERVICE_URL),
            ("shipment", settings.SHIPMENT_SERVICE_URL),
            ("tracking", settings.TRACKING_SERVICE_URL)
        ]:
            try:
                response = await client.get(f"{service_url}/health")
                services_status[service_name] = "healthy" if response.status_code == 200 else "unhealthy"
            except httpx.RequestError:
                services_status[service_name] = "unavailable"
    
    all_healthy = all(s == "healthy" for s in services_status.values())
    
    return {
        "status": "healthy" if all_healthy else "degraded",
        "services": services_status
    }
