"""Fnac purchase path: httpx first; Playwright when Akamai blocks raw HTTP."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from accounts.cookie_store import CookieStore
from sites.fnac import config
from sites.fnac.http_client import ApiResult, FnacHttpClient
from sites.fnac.playwright_fnac import add_to_cart_playwright, is_akamai_challenge, checkout_sequence_playwright
from sites.fnac.product_id import extract_product_id_from_url
from infra.proxy_manager import ProxyManager

# Import Page for type hinting
from playwright.sync_api import Page


@dataclass
class AddToCartResult:
    ok: bool
    http_status: int
    body: Any
    raw_text: str

    @classmethod
    def from_api(cls, r: ApiResult) -> AddToCartResult:
        return cls(ok=r.ok, http_status=r.status_code, body=r.body, raw_text=r.text)


class FnacBuyer:
    """Cookie-backed flow: httpx, then Playwright if Akamai challenge HTML."""

    def __init__(
        self,
        *,
        cookie_store: CookieStore | None = None,
        user_agent: str | None = None,
        headless: bool = False,
        transport: Literal["auto", "httpx", "playwright"] = "auto",
        proxy_manager: ProxyManager | None = None,
    ) -> None:
        self.cookie_store = cookie_store
        self.user_agent = user_agent or config.DEFAULT_USER_AGENT
        self.headless = headless
        self.transport = transport
        self.proxy_manager = proxy_manager

    def build_payload(
        self,
        product_id: str,
        *,
        quantity: int = 1,
        referential: str | None = None,
        offer: str | None = None,
        shop_id: None | str = None,
        master_product_id: None | str = None,
    ) -> list[dict[str, Any]]:
        return [
            {
                "productID": product_id,
                "referential": referential or config.REFERENTIAL_FR,
                "quantity": quantity,
                "offer": offer or config.DEFAULT_OFFER,
                "shopID": shop_id,
                "masterProductID": master_product_id,
            }
        ]

    def add_to_cart(
        self,
        product_id: str,
        *,
        quantity: int = 1,
        referer_path: str = "/SearchResult/ResultList.aspx?Search=pokemon&sft=1&sa=0",
        page: Page | None = None,
    ) -> AddToCartResult:
        payload = self.build_payload(product_id, quantity=quantity)

        if page or self.transport == "playwright":
            ok, st, body, raw = add_to_cart_playwright(
                product_id,
                payload,
                referer_path=referer_path,
                cookie_store=self.cookie_store,
                user_agent=self.user_agent,
                headless=self.headless,
                proxy_manager=self.proxy_manager,
                page=page,
            )
            return AddToCartResult(ok=ok, http_status=st, body=body, raw_text=raw)

        if self.transport == "httpx":
            return self._add_via_httpx(payload, referer_path)

        r = self._add_via_httpx(payload, referer_path)
        if r.ok and not is_akamai_challenge(r.raw_text):
            return r
            
        ok, st, body, raw = add_to_cart_playwright(
            product_id,
            payload,
            referer_path=referer_path,
            cookie_store=self.cookie_store,
            user_agent=self.user_agent,
            headless=self.headless,
            proxy_manager=self.proxy_manager,
            page=page,
        )
        return AddToCartResult(ok=ok, http_status=st, body=body, raw_text=raw)

    def _add_via_httpx(
        self,
        payload: list[dict[str, Any]],
        referer_path: str,
    ) -> AddToCartResult:
        with FnacHttpClient(
            cookie_store=self.cookie_store,
            user_agent=self.user_agent,
            proxy_manager=self.proxy_manager,
        ) as http:
            warm = http.warm_session(referer_path=referer_path)
            if not warm.ok:
                return AddToCartResult(
                    ok=False,
                    http_status=warm.status_code,
                    body=None,
                    raw_text=warm.text,
                )
            referer = warm.final_url or (
                f"https://www.fnac.com"
                f"{referer_path if referer_path.startswith('/') else '/' + referer_path}"
            )
            r = http.add_to_cart(payload, referer=referer)
            return AddToCartResult.from_api(r)

    def checkout(self, page: Page | None = None) -> bool:
        """Execute the checkout sequence via Playwright."""
        return checkout_sequence_playwright(
            cookie_store=self.cookie_store,
            user_agent=self.user_agent,
            headless=self.headless,
            proxy_manager=self.proxy_manager,
            page=page,
        )

    def buy(self, product: dict[str, Any], account: Any, payment: Any, page: Page | None = None) -> bool:
        pid = product.get("product_id")
        if not pid:
            return False
        ref = product.get("fnac_referer_path")
        kwargs: dict[str, Any] = {}
        if isinstance(ref, str) and ref.startswith("/"):
            kwargs["referer_path"] = ref
        
        # 1. Ajouter au panier
        print(f"DEBUG: Buying product {pid}...")
        r = self.add_to_cart(str(pid), page=page, **kwargs)
        if not r.ok:
            print(f"DEBUG: Add to cart failed: {r.http_status}")
            return False
            
        # 2. Finaliser la commande (Checkout)
        print("DEBUG: Proceeding to Checkout...")
        return self.checkout(page=page)


class FnacSite:
    """SiteAdapter-shaped entry for the orchestrator."""

    site_id = config.SITE_ID
    supports_api = config.SUPPORTS_API

    def __init__(self, buyer: FnacBuyer | None = None) -> None:
        self._buyer = buyer or FnacBuyer()

    def search_products(self, query: str) -> list[dict[str, Any]]:
        q = query.replace(" ", "+")
        return [
            {
                "title": query,
                "url": f"{config.BASE_URL}/SearchResult/ResultList.aspx?Search={q}&sft=1&sa=0",
                "product_id": None,
            }
        ]

    def get_product(self, url: str) -> dict[str, Any]:
        pid = extract_product_id_from_url(url)
        return {"url": url, "product_id": pid, "title": None}

    def buy(self, product: dict[str, Any], account: Any, payment: Any) -> bool:
        # Note: In a real Orchestrator call, we might not have 'page' yet.
        # But our Worker will bypass FnacSite.buy and call FnacMonitor.purchase_from_snapshot.
        return self._buyer.buy(product, account, payment)
