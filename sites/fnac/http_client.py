"""httpx session against Fnac (cookie jar + JSON basket API)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from http.cookiejar import Cookie
from typing import Any

import httpx
from httpx_socks import SyncProxyTransport

from accounts.cookie_store import CookieStore
from sites.fnac import config, endpoints
from infra.proxy_manager import ProxyManager


def _apply_playwright_cookies(client: httpx.Client, rows: list[dict]) -> None:
    for c in rows:
        name = c.get("name")
        value = c.get("value")
        if not name or value is None:
            continue
        domain = (c.get("domain") or "").lstrip(".")
        path = c.get("path") or "/"
        client.cookies.set(name, value, domain=domain, path=path)


def _export_cookies_for_store(client: httpx.Client) -> list[dict]:
    out: list[dict] = []
    for c in client.cookies.jar:
        if not isinstance(c, Cookie):
            continue
        dom = c.domain or ""
        if dom and not dom.startswith("."):
            dom = "." + dom
        out.append(
            {
                "name": c.name,
                "value": c.value,
                "domain": dom or ".fnac.com",
                "path": c.path or "/",
                "expires": float(c.expires) if c.expires else -1,
                "httpOnly": bool(getattr(c, "_rest", {}).get("HttpOnly", False)),
                "secure": bool(c.secure),
                "sameSite": "Lax",
            }
        )
    return out


@dataclass
class ApiResult:
    ok: bool
    status_code: int
    body: Any
    text: str
    final_url: str | None = None


class FnacHttpClient:
    """Cookie-backed HTTP client; no browser required at runtime."""

    def __init__(
        self,
        *,
        cookie_store: CookieStore | None = None,
        user_agent: str | None = None,
        proxy_manager: ProxyManager | None = None,
        timeout: float = 60.0,
    ) -> None:
        self.cookie_store = cookie_store
        self.user_agent = user_agent or config.DEFAULT_USER_AGENT
        self.proxy_manager = proxy_manager
        self.timeout = timeout
        self._client: httpx.Client | None = None

    def _base_headers(self, *, referer: str | None = None) -> dict[str, str]:
        h = {
            "User-Agent": self.user_agent,
            "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept": "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8",
            "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"macOS"',
            "Upgrade-Insecure-Requests": "1",
        }
        if referer:
            h["Referer"] = referer
        return h

    def __enter__(self) -> FnacHttpClient:
        proxy_url = self.proxy_manager.get_proxy() if self.proxy_manager else None
        transport = SyncProxyTransport.from_url(proxy_url) if proxy_url else httpx.HTTPTransport()

        self._client = httpx.Client(
            follow_redirects=True,
            timeout=self.timeout,
            headers=self._base_headers(),
            transport=transport,
        )
        if self.cookie_store:
            loaded = self.cookie_store.load(config.COOKIE_LABEL)
            if loaded:
                _apply_playwright_cookies(self._client, loaded)
        return self

    def __exit__(self, *args: object) -> None:
        if self._client and self.cookie_store:
            self.cookie_store.save(config.COOKIE_LABEL, _export_cookies_for_store(self._client))
        if self._client:
            self._client.close()
        self._client = None

    @property
    def client(self) -> httpx.Client:
        if not self._client:
            raise RuntimeError("Use FnacHttpClient as context manager")
        return self._client

    def warm_session(self, *, referer_path: str) -> ApiResult:
        """GET home then a storefront page so cookies + Referer match a real visit."""
        c = self.client
        r1 = c.get(endpoints.url(endpoints.HOME), headers=self._base_headers())
        ref1 = str(r1.url)
        path = referer_path if referer_path.startswith("/") else f"/{referer_path}"
        r2 = c.get(
            f"https://www.fnac.com{path}",
            headers=self._base_headers(referer=ref1),
        )
        return ApiResult(
            ok=r2.is_success,
            status_code=r2.status_code,
            body=None,
            text=r2.text[:500],
            final_url=str(r2.url),
        )

    def get_storefront_html(self, path: str) -> tuple[bool, int, str, str]:
        """GET / then GET ``path`` (path includes leading / and optional ?query)."""
        c = self.client
        r1 = c.get(endpoints.url(endpoints.HOME), headers=self._base_headers())
        ref1 = str(r1.url)
        p = path if path.startswith("/") else f"/{path}"
        r2 = c.get(
            f"https://www.fnac.com{p}",
            headers=self._base_headers(referer=ref1),
        )
        return r2.is_success, r2.status_code, r2.text, str(r2.url)

    def get_page(self, url: str, *, referer: str | None = None) -> ApiResult:
        """Arbitrary GET (e.g. product PDP)."""
        r = self.client.get(
            url,
            headers=self._base_headers(referer=referer or f"{config.BASE_URL}/"),
        )
        return ApiResult(
            ok=r.is_success,
            status_code=r.status_code,
            body=None,
            text=r.text,
            final_url=str(r.url),
        )

    def add_to_cart(self, payload: list[dict[str, Any]], *, referer: str) -> ApiResult:
        url = endpoints.url(endpoints.BASKET_ADD)
        body = json.dumps(payload, separators=(",", ":"))
        r = self.client.post(
            url,
            content=body,
            headers={
                **self._base_headers(referer=referer),
                "Content-Type": "application/json",
                "Accept": "application/json, text/plain, */*",
                "Origin": "https://www.fnac.com",
            },
        )
        raw = r.text
        try:
            parsed: Any = r.json()
        except Exception:
            parsed = raw
        return ApiResult(ok=r.is_success, status_code=r.status_code, body=parsed, text=raw)

    def get_basket_page(self) -> ApiResult:
        """GET /basket (often HTML)."""
        r = self.client.get(
            endpoints.url(endpoints.BASKET_GET),
            headers=self._base_headers(referer="https://www.fnac.com/"),
        )
        return ApiResult(ok=r.is_success, status_code=r.status_code, body=None, text=r.text[:4000])

    def get_basket_json_candidates(self) -> dict[str, ApiResult]:
        """Try inferred JSON endpoints; use results to refine endpoints.py."""
        out: dict[str, ApiResult] = {}
        for name, ep in (
            ("summary", endpoints.BASKET_SUMMARY),
            ("lines", endpoints.BASKET_LINES),
        ):
            r = self.client.get(
                endpoints.url(ep),
                headers={
                    **self._base_headers(referer="https://www.fnac.com/"),
                    "Accept": "application/json, text/plain, */*",
                },
            )
            try:
                body: Any = r.json()
            except Exception:
                body = r.text[:1000]
            out[name] = ApiResult(ok=r.is_success, status_code=r.status_code, body=body, text=r.text[:500])
        return out
