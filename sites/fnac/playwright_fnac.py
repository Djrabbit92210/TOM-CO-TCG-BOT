"""Playwright: Akamai-friendly session, basket POST, HTML fetch, API capture."""

from __future__ import annotations

import json
import time
from collections import OrderedDict
from pathlib import Path
from typing import Any

from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from accounts.cookie_store import CookieStore
from sites.fnac import config

_LAUNCH_ARGS = [
    "--disable-blink-features=AutomationControlled",
    "--no-sandbox",
    "--disable-setuid-sandbox",
]

AKAMAI_MARKERS = ("akam/", "Please enable JS", "id=\"cmsg\"", "bazadebezolkohpepadr")


def is_akamai_challenge(html: str) -> bool:
    if not html:
        return True
    h = html[:8000].lower()
    return any(m.lower() in h for m in AKAMAI_MARKERS)


def _accept_cookies(page: Page) -> None:
    btn = page.locator("button#onetrust-accept-btn-handler")
    if btn.count() > 0:
        try:
            btn.click(timeout=5000)
            time.sleep(0.5)
        except Exception:
            pass


def _new_context(browser: Browser, user_agent: str) -> BrowserContext:
    ctx = browser.new_context(
        user_agent=user_agent,
        locale="fr-FR",
        ignore_https_errors=True,
    )
    ctx.set_extra_http_headers(
        {"Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7"}
    )
    return ctx


def _load_cookies(ctx: BrowserContext, store: CookieStore | None) -> None:
    if not store:
        return
    raw = store.load(config.COOKIE_LABEL)
    if raw:
        ctx.add_cookies(raw)


def _save_cookies(ctx: BrowserContext, store: CookieStore | None) -> None:
    if store:
        store.save(config.COOKIE_LABEL, ctx.cookies())


def warm_page(
    page: Page,
    referer_path: str,
    *,
    timeout_ms: int = 90_000,
) -> str:
    """Home → cookies → storefront path. Returns final URL for Referer."""
    page.goto(config.BASE_URL, timeout=timeout_ms, wait_until="domcontentloaded")
    _accept_cookies(page)
    time.sleep(0.4)
    path = referer_path if referer_path.startswith("/") else f"/{referer_path}"
    page.goto(f"{config.BASE_URL}{path}", timeout=timeout_ms, wait_until="domcontentloaded")
    time.sleep(0.5)
    return page.url


