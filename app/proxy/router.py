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
from app.security.secrets import detect_secrets, redact_secrets
from app.security.tools import check_tools

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

    if req.tools:
        ok, offending = check_tools(req.tools)
        if not ok:
            log_event(
                db,
                api_key_id=api_key_id,
                decision="BLOCK",
                risk_score=95,
                matched_rules=[f"tool:{t}" for t in offending],
                prompt=user_text,
                reason=f"Disallowed tools: {offending}",
            )
            return ProxyResponse(
                decision="BLOCK",
                risk_score=95,
                content=None,
                reason="Requested tool is not permitted.",
            )

    provider = get_provider(req.model)

    try:
        content = provider.chat(req.model, messages)
    except RuntimeError:
        raise HTTPException(status_code=502, detail="Upstream LLM error")

    leaked = detect_secrets(content)
    if leaked:
        log_event(
            db,
            api_key_id=api_key_id,
            decision="REVIEW",
            risk_score=90,
            matched_rules=[f"output_secret:{s}" for s in leaked],
            prompt=user_text,
            reason="Secret detected in model output",
        )
        content = redact_secrets(content)

    out_decision = evaluate(content)
    if out_decision.decision == "BLOCK":
        content = "[response withheld by security policy]"

    return ProxyResponse(
        decision=decision.decision,
        risk_score=decision.risk_score,
        content=content,
        reason=decision.reason,
    )