from fastapi import APIRouter
from app.schemas import ProxyRequest, ProxyResponse
from app.llm.mock_provider import mock_provider
from app.security.policy import evaluate

router = APIRouter(prefix="/v1/proxy", tags=["proxy"])


@router.post("/chat", response_model=ProxyResponse)
def proxy_chat(req: ProxyRequest):
    messages = [m.model_dump() for m in req.messages]

    user_text = " ".join(m["content"] for m in messages if m["role"] == "user")

    decision = evaluate(user_text)

    if decision.decision == "BLOCK":
        return ProxyResponse(
            decision="BLOCK",
            risk_score=decision.risk_score,
            content=None,
            reason="Request blocked by security policy.",
        )

    content = mock_provider.chat(req.model, messages)

    return ProxyResponse(
        decision=decision.decision,
        risk_score=decision.risk_score,
        content=content,
        reason=decision.reason
    )