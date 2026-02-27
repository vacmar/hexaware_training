import time
import logging
from fastapi import Request


# -------------------------------------------------
# Logger Configuration
# -------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger("app_logger")


# -------------------------------------------------
# Logging Middleware
# -------------------------------------------------

async def logging_middleware(request: Request, call_next):
    """
    Logs request method, URL, status code and execution time.
    """

    start_time = time.time()

    logger.info(f"Incoming request: {request.method} {request.url.path}")

    response = await call_next(request)

    process_time = time.time() - start_time

    logger.info(
        f"Completed: {request.method} {request.url.path} "
        f"Status: {response.status_code} "
        f"Time: {process_time:.4f}s"
    )

    return response