def add_to_cart_playwright(
    product_id: str,
    payload: list[dict[str, Any]],
    *,
    referer_path: str,
    cookie_store: CookieStore | None,
    user_agent: str,
    headless: bool,
) -> tuple[bool, int, Any, str]:
    """POST /basket/add via Playwright APIRequest (same cookie jar as page)."""
    body = json.dumps(payload, separators=(",", ":"))
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless, args=_LAUNCH_ARGS)
        ctx = _new_context(browser, user_agent)
        _load_cookies(ctx, cookie_store)
        page = ctx.new_page()
        try:
            referer = warm_page(page, referer_path)
            resp = page.request.post(
                config.BASKET_ADD_URL,
                data=body,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json, text/plain, */*",
                    "Origin": config.BASE_URL,
                    "Referer": referer,
                },
            )
            raw = resp.text()
            try:
                parsed: Any = resp.json()
            except Exception:
                parsed = raw
            ok = 200 <= resp.status < 300
            _save_cookies(ctx, cookie_store)
            return ok, resp.status, parsed, raw
        finally:
            page.close()
            ctx.close()
            browser.close()


def fetch_html_playwright(
    target: str,
    *,
    cookie_store: CookieStore | None,
    user_agent: str,
    headless: bool,
    warm_path: str | None = None,
) -> tuple[str, str]:
    """
    Load a URL (full https URL or path like /SearchResult/...).
    If warm_path is set, open home + cookies + warm_path first (better Referer cookie flow).
    Returns (html, final_url).
    """
    url = target if target.startswith("http") else f"{config.BASE_URL}{target if target.startswith('/') else '/' + target}"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless, args=_LAUNCH_ARGS)
        ctx = _new_context(browser, user_agent)
        _load_cookies(ctx, cookie_store)
        page = ctx.new_page()
        try:
            if warm_path:
                warm_page(page, warm_path)
            page.goto(url, timeout=90_000, wait_until="domcontentloaded")
            time.sleep(0.4)
            html = page.content()
            final = page.url
            _save_cookies(ctx, cookie_store)
            return html, final
        finally:
            page.close()
            ctx.close()
            browser.close()


def get_with_session_playwright(
    target_url: str,
    *,
    referer_path: str,
    cookie_store: CookieStore | None,
    user_agent: str,
    headless: bool,
) -> tuple[int, str]:
    """
    Open a Fnac URL like a real visit: warm session, then **navigate** (``page.goto``).

    Using ``page.request.get`` for ``/basket`` often returns HTTP 403 + “Maintenance” HTML;
    full navigation matches the browser tab and usually works.
    """
    url = (
        target_url
        if target_url.startswith("http")
        else f"{config.BASE_URL}{target_url if target_url.startswith('/') else '/' + target_url}"
    )
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless, args=_LAUNCH_ARGS)
        ctx = _new_context(browser, user_agent)
        _load_cookies(ctx, cookie_store)
        page = ctx.new_page()
        try:
            warm_page(page, referer_path)
            resp = page.goto(url, timeout=90_000, wait_until="domcontentloaded")
            time.sleep(0.5)
            status = int(resp.status) if resp is not None else 0
            text = page.content()
            _save_cookies(ctx, cookie_store)
            return status, text
        finally:
            page.close()
            ctx.close()
            browser.close()


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
) -> list[dict[str, Any]]:
    """
    Log XHR/fetch to *.fnac.com / secure.fnac.com while running a short scripted browse.
    Writes JSON array to output_path.
    """
    rows: "OrderedDict[str, dict[str, Any]]" = OrderedDict()

    def key_for(method: str, url: str) -> str:
        return f"{method}\t{url}"

    def on_request(request) -> None:
        try:
            rt = request.resource_type
            u = request.url
            if "fnac.com" not in u and "secure.fnac.com" not in u:
                return
            ul = u.lower()
            interesting_path = any(
                x in ul for x in ("/basket", "/cart", "/api/", "/panier", "/checkout", "graphql")
            )
            if rt not in ("xhr", "fetch") and not interesting_path:
                return
            k = key_for(request.method, u)
            if k in rows:
                return
            post = request.post_data
            if post and len(post) > 4000:
                post = post[:4000] + "…"
            rows[k] = {
                "method": request.method,
                "url": u,
                "resourceType": rt,
                "postData": post,
            }
        except Exception:
            pass

    def on_response(response) -> None:
        try:
            req = response.request
            u = req.url
            if "fnac.com" not in u and "secure.fnac.com" not in u:
                return
            k = key_for(req.method, u)
            if k not in rows:
                # Only enrich what we already decided to keep.
                return
            rows[k]["status"] = response.status
            try:
                ct = response.headers.get("content-type")
            except Exception:
                ct = None
            if ct:
                rows[k]["contentType"] = ct
        except Exception:
            pass

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless, args=_LAUNCH_ARGS)
        ctx = _new_context(browser, user_agent)
        _load_cookies(ctx, cookie_store)
        page = ctx.new_page()
        page.on("request", on_request)
        page.on("response", on_response)
        try:
            warm_page(page, referer_path)
            if extra_goto_url:
                page.goto(
                    extra_goto_url if extra_goto_url.startswith("http") else config.BASE_URL + extra_goto_url,
                    timeout=90_000,
                    wait_until="domcontentloaded",
                )
                time.sleep(0.6)
            if auto_click_add_to_cart:
                btn = page.locator("button:has-text('Ajouter au panier')").first
                if btn.count() > 0:
                    try:
                        btn.scroll_into_view_if_needed()
                        time.sleep(0.3)
                        btn.click(timeout=15_000)
                        time.sleep(2.0)
                    except Exception:
                        pass
            # Give time for a manual workflow (search → refresh → click → refresh → add → basket → checkout).
            time.sleep(max(0.0, duration_seconds))
            time.sleep(max(0.0, settle_seconds))
            _save_cookies(ctx, cookie_store)
        finally:
            page.close()
            ctx.close()
            browser.close()

    out_list = list(rows.values())
    output_path.write_text(json.dumps(out_list, indent=2, ensure_ascii=False), encoding="utf-8")
    from sites.fnac.capture_tools import write_sidecar_report

    write_sidecar_report(output_path, out_list)
    return out_list
