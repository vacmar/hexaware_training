"""
CORS configuration
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ..core.config import settings


def setup_cors(app: FastAPI) -> None:
    """Configure CORS middleware"""
    origins = settings.ALLOWED_ORIGINS.split(",") if settings.ALLOWED_ORIGINS != "*" else ["*"]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
