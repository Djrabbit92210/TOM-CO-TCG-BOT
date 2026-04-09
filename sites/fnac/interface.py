"""Map UI / API JSON payloads into ``FnacWatchConfig``."""

from __future__ import annotations

from typing import Any

from sites.fnac.models import FnacWatchConfig


def fnac_watch_from_interface(raw: dict[str, Any]) -> FnacWatchConfig:
    """
    Expected keys (flexible naming):

    - ``mode``: ``"search"`` | ``"url"``
    - ``search_query`` / ``search`` / ``query``
    - ``product_url`` / ``url`` / ``pdp_url``
    - ``product_id`` / ``productId`` / ``article_id``
    - ``name_hint`` / ``product_name`` / ``display_name``
    - ``keyword_groups``: list of OR-groups, e.g. ``[["etb"], ["chaos"]]``
    - ``exclude`` / ``exclude_substrings``: list of strings
    - ``price_min`` / ``price_min_eur``, ``price_max`` / ``price_max_eur``
    - ``min_match_score`` (float)
    """
    mode = str(raw.get("mode") or "search").lower()
    if mode not in ("search", "url"):
        mode = "search"

    sq = raw.get("search_query") or raw.get("search") or raw.get("query") or ""
    purl = raw.get("product_url") or raw.get("url") or raw.get("pdp_url") or ""

    pid = raw.get("product_id") or raw.get("productId") or raw.get("article_id")
    pid_s = str(pid).strip() if pid is not None and str(pid).strip() else None

    name = raw.get("name_hint") or raw.get("product_name") or raw.get("display_name") or ""
    kws = raw.get("keyword_groups")
    if kws is None:
        kws = raw.get("keywords")
    groups: list[list[str]] = []
    if isinstance(kws, list):
        for g in kws:
            if isinstance(g, str):
                groups.append([g])
            elif isinstance(g, list):
                groups.append([str(x) for x in g])

    ex = raw.get("exclude_substrings") or raw.get("exclude") or []
    exclude = [str(x) for x in ex] if isinstance(ex, list) else []

    pmin = raw.get("price_min_eur", raw.get("price_min"))
    pmax = raw.get("price_max_eur", raw.get("price_max"))
    lo = float(pmin) if pmin is not None and str(pmin) != "" else None
    hi = float(pmax) if pmax is not None and str(pmax) != "" else None

    score = raw.get("min_match_score", 0.25)
    try:
        min_score = float(score)
    except (TypeError, ValueError):
        min_score = 0.25

    return FnacWatchConfig(
        mode=mode,  # type: ignore[arg-type]
        search_query=str(sq),
        product_url=str(purl),
        product_id=pid_s,
        name_hint=str(name),
        keyword_groups=groups,
        exclude_substrings=exclude,
        min_match_score=min_score,
        price_min_eur=lo,
        price_max_eur=hi,
    )


def is_fnac_job(raw: dict[str, Any]) -> bool:
    s = str(raw.get("site") or raw.get("retailer") or "").lower()
    return s == "fnac"
