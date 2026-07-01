from fastapi import APIRouter, Depends, HTTPException
from app.schemas import ProxyRequest, ProxyResponse
from app.llm.mock_provider import mock_provider
from app.security.policy import evaluate
from app.security.audit import log_event
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.auth.dependencies import require_api_key
from app.security.rate_limit import enforce_rate_limit
from app.llm.factory import get_provider

router = APIRouter(prefix="/v1/proxy", tags=["proxy"])


@router.post("/chat", response_model=ProxyResponse)
def proxy_chat(
        req: ProxyRequest,
        db: Session = Depends(get_db),
        api_key_id: str = Depends(require_api_key)
):
    enforce_rate_limit(api_key_id)

    messages = [m.model_dump() for m in req.messages]

    user_text = " ".join(m["content"] for m in messages if m["role"] == "user")

    decision = evaluate(user_text)

    log_event(
        db,
        api_key_id=api_key_id,
        decision=decision.decision,
        risk_score=decision.risk_score,
        matched_rules=decision.matched_rules,
        prompt=user_text,
        reason=decision.reason
    )

    if decision.decision == "BLOCK":
        return ProxyResponse(
            decision="BLOCK",
            risk_score=decision.risk_score,
            content=None,
            reason="Request blocked by security policy.",
        )

    provider = get_provider(req.model)

    try:
        content = provider.chat(req.model, messages)
    except RuntimeError:
        raise HTTPException(status_code=502, detail="Upstream LLM error")

    return ProxyResponse(
        decision=decision.decision,
        risk_score=decision.risk_score,
        content=content,
        reason=decision.reason
    )