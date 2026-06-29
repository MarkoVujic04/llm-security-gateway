from dataclasses import dataclass
from functools import lru_cache
import yaml

SEVERITY_WEIGHTS = {"low": 10, "medium": 30, "high": 60, "critical": 90}
VALID_ACTIONS = {"allow", "review", "block"}


@dataclass(frozen=True)
class Rule:
    name: str
    severity: str
    action: str
    patterns: tuple[str, ...]

    @property
    def weight(self) -> int:
        return SEVERITY_WEIGHTS.get(self.severity, 10)


@lru_cache
def load_rules(path: str = "policies/rules.yaml") -> tuple[Rule, ...]:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    rules = []
    for raw in data.get("rules", []):
        action = raw["action"].lower()
        if action not in VALID_ACTIONS:
            raise ValueError(f"Invalid action '{action}' in rule {raw['name']}")
        rules.append(
            Rule(
                name=raw["name"],
                severity=raw["severity"].lower(),
                action=action,
                patterns=tuple(p.lower() for p in raw["patterns"]),
            )
        )
    return tuple(rules)