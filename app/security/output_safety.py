import re

DANGEROUS_OUTPUT = {
    "html_script": re.compile(r"<script\b", re.I),
    "js_event_handler": re.compile(r"on(click|error|load)\s*=", re.I),
    "sql_write": re.compile(r"\b(DROP|DELETE|INSERT|UPDATE|ALTER)\s+.*\b(TABLE|INTO|FROM)\b", re.I),
    "shell_command": re.compile(r"\b(rm\s+-rf|curl\s+.*\|\s*sh|wget\s+.*\|\s*bash)\b", re.I),
    "template_injection": re.compile(r"\{\{.*\}\}"),
}


def scan_output_safety(text: str) -> list[str]:
    return [name for name, pat in DANGEROUS_OUTPUT.items() if pat.search(text)]