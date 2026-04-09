"""Playwright: Akamai-friendly session, visual add-to-cart, persistent session support."""

from __future__ import annotations

import json
import time
import random
from collections import OrderedDict
from pathlib import Path
from typing import Any

from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from accounts.cookie_store import CookieStore
from sites.fnac import config
from infra.proxy_manager import ProxyManager

_LAUNCH_ARGS = [
    "--disable-blink-features=AutomationControlled",
    "--no-sandbox",
    "--disable-setuid-sandbox",
    "--disable-infobars",
    "--window-size=1920,1080",
    "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
]

AKAMAI_MARKERS = ("akam/", "Please enable JS", "id=\"cmsg\"", "bazadebezolkohpepadr", "Access Denied", "incident ID")


def is_akamai_challenge(html: str) -> bool:
    if not html:
        return True
    h = html[:10000].lower()
    return any(m.lower() in h for m in AKAMAI_MARKERS)


def _accept_cookies(page: Page) -> None:
    btn = page.locator("button#onetrust-accept-btn-handler")
    if btn.count() > 0:
        try:
            btn.click(timeout=5000)
            time.sleep(0.5)
        except Exception:
            pass


def _new_context(browser: Browser, user_agent: str | None = None) -> BrowserContext:
    ua = user_agent or "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    ctx = browser.new_context(
        user_agent=ua,
        locale="fr-FR",
        timezone_id="Europe/Paris",
        viewport={"width": 1920, "height": 1080},
        ignore_https_errors=True,
    )
    ctx.set_extra_http_headers(
        {
            "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
            "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"macOS"',
            "Upgrade-Insecure-Requests": "1",
        }
    )
    return ctx


def _clean_cookies(cookies: list[dict]) -> list[dict]:
    clean = []
    # On garde TOUT pour Akamai si on est dans une session active
    return cookies


def _load_cookies(ctx: BrowserContext, store: CookieStore | None) -> None:
    if not store:
        return
    raw = store.load(config.COOKIE_LABEL)
    if raw:
        ctx.add_cookies(raw) # On charge tout


def _save_cookies(ctx: BrowserContext, store: CookieStore | None) -> None:
    if store:
        store.save(config.COOKIE_LABEL, ctx.cookies())


def _handle_queue(page: Page, timeout_ms: int = 120_000) -> None:
    if "queue.fnac.com" in page.url:
        print(f"DEBUG: [Browser] Entering Fnac Waiting Room (Queue-it)...")
        try:
            page.wait_for_url("**/fnac.com/**", timeout=timeout_ms, wait_until="domcontentloaded")
            print("DEBUG: [Browser] Queue-it cleared!")
        except Exception:
            print("DEBUG: [Browser] Queue-it wait timed out.")


def _simulate_human(page: Page) -> None:
    """Add mouse noise and random scroll to evade Akamai bot detection."""
    try:
        # Mouse jitter
        for _ in range(random.randint(1, 3)):
            x, y = random.randint(100, 800), random.randint(100, 600)
            page.mouse.move(x, y, steps=random.randint(5, 15))
        
        # Subtle scroll
        if random.random() > 0.5:
            scroll_amt = random.randint(50, 200)
            page.mouse.wheel(0, scroll_amt)
            time.sleep(0.2)
            page.mouse.wheel(0, -scroll_amt)
    except:
        pass


def warm_page(page: Page, referer_path: str, *, timeout_ms: int = 90_000) -> str:
    path = referer_path if referer_path.startswith("/") else f"/{referer_path}"
    target_url = f"{config.BASE_URL}{path}"
    
    if config.BASE_URL not in page.url:
        page.goto(config.BASE_URL, timeout=timeout_ms, wait_until="domcontentloaded")
        _handle_queue(page)
        _accept_cookies(page)
    
    if path not in page.url:
        page.goto(target_url, timeout=timeout_ms, wait_until="domcontentloaded")
        _handle_queue(page)
    
    time.sleep(0.2)
    return page.url


