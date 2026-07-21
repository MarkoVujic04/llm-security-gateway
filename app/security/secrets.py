import re

PATTERNS = {
    "openai_key": re.compile(r"sk-[A-Za-z0-9\-]{16,}"),
    "aws_key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "private_key": re.compile(r"-----BEGIN (?:RSA )?PRIVATE KEY-----"),
    "bearer_token": re.compile(r"Bearer\s+[A-Za-z0-9._-]{16,}"),
    "email": re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"),
    "credit_card": re.compile(r"\b(?:\d[ -]*?){13,16}\b"),
}


def detect_secrets(text: str) -> list[str]:
    return [name for name, pat in PATTERNS.items() if pat.search(text)]


def redact_secrets(text: str) -> str:
    for pat in PATTERNS.values():
        text = pat.sub("[REDACTED]", text)
    return text
