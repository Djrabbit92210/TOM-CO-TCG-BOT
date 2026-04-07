"""Typed config for Fnac watch jobs (from UI / orchestrator)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal
from urllib.parse import quote_plus, urlparse


@dataclass
class FnacWatchConfig:
    """One monitoring target: search by keywords or watch a direct PDP URL."""

    mode: Literal["search", "url"]
    # Search mode
    search_query: str = ""
    # URL mode
    product_url: str = ""
    # Optional explicit id from interface (skips HTML/URL parsing when set)
    product_id: str | None = None
    # Matching (search mode) — name_hint + keyword_groups refine which row is ours
    name_hint: str = ""
    keyword_groups: list[list[str]] = field(default_factory=list)
    exclude_substrings: list[str] = field(default_factory=list)
    min_match_score: float = 0.25
    # Price band (EUR); None = no bound
    price_min_eur: float | None = None
    price_max_eur: float | None = None

    def search_referer_path(self) -> str:
        q = quote_plus(self.search_query.strip() or "pokemon")
        return f"/SearchResult/ResultList.aspx?Search={q}&sft=1&sa=0"

    def product_referer_path(self) -> str:
        p = urlparse(self.product_url.strip())
        out = p.path or "/"
        if p.query:
            out = f"{out}?{p.query}"
        return out if out.startswith("/") else f"/{out}"
