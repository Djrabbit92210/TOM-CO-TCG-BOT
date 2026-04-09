"""Configure outbound proxies per worker."""

import logging

logger = logging.getLogger(__name__)

class ProxyManager:
    """Manages the outbound tunnel connection (Ionos via v2box local proxy)."""

    def __init__(self, use_tunnel: bool = True) -> None:
        # Adresse locale du tunnel v2box/v2ray sur Mac (PacketTun).
        self._base_url = "127.0.0.1:1087"
        self.use_tunnel = use_tunnel

    def get_proxy(self) -> str | None:
        """Returns the string proxy URL for httpx."""
        if not self.use_tunnel:
            return None
        return f"socks5://{self._base_url}"
        
    def get_playwright_proxy(self) -> dict[str, str] | None:
        """Returns the dictionary format required by Playwright."""
        if not self.use_tunnel:
            return None
        return {"server": f"socks5://{self._base_url}"}
