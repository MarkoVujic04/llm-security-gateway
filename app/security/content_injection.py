import re


INJECTION_MARKERS = [
    re.compile(r"\bignore\s+(all\s+|the\s+|your\s+)?(previous|prior|above)\b", re.I),
    re.compile(r"\byou\s+are\s+now\b", re.I),
    re.compile(r"\bdisregard\s+(your|the|all)\b", re.I),
    re.compile(r"\bnew\s+instructions?\b", re.I),
    re.compile(r"\bsystem\s+prompt\b", re.I),
    re.compile(r"\bdo\s+not\s+(tell|mention|inform|reveal)\b", re.I),
    re.compile(r"\b(act|behave|respond)\s+as\s+(if|though|a)\b", re.I),
    re.compile(r"\boverride\b.*\b(instructions?|rules?|settings?)\b", re.I),
    re.compile(r"\bpretend\s+(you|to)\b", re.I),
]

OBFUSCATION_MARKERS = [
    re.compile(r"[\u200b\u200c\u200d\u2060\ufeff]"),
    re.compile(r"<!--.*?-->", re.DOTALL),
    re.compile(r"color\s*:\s*(#fff|#ffffff|white)", re.I),
    re.compile(r"font-size\s*:\s*0", re.I),
]


def scan_untrusted_content(text: str) -> list[str]:
    """Flag instruction-like or hidden content embedded in external data."""
    findings = []
    for pat in INJECTION_MARKERS:
        if pat.search(text):
            findings.append(f"embedded_instruction:{pat.pattern[:30]}")
    for pat in OBFUSCATION_MARKERS:
        if pat.search(text):
            findings.append("hidden_text_obfuscation")
            break
    return findings
