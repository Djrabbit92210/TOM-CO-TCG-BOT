from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Literal
from accounts.cookie_store import CookieStore
from sites.fnac import config
from sites.fnac.http_client import ApiResult, FnacHttpClient
from sites.fnac.playwright_fnac import add_to_cart_playwright, is_akamai_challenge
from accounts.fnac_session import farm_fnac_session

@dataclass
class AddToCartResult:
    ok: bool
    http_status: int
    body: Any
    raw_text: str

class FnacBuyer:
    def __init__(self, *, cookie_store: CookieStore | None = None, user_agent: str | None = None, headless: bool = True, transport: Literal["auto", "httpx", "playwright"] = "auto") -> None:
        self.cookie_store, self.user_agent, self.headless, self.transport = cookie_store, user_agent or config.DEFAULT_USER_AGENT, headless, transport

    def build_payload(self, product_id: str, quantity: int = 1) -> list[dict[str, Any]]:
        return [{"productID": product_id, "referential": config.REFERENTIAL_FR, "quantity": quantity, "offer": config.DEFAULT_OFFER}]

    def _add_via_httpx(self, payload: list[dict[str, Any]], referer_path: str) -> AddToCartResult:
        with FnacHttpClient(cookie_store=self.cookie_store, user_agent=self.user_agent) as http:
            warm = http.warm_session(referer_path=referer_path)
            r = http.add_to_cart(payload, referer=warm.final_url or "https://www.fnac.com/")
            return AddToCartResult(ok=r.ok, http_status=r.status_code, body=r.body, raw_text=r.text)

    def add_to_cart(self, product_id: str, **kwargs) -> AddToCartResult:
        payload = self.build_payload(product_id, quantity=kwargs.get("quantity", 1))
        referer = kwargs.get("referer_path", "/")
        
        # 1. Tentative ultra-rapide via l'API
        res = self._add_via_httpx(payload, referer)
        
        # 2. Si Akamai bloque (403), on lance le Key Farming pour voler de nouvelles clés
        if res.http_status == 403 or is_akamai_challenge(res.raw_text):
            print("Akamai détecté. Lancement automatique du Key Farming...")
            if farm_fnac_session(config.COOKIE_LABEL, self.cookie_store, self.user_agent):
                res = self._add_via_httpx(payload, referer)
        
        # 3. Repli de sécurité sur Playwright complet si l'API est toujours bloquée
        if not res.ok:
            ok, st, body, raw = add_to_cart_playwright(product_id, payload, referer_path=referer, cookie_store=self.cookie_store, user_agent=self.user_agent, headless=self.headless)
            return AddToCartResult(ok=ok, http_status=st, body=body, raw_text=raw)
        
        return res
    