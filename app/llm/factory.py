from app.llm.mock_provider import mock_provider
from app.llm.openai_provider import OpenAIProvider
from app.llm.lmstudio_provider import LMStudioProvider


def get_provider(model: str):
    if model.startswith("mock"):
        return mock_provider
    if model.startswith("gpt-"):
        return OpenAIProvider()
    return LMStudioProvider()
