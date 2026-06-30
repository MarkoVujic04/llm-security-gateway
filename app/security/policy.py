from dataclasses import dataclass
from app.security.scanner import Match
from app.security.scoring import calculate_risk

ACTION_PRIORITY = {"allow": 0, "review": 1, "block": 2}


@dataclass
class Decision:
    decision: str
    risk_score: int
    reason: str
    matched_rules: list[str]


def evaluate(text: str) -> Decision:
    from app.security.scanner import scan_text
    matches = scan_text(text)
    score = calculate_risk(text, matches)

    # Strictest action among matched rules
    action = "allow"
    for m in matches:
        if ACTION_PRIORITY[m.rule.action] > ACTION_PRIORITY[action]:
            action = m.rule.action

    if action == "allow" and score >= 61:
        action = "review"

    matched_names = [m.rule.name for m in matches]
    reason = (
        f"Matched: {', '.join(matched_names)}" if matched_names
        else "No rules matched"
    )

    return Decision(
        decision=action.upper(),
        risk_score=score,
        reason=reason,
        matched_rules=matched_names,
    )
