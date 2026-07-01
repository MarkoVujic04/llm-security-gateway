from app.llm.openai_provider import OpenAIProvider
from app.config import settings


class LMStudioProvider(OpenAIProvider):

    def __init__(self):
        super().__init__(base_url=settings.lmstudio_base_url)
        self.api_key = "lm-studio"  # any non-empty string; LM Studio ignores it