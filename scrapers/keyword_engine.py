"""Match product descriptions against keyword groups (AND / OR)."""


def matches_keywords(text: str, required_groups: list[list[str]]) -> bool:
    """True if every group has at least one keyword present in text (stub)."""
    lowered = text.lower()
    for group in required_groups:
        if not any(k.lower() in lowered for k in group):
            return False
    return True
