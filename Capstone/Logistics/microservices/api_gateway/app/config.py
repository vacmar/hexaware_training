"""
API Gateway Configuration
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    """Gateway settings loaded from environment variables"""
    
    # Application
    APP_NAME: str = "Logistics API Gateway"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Service URLs
    AUTH_SERVICE_URL: str = os.getenv("AUTH_SERVICE_URL", "http://auth-service:8001")
    HUB_SERVICE_URL: str = os.getenv("HUB_SERVICE_URL", "http://hub-service:8002")
    SHIPMENT_SERVICE_URL: str = os.getenv("SHIPMENT_SERVICE_URL", "http://shipment-service:8003")
    TRACKING_SERVICE_URL: str = os.getenv("TRACKING_SERVICE_URL", "http://tracking-service:8004")
    
    # JWT Settings (for token validation)
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    
    # Request timeout
    REQUEST_TIMEOUT: float = 30.0
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


settings = get_settings()
