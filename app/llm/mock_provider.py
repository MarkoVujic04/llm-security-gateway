class MockLLMProvider:
    """Deterministic fake LLM for development and testing."""

    def chat(self, model: str, messages: list[dict]) -> str:
        last_user = next(
            (m["content"] for m in reversed(messages) if m["role"] == "user"),
            "",
        )

        if "leak secret" in last_user.lower():
            return "Sure, the key is sk-test-ABC123XYZsecretvalue000"

        return f"[mock-{model}] You said: {last_user}"


mock_provider = MockLLMProvider()
