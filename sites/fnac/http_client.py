from __future__ import annotations
import json
from dataclasses import dataclass
from http.cookiejar import Cookie
from typing import Any
import httpx
from accounts.cookie_store import CookieStore
from sites.fnac import config, endpoints

def _apply_playwright_cookies(client: httpx.Client, rows: list[dict]) -> None:
    for c in rows:
        name, value = c.get("name"), c.get("value")
        if not name or value is None: continue
        client.cookies.set(name, value, domain=(c.get("domain") or "").lstrip("."), path=c.get("path") or "/")

@dataclass
class ApiResult:
    ok: bool
    status_code: int
    body: Any
    text: str
    final_url: str | None = None

class FnacHttpClient:
    def __init__(self, *, cookie_store: CookieStore | None = None, user_agent: str | None = None, timeout: float = 60.0) -> None:
        self.cookie_store, self.user_agent, self.timeout = cookie_store, user_agent or config.DEFAULT_USER_AGENT, timeout
        self._client: httpx.Client | None = None

    def _base_headers(self, *, referer: str | None = None) -> dict[str, str]:
        h = {
            "User-Agent": self.user_agent,
            "Accept": "application/json, text/plain, */*",
            "X-Requested-With": "XMLHttpRequest", # Indispensable pour l'API
            "Origin": "https://www.fnac.com",
            "Accept-Language": "fr-FR,fr;q=0.9"
        }
        if referer: h["Referer"] = referer
        return h

    def __enter__(self) -> FnacHttpClient:
        self._client = httpx.Client(follow_redirects=True, timeout=self.timeout, headers=self._base_headers())
        if self.cookie_store:
            loaded = self.cookie_store.load(config.COOKIE_LABEL)
            if loaded: _apply_playwright_cookies(self._client, loaded)
        return self

    def __exit__(self, *args: object) -> None:
        if self._client: self._client.close()

    def add_to_cart(self, payload: list[dict[str, Any]], *, referer: str) -> ApiResult:
        r = self._client.post(endpoints.url(endpoints.BASKET_ADD), content=json.dumps(payload), headers=self._base_headers(referer=referer))
        try: body = r.json()
        except: body = r.text
        return ApiResult(ok=r.is_success, status_code=r.status_code, body=body, text=r.text)
    
    def warm_session(self, *, referer_path: str) -> ApiResult:
        path = referer_path if referer_path.startswith("/") else f"/{referer_path}"
        r = self._client.get(f"https://www.fnac.com{path}", headers=self._base_headers())
        return ApiResult(ok=r.is_success, status_code=r.status_code, body=None, text=r.text[:500], final_url=str(r.url))