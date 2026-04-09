"""Poll Fnac (search or PDP) until in stock + price band, then add to cart."""

from __future__ import annotations

import time
import random
import logging
from dataclasses import dataclass
from typing import Callable, Any

from accounts.cookie_store import CookieStore
from sites.fnac import config
from sites.fnac.buyer import AddToCartResult, FnacBuyer
from sites.fnac.http_client import FnacHttpClient
from sites.fnac.match import pick_best_listing
from sites.fnac.playwright_fnac import fetch_html_playwright, is_akamai_challenge
from sites.fnac.models import FnacWatchConfig
from sites.fnac.product_id import resolve_product_id
from sites.fnac.scrape import listing_to_dict, parse_product_page, parse_search_results

# Import for persistent page support
from infra.browser_manager import BrowserManager

logger = logging.getLogger(__name__)

@dataclass
class WatchSnapshot:
    """Outcome of a single poll (no purchase)."""

    ready_to_buy: bool
    reason: str
    product_id: str | None
    price_eur: float | None
    add_to_cart_hint: bool
    matched_title: str | None
    product_url: str | None
    referer_path: str


def _price_in_band(
    price: float | None,
    lo: float | None,
    hi: float | None,
) -> bool:
    if price is None:
        return False
    if lo is not None and price < lo:
        return False
    if hi is not None and price > hi:
        return False
    return True


