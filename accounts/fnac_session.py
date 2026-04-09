"""Headed Playwright flow: manual Fnac login, then persist cookies for a registry label."""

from __future__ import annotations

import importlib.util
import sys
import time
import types
from pathlib import Path

from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from accounts.cookie_store import CookieStore
from accounts.session_store import SessionStore


def _fnac_config_module() -> types.ModuleType:
    """Load ``sites/fnac/config.py`` without importing ``sites.fnac`` (heavy ``__init__``)."""
    name = "tom_co_fnac_config_runtime"
    if name in sys.modules:
        return sys.modules[name]
    root = Path(__file__).resolve().parents[1]
    path = root / "sites" / "fnac" / "config.py"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise FileNotFoundError(f"Missing Fnac config at {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


config = _fnac_config_module()

_LAUNCH_ARGS = [
    "--disable-blink-features=AutomationControlled",
    "--no-sandbox",
    "--disable-setuid-sandbox",
]


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


def capture_fnac_session_after_manual_login(
    *,
    cookie_label: str,
    cookie_store: CookieStore | None = None,
    session_store: SessionStore | None = None,
    user_agent: str | None = None,
    login_url: str | None = None,
    start_path: str | None = None,
) -> Path:
    """
    Opens a visible browser on Fnac login. You complete login (and any address setup) yourself,
    then press Enter in the terminal to save ``context.cookies()`` for ``cookie_label``.
    """
    ua = user_agent or config.DEFAULT_USER_AGENT
    url = login_url or config.FNAC_LOGIN_URL
    store = cookie_store or CookieStore()
    reg = session_store

    print(f"Browser opening: {url}")
    print("After you are logged in and the account looks good, return here and press Enter to save cookies.")
    if start_path:
        print(f"(Optional warm-up) storefront path after login: {start_path}")

    cookies: list[dict] = []
    out = store.path_for(cookie_label)
    with sync_playwright() as p:
        browser: Browser = p.chromium.launch(headless=False, args=_LAUNCH_ARGS)
        ctx = _new_context(browser, ua)
        raw = store.load(cookie_label)
        if raw:
            ctx.add_cookies(raw)
        page = ctx.new_page()
        try:
            page.goto(url, timeout=120_000, wait_until="domcontentloaded")
            _accept_cookies(page)
            input("Press Enter when logged in and ready to save cookies… ")
            if start_path:
                path = start_path if start_path.startswith("/") else f"/{start_path}"
                page.goto(f"{config.BASE_URL}{path}", timeout=120_000, wait_until="domcontentloaded")
                time.sleep(0.5)
            cookies = ctx.cookies()
            store.save(cookie_label, cookies)
            out = store.path_for(cookie_label)
            if reg:
                reg.touch_session_by_cookie_label(cookie_label, status="ok")
        finally:
            page.close()
            ctx.close()
            browser.close()

    print(f"Saved {len(cookies)} cookies to {out}")
    return out
