from app.security.semantic import semantic_score
from app.security.judge import judge_score

SEMANTIC_ATTACK = 0.60
SEMANTIC_BENIGN = 0.30


def layered_score(text: str) -> tuple[int, str]:
    """
    Two-layer detection.
    Returns (risk 0-100, reason). Takes the STRICTER of the two layers.
    """
    sem = semantic_score(text)
    sem_risk = int(sem * 100)

    if sem >= SEMANTIC_ATTACK:
        return sem_risk, f"semantic match ({sem:.2f})"

    if sem < SEMANTIC_BENIGN:
        return sem_risk, f"semantic low ({sem:.2f})"

    j_risk, j_reason = judge_score(text)
    if j_risk >= sem_risk:
        return j_risk, f"judge: {j_reason}"
    return sem_risk, f"semantic ambiguous ({sem:.2f})"