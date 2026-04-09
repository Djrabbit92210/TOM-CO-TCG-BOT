"""One-off: pull fnac HTML/JS and print candidate API paths (run manually)."""

from __future__ import annotations

import re
import sys
import urllib.request
from urllib.parse import urljoin, urlparse

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def fetch(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Accept-Language": "fr-FR,fr;q=0.9",
            "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
        },
    )
    with urllib.request.urlopen(req, timeout=45) as r:
        return r.read().decode("utf-8", errors="replace")


def paths_in_text(text: str) -> set[str]:
    # common patterns in minified JS
    patterns = [
        r'"/basket/[a-zA-Z0-9/_-]+"',
        r"'/basket/[a-zA-Z0-9/_-]+'",
        r'"/api/[a-zA-Z0-9/_-]+"',
        r"'/api/[a-zA-Z0-9/_-]+'",
        r'"/cart/[a-zA-Z0-9/_-]+"',
        r"'/cart/[a-zA-Z0-9/_-]+'",
        r'"/checkout/[a-zA-Z0-9/_-]+"',
        r"'/checkout/[a-zA-Z0-9/_-]+'",
        r'"/ws/[a-zA-Z0-9/_-]+"',
        r"'/ws/[a-zA-Z0-9/_-]+'",
    ]
    out: set[str] = set()
    for pat in patterns:
        for m in re.findall(pat, text):
            out.add(m.strip("'\""))
    return out


def main() -> int:
    base = "https://www.fnac.com"
    html = fetch(base)
    srcs = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', html, re.I)
    print("homepage scripts:", len(srcs))
    all_paths: set[str] = set()
    all_paths |= paths_in_text(html)

    for src in srcs:
        if not src or src.startswith("data:"):
            continue
        js_url = urljoin(base + "/", src)
        if urlparse(js_url).netloc and "fnac" not in js_url:
            continue
        try:
            js = fetch(js_url)
        except Exception as e:
            print("skip", js_url[:80], e, file=sys.stderr)
            continue
        found = paths_in_text(js)
        if found:
            print("from", js_url[:100], "->", sorted(found)[:20])
        all_paths |= found

    print("\n--- merged basket/cart/checkout/api paths ---")
    for p in sorted(all_paths):
        if any(x in p for x in ("basket", "cart", "checkout", "/api/")):
            print(p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
