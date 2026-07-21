try:
    from presidio_analyzer import AnalyzerEngine
    _analyzer = AnalyzerEngine()
    _available = True
except Exception:
    _available = False


def detect_pii(text: str) -> list[str]:
    if not _available:
        return []
    results = _analyzer.analyze(text=text, language="en")
    return sorted({r.entity_type for r in results})
