from dataclasses import dataclass
from app.security.rules import Rule, load_rules


@dataclass
class Match:
    rule: Rule
    matched_patterns: list[str]


def scan_text(text: str, rules: tuple[Rule, ...] | None = None) -> list[Match]:
    rules = rules or load_rules()
    text_lower = text.lower()
    matches: list[Match] = []

    for rule in rules:
        hit = [p for p in rule.patterns if p in text_lower]
        if hit:
            matches.append(Match(rule=rule, matched_patterns=hit))

    return matches
