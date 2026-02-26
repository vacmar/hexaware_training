from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
from app.core.logger import logger

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log all incoming requests and their execution time.
    Logs: HTTP method, path, and time taken to process the request.
    """
    
    async def dispatch(self, request: Request, call_next):
        # Record start time
        start_time = time.time()
        
        # Log incoming request
        logger.info(f"Incoming request: {request.method} {request.url.path}")
        
        # Process the request
        response = await call_next(request)
        
        # Calculate execution time
        execution_time = time.time() - start_time
        
        # Log response details
        logger.info(
            f"Completed {request.method} {request.url.path} - "
            f"Status: {response.status_code} - "
            f"Time: {execution_time:.4f}s"
        )
        
        return response
