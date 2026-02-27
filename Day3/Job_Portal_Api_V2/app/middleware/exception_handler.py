from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette import status
import logging


logger = logging.getLogger("app_logger")


# -------------------------------------------------
# HTTP Exception Handler
# -------------------------------------------------

async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP Error: {exc.detail}")

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail
        },
    )


# -------------------------------------------------
# Validation Exception Handler
# -------------------------------------------------

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation Error: {exc.errors()}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": "Validation Error",
            "details": exc.errors()
        },
    )


# -------------------------------------------------
# Global Exception Handler (Unhandled Errors)
# -------------------------------------------------

async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Error: {str(exc)}")

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": "Internal Server Error"
        },
    )