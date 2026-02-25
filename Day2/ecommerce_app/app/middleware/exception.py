from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import traceback

class GlobalExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            # Log the exception details (you can use logging instead of print in production)
            print(f"Exception occurred: {str(e)}")
            traceback.print_exc()
            
            # Return a generic error response
            return JSONResponse(
                status_code=500,
                content={"detail": "An unexpected error occurred. Please try again later."}
            )