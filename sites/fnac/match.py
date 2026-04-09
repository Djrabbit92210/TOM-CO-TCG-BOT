"""Normalize names and decide if a search hit matches the user's intent."""

from __future__ import annotations

import re
import unicodedata

from scrapers.keyword_engine import matches_keywords


def normalize_for_match(text: str) -> str:
    """Lowercase, strip accents, collapse whitespace, drop most punctuation."""
    if not text:
        return ""
    nfkd = unicodedata.normalize("NFKD", text)
    ascii_like = "".join(c for c in nfkd if not unicodedata.combining(c))
    lowered = ascii_like.lower()
    lowered = re.sub(r"[^\w\s]+", " ", lowered)
    return re.sub(r"\s+", " ", lowered).strip()


def token_set(text: str) -> set[str]:
    """Significant tokens (length > 1) after normalization."""
    n = normalize_for_match(text)
    return {t for t in n.split() if len(t) > 1}


def overlap_score(query: str, title: str) -> float:
    """Jaccard-like overlap between query tokens and title tokens."""
    q, t = token_set(query), token_set(title)
    if not q or not t:
        return 0.0
    inter = len(q & t)
    union = len(q | t)
    return inter / union if union else 0.0


def listing_matches(
    title: str,
    *,
    name_hint: str = "",
    keyword_groups: list[list[str]] | None = None,
    exclude_substrings: list[str] | None = None,
    min_score: float = 0.25,
) -> bool:
    """
    True if the listing should be treated as the target product.

    - ``name_hint``: free text from the interface (partial product name).
    - ``keyword_groups``: AND-of-OR groups (same semantics as ``matches_keywords``).
    - ``exclude_substrings``: if any appears in normalized title, reject.
    - ``min_score``: minimum token overlap vs ``name_hint`` when groups are empty.
    """
    if exclude_substrings:
        nt = normalize_for_match(title)
        for ex in exclude_substrings:
            nex = normalize_for_match(ex)
            if nex and nex in nt:
                return False

    k_ok = matches_keywords(title, keyword_groups) if keyword_groups else True
    n_ok = overlap_score(name_hint, title) >= min_score if name_hint.strip() else True

    if keyword_groups and name_hint.strip():
        return k_ok and n_ok
    if keyword_groups:
        return k_ok
    if name_hint.strip():
        return n_ok
    return False


def pick_best_listing(
    listings: list[dict],
    *,
    name_hint: str = "",
    keyword_groups: list[list[str]] | None = None,
    exclude_substrings: list[str] | None = None,
    min_score: float = 0.25,
) -> tuple[dict | None, float]:
    """Choose listing with highest overlap among those that pass filters."""
    best: dict | None = None
    best_score = -1.0
    for L in listings:
        title = L.get("title") or ""
        if not listing_matches(
            title,
            name_hint=name_hint,
            keyword_groups=keyword_groups,
            exclude_substrings=exclude_substrings,
            min_score=min_score,
        ):
            continue
        if name_hint.strip():
            sc = overlap_score(name_hint, title)
        elif keyword_groups:
            sc = 1.0
        else:
            sc = 0.0
        if sc > best_score:
            best_score = sc
            best = L
    return best, best_score
