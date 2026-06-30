from fastapi import Header, HTTPException, status
from app.config import settings


def require_api_key(x_api_key: str = Header(default="")) -> str:
    if x_api_key not in settings.api_key_set:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key.",
        )
    return f"key-{hash(x_api_key) & 0xffffff:06x}"
