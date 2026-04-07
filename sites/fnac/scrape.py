"""Parse Fnac search and product HTML for id, price, availability."""

from __future__ import annotations

import re
from dataclasses import dataclass
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from sites.fnac import config

# French price: 49,99 € or 49.99 €
_PRICE_EUR = re.compile(
    r"(\d{1,4}(?:[.,]\d{2})?)\s*(?:€|EUR)",
    re.IGNORECASE,
)


@dataclass
class Listing:
    url: str
    title: str
    product_id: str | None
    price_eur: float | None
    add_to_cart_hint: bool


def _parse_price_eur(text: str) -> float | None:
    if not text:
        return None
    m = _PRICE_EUR.search(text.replace("\xa0", " "))
    if not m:
        return None
    raw = m.group(1).replace(",", ".")
    try:
        return float(raw)
    except ValueError:
        return None


def _norm_url(href: str) -> str | None:
    if not href or href.startswith("#") or "javascript:" in href.lower():
        return None
    full = urljoin(config.BASE_URL + "/", href)
    if "fnac.com" not in full:
        return None
    return full.split("#")[0]


def _block_signals(html_lower: str) -> tuple[bool, float | None]:
    """Heuristics for availability + price inside a HTML chunk."""
    unavailable = any(
        x in html_lower
        for x in (
            "indisponible",
            "rupture de stock",
            "non disponible",
            "vendeur externe",
        )
    )
    cart = "ajouter au panier" in html_lower or "ajouter&nbsp;au&nbsp;panier" in html_lower
    add_ok = cart and not unavailable
    price = _parse_price_eur(html_lower)
    return add_ok, price


def parse_search_results(html: str) -> list[Listing]:
    """
    Extract product cards from a Fnac search results page.

    DOM changes over time; this uses ``/a{digits}/`` links as anchors.
    """
    soup = BeautifulSoup(html, "html.parser")
    seen: set[str] = set()
    out: list[Listing] = []

    for a in soup.find_all("a", href=True):
        href = a.get("href", "")
        full = _norm_url(href)
        if not full or "/a" not in full.lower():
            continue
        m = re.search(r"/a(\d{5,12})/", full, re.I)
        if not m:
            continue
        pid = m.group(1)
        if full in seen:
            continue
        seen.add(full)

        title = (a.get("title") or "").strip() or a.get_text(" ", strip=True)
        # Walk up a few levels to capture price + CTA snippet
        node = a
        chunks: list[str] = []
        for _ in range(6):
            if node is None:
                break
            chunks.append(node.decode())
            node = node.parent
        block = "\n".join(chunks)
        low = block.lower()
        add_ok, price = _block_signals(low)

        out.append(
            Listing(
                url=full,
                title=title,
                product_id=pid,
                price_eur=price,
                add_to_cart_hint=add_ok,
            )
        )

    return out


def parse_product_page(html: str, page_url: str) -> tuple[str | None, float | None, bool]:
    """
    From a product detail page: product id, price, whether add-to-cart looks possible.

    Returns:
        product_id, price_eur, looks_purchasable
    """
    from sites.fnac.product_id import extract_product_id_from_html, extract_product_id_from_url

    pid = extract_product_id_from_url(page_url) or extract_product_id_from_html(html)
    low = html.lower()
    purchasable, price_near_cta = _block_signals(low)
    price = _parse_price_eur(html) or price_near_cta
    return pid, price, purchasable


def listing_to_dict(L: Listing) -> dict:
    return {
        "url": L.url,
        "title": L.title,
        "product_id": L.product_id,
        "price_eur": L.price_eur,
        "add_to_cart_hint": L.add_to_cart_hint,
    }
