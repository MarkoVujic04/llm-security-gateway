from datetime import datetime, timedelta, timezone
import jwt
from app.config import settings

ALGORITHM = "HS256"


def create_token(subject: str, minutes: int = 60) -> str:
    payload = {
        "sub": subject,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=minutes),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=ALGORITHM)


def verify_token(token: str) -> str:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[ALGORITHM])
        return payload["sub"]
    except jwt.PyJWTError:
        raise ValueError("Invalid token")