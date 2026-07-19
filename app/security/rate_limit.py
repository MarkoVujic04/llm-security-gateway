from fastapi import HTTPException, status
import redis
from app.config import settings
import logging

logger = logging.getLogger(__name__)
_r = redis.from_url(settings.redis_url, decode_responses=True)

LIMIT = 20
WINDOW_SECONDS = 60

def enforce_rate_limit(api_key_id: str) -> None:
    key = f"ratelimit:{api_key_id}"
    try:
        count = _r.incr(key)
        if count == 1:
            _r.expire(key, WINDOW_SECONDS)
    except redis.exceptions.ConnectionError:
        logger.warning("Redis unavailable — skipping rate limit for %s", api_key_id)
        return

    if count > LIMIT:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded ({LIMIT}/{WINDOW_SECONDS}s).",
        )
