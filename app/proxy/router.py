from fastapi import APIRouter
from app.schemas import ProxyRequest, ProxyResponse
from app.llm.mock_provider import mock_provider

router = APIRouter(prefix="/v1/proxy", tags=["proxy"])


@router.post("/chat", response_model=ProxyResponse)
def proxy_chat(req: ProxyRequest):
    messages = [m.model_dump() for m in req.messages]

    content = mock_provider.chat(req.model, messages)

    return ProxyResponse(decision="ALLOW", risk_score=0, content=content)