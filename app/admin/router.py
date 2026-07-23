import csv
import io
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import SecurityEvent
from app.auth.dependencies import require_api_key

router = APIRouter(prefix="/v1/admin", tags=["admin"])


@router.get("/events")
def list_events(
    min_score: int = Query(60, ge=0, le=100),
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db),
    _: str = Depends(require_api_key),
):
    stmt = (
        select(SecurityEvent)
        .where(SecurityEvent.risk_score >= min_score)
        .order_by(desc(SecurityEvent.created_at))
        .limit(limit)
    )
    rows = db.execute(stmt).scalars().all()
    return [
        {
            "id": e.id, "created_at": e.created_at.isoformat(),
            "api_key_id": e.api_key_id, "decision": e.decision,
            "risk_score": e.risk_score, "matched_rules": e.matched_rules,
            "reason": e.reason,
        }
        for e in rows
    ]


@router.get("/events/export")
def export_events(
    fmt: str = Query("json", pattern="^(json|csv)$"),
    db: Session = Depends(get_db),
    _: str = Depends(require_api_key),
):
    rows = db.execute(
        select(SecurityEvent).order_by(desc(SecurityEvent.created_at))
    ).scalars().all()

    data = [
        {
            "id": e.id, "created_at": e.created_at.isoformat(),
            "api_key_id": e.api_key_id, "decision": e.decision,
            "risk_score": e.risk_score, "matched_rules": e.matched_rules,
            "reason": e.reason,
        }
        for e in rows
    ]

    if fmt == "json":
        return data

    buf = io.StringIO()
    if data:
        writer = csv.DictWriter(buf, fieldnames=list(data[0].keys()))
        writer.writeheader()
        writer.writerows(data)
    return StreamingResponse(
        iter([buf.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=events.csv"},
    )
