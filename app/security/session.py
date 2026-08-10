import json
import time
import redis
from app.config import settings

_r = redis.from_url(settings.redis_url, decode_responses=True)

WINDOW = 6
TTL_SECONDS = 1800
DECAY = 0.8


def record_turn(session_id: str, text: str, risk: int) -> None:
    key = f"session:{session_id}"
    entry = json.dumps({"t": time.time(), "text": text[:500], "risk": risk})
    try:
        _r.lpush(key, entry)
        _r.ltrim(key, 0, WINDOW - 1)
        _r.expire(key, TTL_SECONDS)
    except redis.exceptions.ConnectionError:
        return


def recent_context(session_id: str) -> list[dict]:
    key = f"session:{session_id}"
    try:
        raw = _r.lrange(key, 0, WINDOW - 1)
    except redis.exceptions.ConnectionError:
        return []
    return [json.loads(x) for x in raw]


def cumulative_risk(session_id: str) -> int:
    """Decaying sum of recent turn risks — spikes when risk clusters."""
    turns = recent_context(session_id)
    total = 0.0
    for i, turn in enumerate(turns):
        total += turn["risk"] * (DECAY ** i)
    return min(100, int(total))