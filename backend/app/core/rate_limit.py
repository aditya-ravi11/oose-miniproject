import asyncio
import time
from collections import defaultdict, deque
from typing import Deque

from fastapi import HTTPException, Request, status

from .config import get_settings

_BUCKETS: dict[str, Deque[float]] = defaultdict(deque)
_LOCK = asyncio.Lock()


async def rate_limit_middleware(request: Request, call_next):
    settings = get_settings()
    identifier = request.client.host if request.client else "anonymous"
    now = time.monotonic()
    async with _LOCK:
        bucket = _BUCKETS[identifier]
        while bucket and now - bucket[0] > 60:
            bucket.popleft()
        if len(bucket) >= settings.rate_limit_per_min:
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Slow down")
        bucket.append(now)
    response = await call_next(request)
    return response