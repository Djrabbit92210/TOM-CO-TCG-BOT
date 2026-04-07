"""Fnac HTTP routes: storefront (www) vs account/checkout (secure).

Confidence tags:
  confirmed   — observed in browser (e.g. POST body capture).
  inferred    — common REST sibling of a confirmed route; verify with DevTools.
  page        — user-facing HTML URL (Referer, sanity checks), not JSON API.
  needs_capture — expected step for checkout; path/method not fixed here — record from Network tab.

Flow A→Z (what to capture next on your machine):
  A. Session/cookies on www.fnac.com (GET / + cookie banner if needed).
  B. Add line — POST /basket/add (confirmed).
  C. Read cart — try JSON siblings below; if HTML only, parse cart page or capture XHR.
  D. Update qty / remove line — often POST/PATCH/DELETE under /basket/ (needs_capture).
  E. Checkout — moves to secure.fnac.com (login, addresses, shipping, payment) — needs_capture.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Confidence = Literal["confirmed", "inferred", "page", "needs_capture"]


@dataclass(frozen=True)
class Endpoint:
    """Single HTTP call site."""

    method: str
    path: str
    host: Literal["www", "secure"]
    about: str
    confidence: Confidence


def _u(host: Literal["www", "secure"], path: str) -> str:
    base = "https://www.fnac.com" if host == "www" else "https://secure.fnac.com"
    return f"{base}{path}"


# --- www.fnac.com — storefront / basket API ---------------------------------

HOME = Endpoint("GET", "/", "www", "Bootstrap session cookies.", "page")

SEARCH = Endpoint(
    "GET",
    "/SearchResult/ResultList.aspx",
    "www",
    "Search results; use as Referer for basket calls.",
    "page",
)

BASKET_ADD = Endpoint(
    "POST",
    "/basket/add",
    "www",
    "Add items JSON array [{productID, referential, quantity, offer, shopID, masterProductID}].",
    "confirmed",
)

# Typical companions on the same host (verify in DevTools → XHR/fetch filtered by "basket")
BASKET_GET = Endpoint(
    "GET",
    "/basket",
    "www",
    "Often cart HTML or redirect; try Accept: application/json first.",
    "inferred",
)

BASKET_SUMMARY = Endpoint(
    "GET",
    "/basket/summary",
    "www",
    "Mini-cart / line count JSON on many stacks — may 404 on Fnac; capture real URL if different.",
    "inferred",
)

BASKET_LINES = Endpoint(
    "GET",
    "/basket/lines",
    "www",
    "Alternate name for cart JSON — capture if Fnac uses it.",
    "inferred",
)

BASKET_UPDATE = Endpoint(
    "POST",
    "/basket/update",
    "www",
    "Change quantity — payload needs_capture.",
    "needs_capture",
)

BASKET_REMOVE = Endpoint(
    "POST",
    "/basket/remove",
    "www",
    "Remove line — payload needs_capture.",
    "needs_capture",
)

# Product JSON (if exposed — capture from product page network)
PRODUCT_API = Endpoint(
    "GET",
    "/api/product/",
    "www",
    "Prefix only; full path/query from product page XHR (e.g. offers, stock).",
    "needs_capture",
)


# --- secure.fnac.com — login & checkout -------------------------------------

LOGON_PAGE = Endpoint(
    "GET",
    "/interaction/connection",
    "secure",
    "Current Fnac login entry (path may change — capture from 'Se connecter').",
    "needs_capture",
)

ACCOUNT_HOME = Endpoint(
    "GET",
    "/Account/Profil/Default.aspx",
    "secure",
    "Legacy account hub; may redirect — use for discovery only.",
    "page",
)

CHECKOUT_ENTRY = Endpoint(
    "GET",
    "/checkout",
    "secure",
    "Hypothetical checkout entry — capture actual URL when clicking 'Commander'.",
    "needs_capture",
)

# Legacy basket recalc (often dead or 403); listed so you recognize it in old writeups
LEGACY_BASKET_RECALC = Endpoint(
    "POST",
    "/Account/Basket/IntermediaryShoppingCartRecalculate.aspx",
    "secure",
    "Legacy WebForms — do not rely on; capture modern checkout XHR instead.",
    "needs_capture",
)


def url(ep: Endpoint, *, query: str | None = None) -> str:
    u = _u(ep.host, ep.path)
    if query:
        sep = "&" if "?" in u else "?"
        return f"{u}{sep}{query.lstrip('?&')}"
    return u


# Ordered checklist for documenting your own captures
CHECKLIST: tuple[Endpoint, ...] = (
    HOME,
    SEARCH,
    BASKET_ADD,
    BASKET_GET,
    BASKET_SUMMARY,
    BASKET_LINES,
    BASKET_UPDATE,
    BASKET_REMOVE,
    LOGON_PAGE,
    CHECKOUT_ENTRY,
)
