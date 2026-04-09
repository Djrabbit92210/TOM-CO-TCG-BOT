"""Manage a persistent Playwright browser instance for zero-latency detection/purchase.
Supports 'Ghost Mode' (connecting to a real Chrome instance via CDP)."""

from __future__ import annotations

import logging
import random
import time
from typing import Any
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page

from infra.proxy_manager import ProxyManager

logger = logging.getLogger(__name__)

SERVICE_WORKERS_PATCH = """
Object.defineProperty(navigator, 'webdriver', { get: () => False });
"""

STEALTH_JS = """
// Masque le fait que le navigateur est piloté
Object.defineProperty(navigator, 'webdriver', {
    get: () => false
});

// Patch supplémentaire pour les empreintes communes
window.chrome = {
    runtime: {},
    loadTimes: function() {},
    csi: function() {},
    app: {}
};
"""

class BrowserManager:
    """Maintains a single browser instance and context for the worker."""

    def __init__(self, headless: bool = False, proxy_manager: ProxyManager | None = None) -> None:
        self.headless = headless
        self.proxy_manager = proxy_manager
        self._pw = None
        self._browser = None
        self._context = None
        self._page = None
        self.is_ghost_mode = False

    def start(self) -> None:
        """Launch the browser or connect to an existing one via CDP."""
        if self._browser:
            return
        
        # On force Playwright à ignorer la boucle asyncio présente dans le thread principal
        self._pw = sync_playwright().start()
        
        # Tentative de connexion au port de débogage (Ghost Mode)
        try:
            logger.info("[BrowserManager] Attempting to connect to existing Chrome (Ghost Mode) on port 9222...")
            self._browser = self._pw.chromium.connect_over_cdp("http://localhost:9222")
            self.is_ghost_mode = True
            logger.info("[BrowserManager] Successfully connected to existing Chrome! 👻")
            
            # Application de la furtivité sur le contexte existant
            self._context = self._browser.contexts[0]
            self._context.add_init_script(STEALTH_JS)
            
            # On écoute aussi les nouvelles pages pour leur appliquer le script
            self._context.on("page", lambda page: page.add_init_script(STEALTH_JS))
        except Exception:
            logger.info("[BrowserManager] Ghost Mode not available (Chrome debug not found). Falling back to standard launch.")
            self.is_ghost_mode = False
            
            proxy_conf = self.proxy_manager.get_playwright_proxy() if self.proxy_manager else None
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
        """Create or return the persistent context."""
        if self._context:
            return self._context
            
        if self.is_ghost_mode:
            # En mode CDP, on utilise le contexte par défaut déjà ouvert dans Chrome
            # Le proxy est déjà géré par les flags de lancement de Chrome dans launch_fnac_chrome.sh
            self._context = self._browser.contexts[0]
            logger.info("[BrowserManager] Using existing Chrome context (Native Proxy active).")
            return self._context

        logger.info("[BrowserManager] Creating new persistent context...")
        viewport = {"width": random.randint(1280, 1920), "height": random.randint(720, 1080)}
        self._context = self._browser.new_context(
            user_agent=user_agent,
            viewport=viewport,
            locale="fr-FR",
            timezone_id="Europe/Paris",
            ignore_https_errors=True
        )
        
        self._context.set_extra_http_headers({
            "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
            "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"macOS"',
            "Upgrade-Insecure-Requests": "1",
        })
        
        if cookies:
            self._context.add_cookies(cookies)
            
        return self._context

    def get_page(self) -> Page:
        """Return the main monitoring page."""
        if self._page and not self._page.is_closed():
            return self._page
            
        if not self._context:
            raise RuntimeError("Context must be initialized before getting a page.")
            
        if self.is_ghost_mode:
            # On cherche s'il y a déjà une page ouverte sur fnac.com
            for p in self._context.pages:
                if "fnac.com" in p.url:
                    self._page = p
                    logger.info(f"[BrowserManager] Attached to existing Fnac page: {p.url}")
                    return self._page
            # Sinon on en crée une nouvelle dans le navigateur réel
            logger.info("[BrowserManager] Creating new page in existing Chrome.")
            self._page = self._context.new_page()
            return self._page

        logger.info("[BrowserManager] Creating new persistent page...")
        self._page = self._context.new_page()
        return self._page

    def stop(self) -> None:
        """Clean shutdown (in Ghost Mode, we don't close the browser to let user continue)."""
        logger.info("[BrowserManager] Stopping session...")
        if self.is_ghost_mode:
            # En mode fantôme, on se déconnecte juste sans tuer le Chrome de l'utilisateur
            self._page = None
            self._context = None
            if self._browser:
                try: self._browser.close() # close() on a CDP browser just disconnects unless forced
                except: pass
            if self._pw:
                try: self._pw.stop()
                except: pass
        else:
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
