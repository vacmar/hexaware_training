"""
Exception handlers for the application
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .custom_exceptions import LogisticsBaseException


def setup_exception_handlers(app: FastAPI) -> None:
    """Register exception handlers with the FastAPI app"""
    
    @app.exception_handler(LogisticsBaseException)
    async def logistics_exception_handler(request: Request, exc: LogisticsBaseException):
        """Handle custom logistics exceptions"""
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": True,
                "message": exc.message,
                "status_code": exc.status_code
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle unexpected exceptions"""
        return JSONResponse(
            status_code=500,
            content={
                "error": True,
                "message": "An unexpected error occurred",
                "status_code": 500
            }
        )