def add_to_cart_playwright(
    product_id: str,
    payload: list[dict[str, Any]],
    *,
    referer_path: str,
    cookie_store: CookieStore | None,
    user_agent: str,
    headless: bool,
    proxy_manager: ProxyManager | None = None,
    page: Page | None = None,
) -> tuple[bool, int, Any, str]:
    """Perform visual 'Add to Cart' click (supports persistent page)."""
    if page:
        try:
            print(f"DEBUG: [Browser] [Turbo] Adding {product_id} to cart...")
            _simulate_human(page)
            # On s'assure d'être sur la page
            warm_page(page, referer_path)
            
            product_link_pattern = f"/a{product_id}/"
            card = page.locator(f".f-productCard, .Article-item").filter(has=page.locator(f'a[href*="{product_link_pattern}"]')).first
            
            if card.count() == 0:
                # On tente un petit scroll car le produit peut être "lazy loaded"
                page.evaluate("window.scrollBy(0, 500)")
                time.sleep(0.5)
                if card.count() == 0:
                    return False, 0, None, "card_not_found"

            btn = card.locator('button:has-text("Ajouter au panier"), .js-addToCart').first
            btn.click()
            time.sleep(1.0)
            return True, 200, {"success": True}, "visual_click_ok"
        except Exception as e:
            return False, 0, None, str(e)

    proxy_conf = proxy_manager.get_playwright_proxy() if proxy_manager else None
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless, args=_LAUNCH_ARGS, proxy=proxy_conf)
        ctx = _new_context(browser, user_agent)
        _load_cookies(ctx, cookie_store)
        page_local = ctx.new_page()
        try:
            res = add_to_cart_playwright(product_id, payload, referer_path=referer_path, 
                                       cookie_store=cookie_store, user_agent=user_agent, 
                                       headless=headless, page=page_local)
            _save_cookies(ctx, cookie_store)
            return res
        finally:
            page_local.close()
            ctx.close()
            browser.close()


def fetch_html_playwright(
    target: str,
    *,
    cookie_store: CookieStore | None,
    user_agent: str,
    headless: bool = False,
    warm_path: str | None = None,
    proxy_manager: ProxyManager | None = None,
    page: Page | None = None,
) -> tuple[str, str]:
    """Load URL HTML (supports persistent page with smart reload)."""
    if page:
        url = target if target.startswith("http") else f"{config.BASE_URL}{target}"
        
        _simulate_human(page)
        
        # Smart Refresh: Si on est déjà sur l'URL, on utilise reload() ce qui est plus naturel
        if url in page.url or page.url in url:
            print(f"DEBUG: [Browser] [Stealth] Reloading current page...")
            page.reload(wait_until="domcontentloaded")
        else:
            print(f"DEBUG: [Browser] [Stealth] Navigating to {url}...")
            page.goto(url, wait_until="domcontentloaded")
            
        _handle_queue(page)
        return page.content(), page.url

    proxy_conf = proxy_manager.get_playwright_proxy() if proxy_manager else None
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless, args=_LAUNCH_ARGS, proxy=proxy_conf)
        ctx = _new_context(browser, user_agent)
        _load_cookies(ctx, cookie_store)
        page_local = ctx.new_page()
        try:
            if warm_path: warm_page(page_local, warm_path)
            html, final = fetch_html_playwright(target, cookie_store=cookie_store, user_agent=user_agent, page=page_local)
            _save_cookies(ctx, cookie_store)
            return html, final
        finally:
            page_local.close()
            ctx.close()
            browser.close()


def checkout_sequence_playwright(
    *,
    cookie_store: CookieStore | None,
    user_agent: str,
    headless: bool = False,
    proxy_manager: ProxyManager | None = None,
    page: Page | None = None,
) -> bool:
    """Full browser flow from /basket to Payment (supports persistent page)."""
    if page:
        return _checkout_steps(page)

    proxy_conf = proxy_manager.get_playwright_proxy() if proxy_manager else None
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless, args=_LAUNCH_ARGS, proxy=proxy_conf)
        ctx = _new_context(browser, user_agent)
        _load_cookies(ctx, cookie_store)
        page_local = ctx.new_page()
        try:
            res = _checkout_steps(page_local)
            _save_cookies(ctx, cookie_store)
            return res
        finally:
            page_local.close()
            ctx.close()
            browser.close()


