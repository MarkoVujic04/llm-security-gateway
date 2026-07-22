from functools import lru_cache
import yaml


@lru_cache
def load_tool_policy(path: str = "policies/tools.yaml") -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def check_tools(requested: list[dict]) -> tuple[bool, list[str]]:
    """Return (allowed, offending_tools)."""
    policy = load_tool_policy()
    allowed = set(policy.get("allowed_tools", []))
    denied = set(policy.get("denied_tools", []))

    offending = []
    for tool in requested or []:
        name = tool.get("name", "")
        if name in denied or name not in allowed:
            offending.append(name)

    return (len(offending) == 0, offending)
