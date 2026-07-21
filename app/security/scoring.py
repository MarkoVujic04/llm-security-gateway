from app.security.scanner import Match
from app.security.secrets import detect_secrets

LOW, MEDIUM, HIGH, CRITICAL = 30, 60, 85, 100
MAX_PROMPT_LEN = 8000


def calculate_risk(text: str, matches: list[Match]) -> int:
    score = 0

    for m in matches:
        score += m.rule.weight
        score += (len(m.matched_patterns) - 1) * 5

    if any(m.rule.severity == "critical" for m in matches):
        score += 15

    found_secrets = detect_secrets(text)
    if found_secrets:
        score += 25

    if len(text) > MAX_PROMPT_LEN:
        score += 20

    return max(0, min(100, score))


def risk_band(score: int) -> str:
    if score <= LOW:
        return "low"
    if score <= MEDIUM:
        return "medium"
    if score <= HIGH:
        return "high"
    return "critical"