class FnacMonitor:
    """
    Stable bot loop driver: reads ``FnacWatchConfig`` (from the interface),
    fetches HTML via httpx, matches listings, checks price/stock hints.
    """

    def __init__(
        self,
        watch: FnacWatchConfig,
        *,
        cookie_store: CookieStore | None = None,
        buyer: FnacBuyer | None = None,
        browser_manager: BrowserManager | None = None,
    ) -> None:
        self.watch = watch
        self.buyer = buyer or FnacBuyer(cookie_store=cookie_store)
        self.browser_manager = browser_manager
        self._persistent_page = None
        if not self.browser_manager:
            logger.warning("[FnacMonitor] Warning: No BrowserManager provided. Falling back to HTTP.")
        else:
            logger.info("[FnacMonitor] BrowserManager received. Ghost Mode enabled.")

    def _get_page(self) -> Any:
        if not self.browser_manager:
            return None
        if not self._persistent_page:
            self.browser_manager.start()
            self.browser_manager.get_context(
                user_agent=self.buyer.user_agent,
                cookies=self.buyer.cookie_store.load(config.COOKIE_LABEL) if self.buyer.cookie_store else None
            )
            self._persistent_page = self.browser_manager.get_page()
        return self._persistent_page

    def _html_via_http_or_playwright(
        self,
        http: FnacHttpClient,
        full_url: str,
        *,
        referer: str,
        warm_path: str | None,
    ) -> tuple[str | None, str]:
        # STEALTH: Si on a le navigateur persistant, on SKIP httpx car c'est un signal suspect
        if self.browser_manager:
            try:
                html, _ = fetch_html_playwright(
                    full_url,
                    cookie_store=self.buyer.cookie_store,
                    user_agent=self.buyer.user_agent,
                    headless=self.buyer.headless,
                    warm_path=warm_path,
                    proxy_manager=self.buyer.proxy_manager,
                    page=self._get_page(),
                )
                if is_akamai_challenge(html):
                    return html, "akamai_after_playwright"
                return html, ""
            except Exception as exc:
                return None, f"playwright_fetch:{exc}"

        # Fallback classique si pas de manager (capture mode etc)
        r = http.get_page(full_url, referer=referer)
        if r.ok and not is_akamai_challenge(r.text):
            return r.text, ""
        try:
            html, _ = fetch_html_playwright(
                full_url,
                cookie_store=self.buyer.cookie_store,
                user_agent=self.buyer.user_agent,
                headless=self.buyer.headless,
                warm_path=warm_path,
                proxy_manager=self.buyer.proxy_manager,
            )
            if is_akamai_challenge(html):
                return html, "akamai_after_playwright"
            return html, ""
        except Exception as exc:
            return None, f"playwright_fetch:{exc}"

    def poll_once(self) -> WatchSnapshot:
        w = self.watch
        with FnacHttpClient(cookie_store=self.buyer.cookie_store, user_agent=self.buyer.user_agent) as http:
            if w.mode == "url":
                return self._poll_url(http, w)
            return self._poll_search(http, w)

    def _poll_url(self, http: FnacHttpClient, w: FnacWatchConfig) -> WatchSnapshot:
        url = w.product_url.strip()
        if not url:
            return WatchSnapshot(False, "missing_product_url", None, None, False, None, None, "/")
        
        ref_path = w.product_referer_path()
        html, err = self._html_via_http_or_playwright(
            http,
            url,
            referer=f"{config.BASE_URL}/",
            warm_path=ref_path,
        )
        if html is None:
            logger.error(f"[FnacMonitor] URL Poll failed: {err}")
            return WatchSnapshot(False, err or "fetch_failed", w.product_id, None, False, None, url, ref_path)
            
        if err == "akamai_after_playwright":
            logger.warning("[FnacMonitor] Akamai challenge detected on PDP page.")
            return WatchSnapshot(False, "akamai_block", w.product_id, None, False, None, url, ref_path)
            
        pid = resolve_product_id(url=url, html=html, explicit=w.product_id)
        _, price, purch = parse_product_page(html, url)
        in_band = _price_in_band(price, w.price_min_eur, w.price_max_eur)
        ready = bool(pid and purch and in_band)
        reason = "ok" if ready else self._explain_url(pid, purch, in_band, price)
        return WatchSnapshot(ready, reason, pid, price, purch, None, url, ref_path)

    def _poll_search(self, http: FnacHttpClient, w: FnacWatchConfig) -> WatchSnapshot:
        path = w.search_referer_path()
        
        # STEALTH: Si persistant, on bypass le premier jet httpx
        if self.browser_manager:
            html, err = self._html_via_http_or_playwright(
                http,
                f"{config.BASE_URL}{path if path.startswith('/') else '/' + path}",
                referer=f"{config.BASE_URL}/",
                warm_path=path,
            )
        else:
            ok, status, html, _final = http.get_storefront_html(path)
            if not ok or is_akamai_challenge(html):
                html, err = self._html_via_http_or_playwright(
                    http,
                    f"{config.BASE_URL}{path if path.startswith('/') else '/' + path}",
                    referer=f"{config.BASE_URL}/",
                    warm_path=path,
                )
            else:
                err = ""

        if html is None:
            logger.error(f"[FnacMonitor] Search Poll failed: {err}")
            return WatchSnapshot(False, "fetch_failed", w.product_id, None, False, None, None, path)
        if err == "akamai_after_playwright":
            logger.warning("[FnacMonitor] Akamai challenge detected on Search page.")
            return WatchSnapshot(False, "akamai_block", w.product_id, None, False, None, None, path)

        listings = [listing_to_dict(x) for x in parse_search_results(html)]
        
        best: dict | None = None
        if w.product_id:
            same = [L for L in listings if str(L.get("product_id")) == str(w.product_id)]
            if same:
                best = same[0]
        if best is None:
            groups = w.keyword_groups if w.keyword_groups else None
            best, _ = pick_best_listing(
                listings,
                name_hint=w.name_hint,
                keyword_groups=groups,
                exclude_substrings=w.exclude_substrings or None,
                min_score=w.min_match_score,
            )
        if not best:
            return WatchSnapshot(False, "no_listing_match", w.product_id, None, False, None, None, path)

        title = best.get("title") or ""
        pid = resolve_product_id(url=best.get("url"), html=None, explicit=w.product_id) or (str(best["product_id"]) if best.get("product_id") else None)
        price = best.get("price_eur")
        add_hint = bool(best.get("add_to_cart_hint"))
        in_band = _price_in_band(price, w.price_min_eur, w.price_max_eur)

        # PDP Fetch if signal weak
        if pid and (price is None or not add_hint):
            purl = best.get("url") or ""
            if purl:
                phtml, perr = self._html_via_http_or_playwright(http, purl, referer=f"{config.BASE_URL}{path}", warm_path=path)
                if phtml and perr != "akamai_after_playwright":
                    pid2, price2, purch2 = parse_product_page(phtml, purl)
                    pid = pid or pid2
                    if price is None: price = price2
                    add_hint = add_hint or purch2

        ready = bool(pid and add_hint and in_band)
        reason = "ok" if ready else self._explain_search(pid, add_hint, in_band, price, title)
        return WatchSnapshot(ready, reason, pid, price, add_hint, title, best.get("url"), path)

    @staticmethod
    def _explain_url(pid: str | None, purch: bool, in_band: bool, price: float | None) -> str:
        if not pid: return "no_product_id"
        if not purch: return "not_purchasable"
        if not in_band: return f"price_out_of_band:{price}"
        return "unknown"

    @staticmethod
    def _explain_search(pid: str | None, add_hint: bool, in_band: bool, price: float | None, title: str) -> str:
        if not pid: return "no_product_id"
        if not add_hint: return "no_add_to_cart"
        if not in_band: return f"price_out_of_band:{price}"
        return "unknown"

    def purchase_from_snapshot(self, snap: WatchSnapshot) -> AddToCartResult | None:
        """Turbo purchase: navigate to PDP first to ensure session sync, then click."""
        if not snap.ready_to_buy or not snap.product_id:
            return None
            
        page = self._get_page()
        if page and snap.product_url:
            print(f"DEBUG: [Browser] Navigating to PDP before purchase: {snap.product_url}")
            page.goto(snap.product_url, wait_until="domcontentloaded")
            time.sleep(1.0) # Petite pause pour stabiliser la session

        print(f"LOG: [Turbo] Triggering purchase for {snap.product_id}...")
        orig_transport = self.buyer.transport
        self.buyer.transport = "playwright"
        try:
            r = self.buyer.add_to_cart(snap.product_id, referer_path=snap.referer_path, page=page)
        finally:
            self.buyer.transport = orig_transport

        if r.ok:
            print("LOG: [Turbo] AddToCart successful, starting checkout sequence...")
            self.buyer.checkout(page=page)
        return r

    def try_purchase(self) -> AddToCartResult | None:
        snap = self.poll_once()
        if not snap.ready_to_buy or not snap.product_id:
            return None
        r = self.buyer.add_to_cart(snap.product_id, referer_path=snap.referer_path, page=self._get_page())
        if r.ok:
            print("LOG: AddToCart successful, starting checkout sequence...")
            self.buyer.checkout(page=self._get_page())
        return r

    def run_loop(
        self,
        *,
        interval_sec: float = 30.0,
        max_iterations: int | None = None,
        on_tick: Callable[[WatchSnapshot], None] | None = None,
    ) -> AddToCartResult | None:
        """Poll until purchase succeeds or max_iterations reached (Manual intervention support)."""
        n = 0
        while True:
            n += 1
            if max_iterations is not None and n > max_iterations: return None
            
            snap = self.poll_once()
            if on_tick: on_tick(snap)
            
            if snap.reason == "akamai_block":
                print("WARNING: [Stealth] Akamai block detected! Waiting for manual solve...")
                time.sleep(30.0) # On attend plus longtemps pour laisser l'utilisateur agir
                continue

            if snap.ready_to_buy and snap.product_id:
                r = self.purchase_from_snapshot(snap)
                if r and r.ok:
                    print("LOG: [Stealth] MISSION ACCOMPLISHED. Payment page reached.")
                    print("LOG: [Stealth] Stopping bot to let user finalize payment manually. DO NOT RESTART.")
                    return r
                
            # Adaptive sleep (jitter)
            sleep_time = interval_sec + random.uniform(-interval_sec * 0.3, interval_sec * 0.5)
            time.sleep(max(5.0, sleep_time))
