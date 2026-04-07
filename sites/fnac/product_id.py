"""Resolve Fnac basket productID from URLs and HTML.

Fnac product URLs commonly use ``/a{ARTICLE_ID}/`` (8-digit article id). That id is
the same ``productID`` sent to ``POST /basket/add`` in typical captures.
"""

from __future__ import annotations

import re
from urllib.parse import unquote, urlparse

# /a21424410/... or /a21424410
_ARTICLE_PATH = re.compile(r"/a(\d{5,12})(?:/|$)", re.IGNORECASE)

# Query string (?ProductId=…)
_QUERY_ID = re.compile(r"(?:^|[?&])ProductId=(\d+)", re.IGNORECASE)

# Embedded JSON (many Fnac pages)
_JSON_PRODUCT_ID = re.compile(
    r'["\']productID["\']\s*:\s*["\']?(\d+)["\']?',
    re.IGNORECASE,
)
_JSON_PRODUCT_ID_ALT = re.compile(
    r'["\']productId["\']\s*:\s*["\']?(\d+)["\']?',
    re.IGNORECASE,
)


def extract_product_id_from_url(url: str) -> str | None:
    """Best-effort product id from a Fnac product or redirect URL."""
    u = unquote(url.strip())
    p = urlparse(u)
    path = p.path or ""
    m = _ARTICLE_PATH.search(path)
    if m:
        return m.group(1)
    qm = _QUERY_ID.search(p.query or "")
    if qm:
        return qm.group(1)
    return None


def extract_product_id_from_html(html: str) -> str | None:
    """Parse product id from PDP HTML / JSON blobs."""
    for pat in (_JSON_PRODUCT_ID, _JSON_PRODUCT_ID_ALT):
        m = pat.search(html)
        if m:
            return m.group(1)
    m = _ARTICLE_PATH.search(html)
    if m:
        return m.group(1)
    return None


def resolve_product_id(*, url: str | None, html: str | None, explicit: str | None) -> str | None:
    """Prefer explicit id from interface, then URL, then HTML."""
    if explicit and explicit.strip().isdigit():
        return explicit.strip()
    if url:
        from_url = extract_product_id_from_url(url)
        if from_url:
            return from_url
    if html:
        return extract_product_id_from_html(html)
    return None
