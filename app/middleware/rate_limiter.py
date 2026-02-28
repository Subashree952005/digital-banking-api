from fastapi import Request
from fastapi.responses import JSONResponse
from collections import defaultdict
import time

request_counts = defaultdict(list)
RATE_LIMIT = 100
WINDOW_SECONDS = 60


async def rate_limiter_middleware(request: Request, call_next):
    client_ip = request.client.host
    now = time.time()

    request_counts[client_ip] = [
        t for t in request_counts[client_ip] if now - t < WINDOW_SECONDS
    ]

    if len(request_counts[client_ip]) >= RATE_LIMIT:
        return JSONResponse(
            status_code=429,
            content={"detail": "Too many requests. Please slow down."},
        )

    request_counts[client_ip].append(now)
    return await call_next(request)
