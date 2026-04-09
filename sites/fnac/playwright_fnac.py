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
    try:
        ctx.set_extra_http_headers(
            {
                "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
                "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": '"macOS"',
                "Upgrade-Insecure-Requests": "1",
            }
        )
    except Exception:
        # En mode CDP, on ne peut pas toujours modifier les headers d'un contexte existant
        pass
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
            print(f"DEBUG: [Browser] Adding {product_id} to cart via physical click...")
            _simulate_human(page)
            
            # 1. On cherche d'abord les boutons spécifiques à une page PRODUIT (PDP)
            pdp_selectors = [
                'button.js-AddBasket',
                '.f-purchase-button button',
                'button:has-text("Ajouter au panier")',
                '.btn-primary:has-text("Ajouter au panier")'
            ]
            
            found_btn = False
            for sel in pdp_selectors:
                try:
                    btn = page.locator(sel).first
                    if btn.is_visible(timeout=3000):
                        print(f"DEBUG: [Browser] Found PDP Add button: {sel}")
                        btn.click()
                        found_btn = True
                        break
                except: continue
            
            # 2. Si pas trouvé, on cherche sur une page de RÉSULTATS (Search)
            if not found_btn:
                print("DEBUG: [Browser] PDP button not found, checking search results card...")
                product_link_pattern = f"/a{product_id}/"
                card = page.locator(f".f-productCard, .Article-item").filter(has=page.locator(f'a[href*="{product_link_pattern}"]')).first
                if card.count() > 0:
                    btn = card.locator('button:has-text("Ajouter au panier"), .js-addToCart').first
                    if btn.count() > 0:
                        btn.click()
                        found_btn = True
            
            if found_btn:
                # Petite attente pour que l'action soit enregistrée par la Fnac
                time.sleep(1.5)
                return True, 200, {"success": True}, "visual_click_ok"
            
            return False, 0, None, "add_button_not_found"
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
        
        # Smart Refresh: Comparaison plus stricte pour éviter de confondre l'accueil et la recherche
        current_url = page.url.rstrip('/')
        target_url = url.rstrip('/')
        
        if current_url == target_url:
            print(f"DEBUG: [Browser] [Stealth] Reloading current page...")
            try:
                page.reload(wait_until="domcontentloaded", timeout=60000)
            except Exception:
                page.goto(url, wait_until="domcontentloaded")
        else:
            print(f"DEBUG: [Browser] [Stealth] Navigating to {url} (current: {current_url})...")
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
    """Internal checkout navigation logic - Ultra Robust version without direct URL triggers."""
    try:
        Path("scratch").mkdir(exist_ok=True)
        
        # 1. Si on est déjà sur la page sécurisée, on s'arrête là pour laisser l'humain
        if "secure.fnac.com" in page.url and "panier" not in page.url:
            print(f"DEBUG: [Browser] Already on secure checkout flow: {page.url}")
            return True

        # 2. Attente massive de la POP-IN d'ajout au panier (chemin le plus sûr)
        print("DEBUG: [Browser] Waiting up to 15s for post-add popin...")
        popin_selectors = [
            'button:has-text("Voir mon panier")',
            'a:has-text("Voir mon panier")',
            '.btn-primary:has-text("Voir le panier")',
            '#basket-popin-validate',
            'a[href*="panier"].btn-primary'
        ]
        
        for p_sel in popin_selectors:
            try:
                btn = page.locator(p_sel).first
                # On attend que le bouton devienne visible (max 15s au total pour la boucle)
                if btn.is_visible(timeout=5000): 
                    print(f"DEBUG: [Browser] Clicking popin button: {p_sel}")
                    btn.click()
                    page.wait_for_load_state("networkidle", timeout=10000)
                    return True
            except: continue

        # 3. Fallback : On cherche l'icône du panier dans le header (clic visuel uniquement)
        print("DEBUG: [Browser] Popin not found, looking for cart icon in header...")
        cart_selectors = [
            'a[href*="panier"]', 
            'a[href*="basket"]',
            '.header-cart', 
            '#mini-cart', 
            '.js-cart-icon',
            'li.ActionPanel-item--cart a',
            '[data-status="cart"]'
        ]
        
        found_cart = False
        for sel in cart_selectors:
            try:
                locator = page.locator(sel).first
                if locator.is_visible(timeout=3000):
                    print(f"DEBUG: [Browser] Clicking cart icon: {sel}")
                    locator.click()
                    page.wait_for_load_state("networkidle", timeout=10000)
                    found_cart = True
                    break
            except: continue
        
        # 4. Fallback Ultime : Navigation vers l'URL sécurisée (plus robuste que /panier)
        if not found_cart and "panier" not in page.url.lower():
            print("DEBUG: [Browser] No visual path found, attempting secure basket URL...")
            try:
                # On évite le /panier générique qui cause le 404 Lego
                page.goto("https://secure.fnac.com/basket", wait_until="networkidle", timeout=15000)
            except Exception as e:
                print(f"DEBUG: [Browser] Secure fallback failed: {e}")

        # 5. On vérifie si on est bien sur le panier avant de continuer
        if "panier" not in page.url.lower() and "basket" not in page.url.lower():
            print("ERROR: [Browser] Still not on Basket page. Diagnostic capture.")
            page.screenshot(path="scratch/basket_fail.png")
            return False

        # 6. Attente du bouton de validation finale ("Choisir ma livraison")
        print("DEBUG: [Browser] Waiting for Checkout button...")
        checkout_selectors = [
            'button:has-text("Choisir ma livraison")',
            '#panier-validate',
            '.button-basket-validate',
            'button:has-text("Valider mon panier")',
            'button.btn--primary:has-text("Commander")',
            'a:has-text("Valider mon panier")'
        ]
        
        found_checkout = False
        for c_sel in checkout_selectors:
            try:
                btn = page.locator(c_sel).first
                if btn.is_visible(timeout=5000):
                    print(f"DEBUG: [Browser] Clicking Checkout button: {c_sel}")
                    btn.click()
                    found_checkout = True
                    break
            except: continue
                
        if not found_checkout:
             print("DEBUG: [Browser] Checkout button not found visually. Saving screenshot.")
             page.screenshot(path="scratch/checkout_error.png")
             return False

        print("DEBUG: Reached Order stages. Handing over to human or continuing...")
        shipping_btn = page.locator('button:has-text("Valider la livraison"), button:has-text("Passer au paiement"), button:has-text("Suivant")').first
        if shipping_btn.count() > 0:
            shipping_btn.click()
            page.wait_for_load_state("networkidle", timeout=10000)

        print("DEBUG: Reached Payment step.")
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
