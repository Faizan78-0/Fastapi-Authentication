from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import time

class LoggingMiddleware(BaseException):
    async def logging_middleware(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        print(f"Request: {request.method} {request.url} completed in {process_time:.2f} seconds")
        return response
