"""
API Gateway Routes - Proxy requests to microservices
"""
from fastapi import APIRouter, Request, HTTPException, Header
from fastapi.responses import JSONResponse
import httpx
from typing import Optional
from .config import settings

gateway_router = APIRouter()


async def proxy_request(
    request: Request,
    service_url: str,
    path: str,
    authorization: Optional[str] = None
):
    """Proxy a request to a microservice"""
    # Build the target URL
    url = f"{service_url}{path}"
    
    # Get headers
    headers = dict(request.headers)
    headers.pop("host", None)
    
    if authorization:
        headers["Authorization"] = authorization
    
    # Get request body
    body = None
    if request.method in ["POST", "PUT", "PATCH"]:
        body = await request.body()
    
    # Get query parameters
    params = dict(request.query_params)
    
    async with httpx.AsyncClient(timeout=settings.REQUEST_TIMEOUT) as client:
        try:
            response = await client.request(
                method=request.method,
                url=url,
                headers=headers,
                content=body,
                params=params
            )
            
            # Return the response from the microservice
            return JSONResponse(
                content=response.json() if response.content else None,
                status_code=response.status_code,
                headers={"X-Proxied-By": "api-gateway"}
            )
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="Service timeout")
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")


# ==================== Auth Service Routes ====================

@gateway_router.api_route("/auth/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def auth_proxy(request: Request, path: str, authorization: str = Header(None)):
    """Proxy requests to Auth Service"""
    return await proxy_request(request, settings.AUTH_SERVICE_URL, f"/auth/{path}", authorization)


@gateway_router.api_route("/users/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def users_proxy(request: Request, path: str, authorization: str = Header(None)):
    """Proxy requests to Auth Service (users endpoint)"""
    return await proxy_request(request, settings.AUTH_SERVICE_URL, f"/users/{path}", authorization)


@gateway_router.get("/users", tags=["Users"])
async def get_users(request: Request, authorization: str = Header(None)):
    """Proxy GET /users to Auth Service"""
    return await proxy_request(request, settings.AUTH_SERVICE_URL, "/users/", authorization)


# ==================== Hub Service Routes ====================

@gateway_router.api_route("/hubs/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def hubs_proxy(request: Request, path: str, authorization: str = Header(None)):
    """Proxy requests to Hub Service"""
    return await proxy_request(request, settings.HUB_SERVICE_URL, f"/hubs/{path}", authorization)


@gateway_router.get("/hubs", tags=["Hubs"])
async def get_hubs(request: Request, authorization: str = Header(None)):
    """Proxy GET /hubs to Hub Service"""
    return await proxy_request(request, settings.HUB_SERVICE_URL, "/hubs/", authorization)


@gateway_router.post("/hubs", tags=["Hubs"])
async def create_hub(request: Request, authorization: str = Header(None)):
    """Proxy POST /hubs to Hub Service"""
    return await proxy_request(request, settings.HUB_SERVICE_URL, "/hubs/", authorization)


# ==================== Shipment Service Routes ====================

@gateway_router.api_route("/shipments/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def shipments_proxy(request: Request, path: str, authorization: str = Header(None)):
    """Proxy requests to Shipment Service"""
    return await proxy_request(request, settings.SHIPMENT_SERVICE_URL, f"/shipments/{path}", authorization)


@gateway_router.get("/shipments", tags=["Shipments"])
async def get_shipments(request: Request, authorization: str = Header(None)):
    """Proxy GET /shipments to Shipment Service"""
    return await proxy_request(request, settings.SHIPMENT_SERVICE_URL, "/shipments/", authorization)


@gateway_router.post("/shipments", tags=["Shipments"])
async def create_shipment(request: Request, authorization: str = Header(None)):
    """Proxy POST /shipments to Shipment Service"""
    return await proxy_request(request, settings.SHIPMENT_SERVICE_URL, "/shipments/", authorization)


# ==================== Tracking Service Routes ====================

@gateway_router.api_route("/tracking/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def tracking_proxy(request: Request, path: str, authorization: str = Header(None)):
    """Proxy requests to Tracking Service"""
    return await proxy_request(request, settings.TRACKING_SERVICE_URL, f"/tracking/{path}", authorization)


@gateway_router.get("/tracking", tags=["Tracking"])
async def get_tracking(request: Request, authorization: str = Header(None)):
    """Proxy GET /tracking to Tracking Service"""
    return await proxy_request(request, settings.TRACKING_SERVICE_URL, "/tracking/", authorization)


# ==================== Public Track Endpoint ====================

@gateway_router.get("/track/{tracking_number}", tags=["Public"])
async def public_track(request: Request, tracking_number: str):
    """Public endpoint to track a shipment by tracking number"""
    return await proxy_request(
        request,
        settings.SHIPMENT_SERVICE_URL,
        f"/shipments/track/{tracking_number}"
    )
