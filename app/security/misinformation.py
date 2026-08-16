import re

FABRICATION_MARKERS = {
    "legal_citation": re.compile(r"\b[A-Z][a-z]+\s+v\.?\s+[A-Z][a-z]+\b"),
    "academic_citation": re.compile(r"\b(et al\.|\(\d{4}\))|doi:\s*\S+", re.I),
    "url_reference": re.compile(r"https?://[^\s)]+", re.I),
    "statistic_claim": re.compile(r"\b\d{1,3}(\.\d+)?%\s+(of|increase|decrease|more|less)\b", re.I),
    "confident_sourcing": re.compile(r"\b(according to (a )?(study|report|research)|studies (show|prove)|research (shows|confirms)|it is (well )?established)\b", re.I),
}


def scan_misinformation(text: str) -> list[str]:
    """Flag unverifiable high-confidence claims prone to fabrication."""
    return [name for name, pat in FABRICATION_MARKERS.items() if pat.search(text)]