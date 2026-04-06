"""Retry helpers with backoff (to be implemented)."""


def retry_stub(fn, max_attempts: int = 3) -> None:
    """Placeholder."""
    for _ in range(max_attempts):
        try:
            fn()
            return
        except Exception:
            continue
