from typing import Protocol

class LLMProvider(Protocol):
    def chat(self, model: str, messages: list[dict]) -> str: ...