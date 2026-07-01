import httpx
from app.config import settings


class OpenAIProvider:
    def __init__(self, base_url: str = "https://api.openai.com/v1"):
        self.base_url = base_url.rstrip("/")
        self.api_key = settings.openai_api_key

    def chat(self, model: str, messages: list[dict]) -> str:
        try:
            resp = httpx.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"model": model, "messages": messages},
                timeout=120,
            )
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]
        except Exception:
            raise RuntimeError("LLM provider error")
        