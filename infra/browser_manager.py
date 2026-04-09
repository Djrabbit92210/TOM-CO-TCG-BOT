"""Manage a persistent Playwright browser instance for zero-latency detection/purchase."""

from __future__ import annotations

import logging
import random
from typing import Any
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page

from infra.proxy_manager import ProxyManager

logger = logging.getLogger(__name__)

class BrowserManager:
    """Maintains a single browser instance and context for the worker."""

    def __init__(self, headless: bool = False, proxy_manager: ProxyManager | None = None) -> None:
        self.headless = headless
        self.proxy_manager = proxy_manager
        self._pw = None
        self._browser = None
        self._context = None
        self._page = None

    def start(self) -> None:
        """Launch the browser if not already running."""
        if self._browser:
            return
        
        logger.info("[BrowserManager] Starting persistent browser...")
        self._pw = sync_playwright().start()
        
        proxy_conf = self.proxy_manager.get_playwright_proxy() if self.proxy_manager else None
        
        # Args plus furtifs
        launch_args = [
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-infobars",
            "--disable-setuid-sandbox",
        ]
        
        self._browser = self._pw.chromium.launch(
            headless=self.headless,
            proxy=proxy_conf,
            args=launch_args
        )

    def get_context(self, user_agent: str, cookies: list[dict] | None = None) -> BrowserContext:
        """Create or return the persistent context with specific UA and cookies."""
        if self._context:
            return self._context
            
        logger.info("[BrowserManager] Creating persistent context...")
        # Simuler un écran réaliste pour éviter la détection headless
        viewport = {"width": random.randint(1280, 1920), "height": random.randint(720, 1080)}
        
        self._context = self._browser.new_context(
            user_agent=user_agent,
            viewport=viewport,
            locale="fr-FR",
            timezone_id="Europe/Paris",
            ignore_https_errors=True
        )
        
        # Headers plus complets pour matcher un vrai Chrome
        self._context.set_extra_http_headers({
            "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
            "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"macOS"',
            "Upgrade-Insecure-Requests": "1",
        })
        
        if cookies:
            # On ajoute les cookies sans les nettoyer ici pour garder les jetons Akamai (si présents)
            self._context.add_cookies(cookies)
            
        return self._context

    def get_page(self) -> Page:
        """Return the main monitoring page."""
        if self._page and not self._page.is_closed():
            return self._page
            
        if not self._context:
            raise RuntimeError("Context must be initialized before getting a page.")
            
        logger.info("[BrowserManager] Creating persistent page...")
        self._page = self._context.new_page()
        return self._page

    def stop(self) -> None:
        """Clean shutdown."""
        logger.info("[BrowserManager] Stopping persistent browser...")
        if self._page:
            try: self._page.close()
            except: pass
        if self._context:
            try: self._context.close()
            except: pass
        if self._browser:
            try: self._browser.close()
            except: pass
        if self._pw:
            try: self._pw.stop()
            except: pass
        
        self._page = None
        self._context = None
        self._browser = None
        self._pw = None
