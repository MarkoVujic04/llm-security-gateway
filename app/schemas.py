from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str = Field(..., pattern="^(system|user|assistant|tool)$")
    content: str


class ProxyRequest(BaseModel):
    model: str = "mock-model"
    messages: list[ChatMessage]
    tools: list[dict] | None = None


class ProxyResponse(BaseModel):
    decision: str
    risk_score: int = 0
    content: str | None = None
    reason: str | None = None
