import re
from sqlalchemy.orm import Session
from app.db.models import SecurityEvent

SECRET_PATTERN = re.compile(r"(sk-[A-Za-z0-9]{8,}|password\S*|token\S*)", re.I)


def _redact(text: str, limit: int = 300) -> str:
    redacted = SECRET_PATTERN.sub("[REDACTED]", text)
    return redacted[:limit]


def log_event(db: Session, *, api_key_id: str, decision: str,
              risk_score: int, matched_rules: list[str],
              prompt: str, reason: str) -> None:
    event = SecurityEvent(
        api_key_id=api_key_id,
        decision=decision,
        risk_score=risk_score,
        matched_rules=",".join(matched_rules),
        prompt_snippet=_redact(prompt),
        reason=reason,
    )
    db.add(event)
    db.commit()
