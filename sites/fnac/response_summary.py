"""Turn Fnac HTTP bodies into short, log-friendly summaries."""

from __future__ import annotations

import json
import re
from typing import Any

from sites.fnac.playwright_fnac import is_akamai_challenge


def summarize_fnac_response(status: int, raw_text: str, *, body: Any = None) -> dict[str, Any]:
    """
    Classify response for CLI / logs.

    Fnac may return JSON for /basket/add or an HTML cart page (still HTTP 200).
    """
    raw = raw_text or ""
    out: dict[str, Any] = {"http_status": status, "length": len(raw)}

    if is_akamai_challenge(raw):
        out["kind"] = "akamai_challenge"
        return out

    if body is not None and isinstance(body, (dict, list)):
        out["kind"] = "json"
        out["data"] = body
        return out

    t = raw.strip()
    if t.startswith("{") or t.startswith("["):
        try:
            out["kind"] = "json"
            out["data"] = json.loads(t)
            return out
        except json.JSONDecodeError:
            pass

    low = raw[:8000].lower()
    if "<html" in low:
        title_m = re.search(r"<title[^>]*>([^<]{1,200})", raw, re.I)
        title = title_m.group(1).strip() if title_m else None
        tl = (title or "").lower()
        if title and "maintenance" in tl:
            out["kind"] = "maintenance_or_block"
            out["page_title"] = title
        elif title and "panier" in tl:
            out["kind"] = "html_cart_page"
            out["page_title"] = title
        else:
            out["kind"] = "html"
            out["page_title"] = title
        return out

    out["kind"] = "text"
    out["snippet"] = t[:400]
    return out


def format_cli_block(status: int, raw_text: str, *, body: Any = None, verbose: bool = False) -> str:
    summ = summarize_fnac_response(status, raw_text, body=body)
    lines = [json.dumps(summ, indent=2, ensure_ascii=False)]
    if verbose:
        lines.append("--- raw (truncated) ---")
        lines.append(raw_text[:25_000])
    return "\n".join(lines)