def _checkout_steps(page: Page) -> bool:
    """Internal checkout navigation logic."""
    try:
        Path("scratch").mkdir(exist_ok=True)
        basket_urls = [f"{config.BASE_URL}/basket", f"{config.BASE_URL}/panier", "https://secure.fnac.com/orderpipe/pop/panier"]
        
        success = False
        for b_url in basket_urls:
            print(f"DEBUG: [Browser] Trying basket URL: {b_url}...")
            try:
                resp = page.goto(b_url, timeout=30_000, wait_until="domcontentloaded")
                _handle_queue(page)
                if resp and resp.status == 404: continue
                if "panier" in page.url.lower() or "basket" in page.url.lower():
                    success = True
                    break
            except: continue

        if not success:
            page.goto(config.BASE_URL, wait_until="domcontentloaded")
            cart_icon = page.locator('a[href*="panier"], .header-cart').first
            if cart_icon.count() > 0:
                cart_icon.click()
                page.wait_for_load_state("domcontentloaded")
            else: return False

        time.sleep(1.0)
        selectors = ['button:has-text("Choisir ma livraison")', 'button:has-text("Commander")', 'button:has-text("Valider mon panier")', '.btn--primary']
        
        checkout_btn = None
        for sel in selectors:
            try:
                loc = page.wait_for_selector(sel, timeout=3000, state="visible")
                if loc:
                    checkout_btn = page.locator(sel).first
                    break
            except: continue
        
        if not checkout_btn:
            page.screenshot(path="scratch/checkout_error.png")
            return False

        print(f"DEBUG: [Browser] Clicking Checkout button...")
        checkout_btn.click()
        page.wait_for_load_state("networkidle")

        if "connection" in page.url or "identification" in page.url:
            print("DEBUG: Login required.")
            return False

        print("DEBUG: Handling Shipping step...")
        shipping_btn = page.locator('button:has-text("Valider la livraison"), button:has-text("Passer au paiement"), button:has-text("Suivant")').first
        if shipping_btn.count() > 0:
            shipping_btn.click()
            page.wait_for_load_state("networkidle")

        print("DEBUG: Reached Payment step.")
        page.wait_for_selector('text="Paiement", text="Carte bancaire"', timeout=10_000)
        return True
    except Exception as e:
        print(f"DEBUG: Checkout failed: {e}")
        return False


def run_endpoint_capture(
    *,
    cookie_store: CookieStore | None,
    output_path: Path,
    user_agent: str,
    headless: bool,
    referer_path: str,
    extra_goto_url: str | None,
    auto_click_add_to_cart: bool,
    duration_seconds: float,
    settle_seconds: float,
    proxy_manager: ProxyManager | None = None,
) -> list[dict[str, Any]]:
    """Log XHR/fetch for reverse engineering (stays standalone for isolation)."""
    rows: "OrderedDict[str, dict[str, Any]]" = OrderedDict()

    def on_request(request) -> None:
        u = request.url
        if "fnac.com" not in u: return
        k = f"{request.method}\t{u}"
        if k in rows: return
        rows[k] = {"method": request.method, "url": u, "resourceType": request.resource_type, "postData": request.post_data}

    def on_response(response) -> None:
        req = response.request
        k = f"{req.method}\t{req.url}"
        if k in rows: rows[k]["status"] = response.status

    output_path.parent.mkdir(parents=True, exist_ok=True)
    proxy_conf = proxy_manager.get_playwright_proxy() if proxy_manager else None

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless, args=_LAUNCH_ARGS, proxy=proxy_conf)
        ctx = _new_context(browser, user_agent)
        _load_cookies(ctx, cookie_store)
        page = ctx.new_page()
        page.on("request", on_request)
        page.on("response", on_response)
        try:
            warm_page(page, referer_path)
            if extra_goto_url:
                page.goto(extra_goto_url if extra_goto_url.startswith("http") else config.BASE_URL + extra_goto_url, wait_until="domcontentloaded")
            if auto_click_add_to_cart:
                btn = page.locator("button:has-text('Ajouter au panier')").first
                if btn.count() > 0:
                    btn.click()
                    time.sleep(2.0)
            time.sleep(duration_seconds + settle_seconds)
            _save_cookies(ctx, cookie_store)
        finally:
            page.close()
            ctx.close()
            browser.close()

    out_list = list(rows.values())
    output_path.write_text(json.dumps(out_list, indent=2, ensure_ascii=False))
    return out_list
