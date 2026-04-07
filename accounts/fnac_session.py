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
    name = "tom_co_fnac_config_runtime"
    if name in sys.modules: return sys.modules[name]
    root = Path(__file__).resolve().parents[1]
    path = root / "sites" / "fnac" / "config.py"
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

config = _fnac_config_module()
_LAUNCH_ARGS = ["--disable-blink-features=AutomationControlled", "--no-sandbox", "--disable-setuid-sandbox"]

def _accept_cookies(page: Page) -> None:
    btn = page.locator("button#onetrust-accept-btn-handler")
    if btn.count() > 0:
        try:
            btn.click(timeout=5000)
            time.sleep(0.5)
        except Exception: pass

def _new_context(browser: Browser, user_agent: str) -> BrowserContext:
    ctx = browser.new_context(user_agent=user_agent, locale="fr-FR", ignore_https_errors=True)
    ctx.set_extra_http_headers({"Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7"})
    return ctx

def farm_fnac_session(cookie_label: str, cookie_store: CookieStore, user_agent: str | None = None) -> bool:
    """Approche Hybride : Ouvre un navigateur invisible pour rafraîchir les jetons Akamai."""
    ua = user_agent or config.DEFAULT_USER_AGENT
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=_LAUNCH_ARGS)
        ctx = _new_context(browser, ua)
        raw = cookie_store.load(cookie_label)
        if raw: ctx.add_cookies(raw)
        page = ctx.new_page()
        try:
            page.goto(config.BASE_URL, wait_until="networkidle", timeout=60000)
            _accept_cookies(page)
            time.sleep(2) # Temps pour les calculs anti-bot
            cookie_store.save(cookie_label, ctx.cookies())
            return True
        except Exception: return False
        finally: browser.close()

def capture_fnac_session_after_manual_login(*, cookie_label: str, cookie_store: CookieStore | None = None, session_store: SessionStore | None = None, user_agent: str | None = None, login_url: str | None = None, start_path: str | None = None) -> Path:
    ua = user_agent or config.DEFAULT_USER_AGENT
    url = login_url or config.FNAC_LOGIN_URL
    store = cookie_store or CookieStore()
    reg = session_store
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=_LAUNCH_ARGS)
        ctx = _new_context(browser, ua)
        page = ctx.new_page()
        page.goto(url, timeout=120_000, wait_until="domcontentloaded")
        input("Connectez-vous, puis appuyez sur Entrée ICI pour sauvegarder la session...")
        store.save(cookie_label, ctx.cookies())
        if reg: reg.touch_session_by_cookie_label(cookie_label, status="ok")
        browser.close()
    return store.path_for(cookie_label)