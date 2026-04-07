"""Load and analyze Playwright capture JSON (data/fnac_api_capture.json)."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse


def load_capture_file(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    raw = json.loads(path.read_text(encoding="utf-8"))
    return raw if isinstance(raw, list) else []


def analyze_capture(rows: list[dict]) -> dict:
    """Group by host, path prefix, method; list unique URLs."""
    by_host: dict[str, list[str]] = defaultdict(list)
    methods: Counter[str] = Counter()
    statuses: Counter[str] = Counter()
    json_like: list[dict] = []
    posts: list[dict] = []

    for row in rows:
        url = str(row.get("url") or "")
        method = str(row.get("method") or "?")
        methods[method] += 1
        st = row.get("status")
        if st is not None:
            statuses[str(st)] += 1
        ct = str(row.get("contentType") or "")
        if any(x in url for x in ("/basket", "/api/", "/graphql", "/checkout")) and (
            "json" in ct.lower() or method.upper() == "POST"
        ):
            json_like.append(
                {
                    "method": method,
                    "url": url,
                    "status": st,
                    "contentType": ct or None,
                }
            )
        p = urlparse(url)
        host = p.netloc or "?"
        path = p.path or "/"
        by_host[host].append(f"{method} {path}")
        pd = row.get("postData")
        if method.upper() == "POST" and pd:
            posts.append({"url": url, "post_preview": str(pd)[:500]})

    # unique ordered URLs
    seen: set[str] = set()
    unique_urls: list[str] = []
    for row in rows:
        u = str(row.get("url") or "")
        if u and u not in seen:
            seen.add(u)
            unique_urls.append(u)

    return {
        "total_rows": len(rows),
        "unique_urls": len(unique_urls),
        "methods": dict(methods),
        "statuses": dict(statuses),
        "by_host_paths": {h: sorted(set(paths)) for h, paths in by_host.items()},
        "unique_urls_list": unique_urls,
        "post_samples": posts[:20],
        "likely_structured_endpoints": json_like[:50],
    }


def write_sidecar_report(capture_path: Path, rows: list[dict]) -> Path:
    """Write ``fnac_api_capture.report.json`` next to capture file."""
    report_path = capture_path.with_suffix(".report.json")
    report = analyze_capture(rows)
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report_path
