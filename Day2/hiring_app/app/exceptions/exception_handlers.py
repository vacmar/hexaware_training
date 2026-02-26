from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware
import traceback
from app.core.logger import logger

from app.exceptions.custom_exception import (
    UserNotFoundException,
    JobNotFoundException,
    ApplicationNotFoundException,
    DuplicateEmailException,
    DuplicateApplicationException,
    InvalidStatusTransitionException,
    HiringAppException
)

# Custom exception handlers
async def user_not_found_handler(request: Request, exc: UserNotFoundException):
    """Handler for UserNotFoundException"""
    logger.error(f"UserNotFoundException: {exc.message}")
    return JSONResponse(
        status_code=404,
        content={"detail": exc.message}
    )

async def job_not_found_handler(request: Request, exc: JobNotFoundException):
    """Handler for JobNotFoundException"""
    logger.error(f"JobNotFoundException: {exc.message}")
    return JSONResponse(
        status_code=404,
        content={"detail": exc.message}
    )

async def application_not_found_handler(request: Request, exc: ApplicationNotFoundException):
    """Handler for ApplicationNotFoundException"""
    logger.error(f"ApplicationNotFoundException: {exc.message}")
    return JSONResponse(
        status_code=404,
        content={"detail": exc.message}
    )

async def duplicate_email_handler(request: Request, exc: DuplicateEmailException):
    """Handler for DuplicateEmailException"""
    logger.error(f"DuplicateEmailException: {exc.message}")
    return JSONResponse(
        status_code=400,
        content={"detail": exc.message}
    )

async def duplicate_application_handler(request: Request, exc: DuplicateApplicationException):
    """Handler for DuplicateApplicationException"""
    logger.error(f"DuplicateApplicationException: {exc.message}")
    return JSONResponse(
        status_code=400,
        content={"detail": exc.message}
    )

async def invalid_status_transition_handler(request: Request, exc: InvalidStatusTransitionException):
    """Handler for InvalidStatusTransitionException"""
    logger.error(f"InvalidStatusTransitionException: {exc.message}")
    return JSONResponse(
        status_code=400,
        content={"detail": exc.message}
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handler for request validation errors"""
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error",
            "errors": exc.errors()
        }
    )

class GlobalExceptionMiddleware(BaseHTTPMiddleware):
    """
    Global exception handler middleware.
    Catches all unhandled exceptions and returns a generic error response.
    """
    
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            # Log the exception details
            logger.error(f"Unhandled exception: {str(e)}")
            logger.error(traceback.format_exc())
            
            # Return a generic error response
            return JSONResponse(
                status_code=500,
                content={"detail": "An unexpected error occurred. Please try again later."}
            )

def register_exception_handlers(app):
    """
    Register all custom exception handlers with the FastAPI app.
    """
    app.add_exception_handler(UserNotFoundException, user_not_found_handler)
    app.add_exception_handler(JobNotFoundException, job_not_found_handler)
    app.add_exception_handler(ApplicationNotFoundException, application_not_found_handler)
    app.add_exception_handler(DuplicateEmailException, duplicate_email_handler)
    app.add_exception_handler(DuplicateApplicationException, duplicate_application_handler)
    app.add_exception_handler(InvalidStatusTransitionException, invalid_status_transition_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
