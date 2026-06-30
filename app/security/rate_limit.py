from fastapi import HTTPException, status
import redis
from app.config import settings

_r = redis.from_url(settings.redis_url, decode_responses=True)

LIMIT = 20
WINDOW_SECONDS = 60

def enforce_rate_limit(api_key_id: str) -> None:
    key = f"ratelimit:{api_key_id}"
    count = _r.incr(key)
    if count == 1:
        _r.expire(key, WINDOW_SECONDS)
        if count > LIMIT:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded ({LIMIT}/{WINDOW_SECONDS}s)."
            )
