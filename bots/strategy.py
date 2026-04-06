"""Choose API vs browser scraping based on site capabilities."""


def prefer_api_for_detection(site_supports_api: bool) -> bool:
    """Return True if detection should use HTTP/API path when available."""
    return site_supports_api
