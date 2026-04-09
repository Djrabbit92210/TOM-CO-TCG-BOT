"""Main polling / event loop for a single worker (one egress IP / session pool)."""

import asyncio
import logging
from typing import Any

from bots.base_bot import BaseBot

logger = logging.getLogger(__name__)

class Worker(BaseBot):
    """Runs monitoring and triggers purchase flow via site adapters."""

    def __init__(self, worker_id: str, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.worker_id = worker_id
        self.site = config.get("site")
        self.monitor = None
        
        from infra.proxy_manager import ProxyManager
        self.proxy_manager = ProxyManager()

        if self.site == "fnac":
            from sites.fnac.monitor import FnacMonitor
            from infra.browser_manager import BrowserManager
            # On initialise un manager de navigateur persistant pour ce worker
            logger.info(f"[Worker {self.worker_id}] Initializing persistent BrowserManager...")
            self.browser_manager = BrowserManager(
                headless=False,
                proxy_manager=self.proxy_manager
            )
            watch_cfg = config.get("fnac_watch")
            self.monitor = FnacMonitor(
                watch=watch_cfg,
                browser_manager=self.browser_manager
            )

    async def run(self) -> None:
        self._running = True
        logger.info(f"[Worker {self.worker_id}] Starting task monitoring: {self.config}")
        
        while self._running:
            try:
                if self.monitor:
                    logger.info(f"[Worker {self.worker_id}] Polling {self.site}...")
                    # Run the synchronous Playwright/HTTP polling in a background thread
                    snapshot = await asyncio.to_thread(self.monitor.poll_once)
                    logger.info(f"[Worker {self.worker_id}] Result: ready={snapshot.ready_to_buy}, reason={snapshot.reason}, price={snapshot.price_eur}, title={snapshot.matched_title}")
                    
                    if snapshot.ready_to_buy:
                        logger.warning(f"[Worker {self.worker_id}] SUCCESS! Product found and ready to buy.")
                        logger.warning(f"[Worker {self.worker_id}] Triggering purchase flow...")
                        # Turbo mode: use the snapshot already fetched
                        result = await asyncio.to_thread(self.monitor.purchase_from_snapshot, snapshot)
                        if result and result.ok:
                            logger.warning(f"[Worker {self.worker_id}] Purchase sequence complete. Stopping worker.")
                            self._running = False
                            break
                else:
                    logger.info(f"[Worker {self.worker_id}] Checking stock for item ... (mocking {self.site})")
                    
                import random
                jitter = random.uniform(8, 18)
                await asyncio.sleep(jitter)  # Attente plus humaine et aléatoire
            except asyncio.CancelledError:
                logger.info(f"[Worker {self.worker_id}] Task cancelled from orchestrator.")
                break
            except Exception as e:
                logger.error(f"[Worker {self.worker_id}] Error in worker loop: {e}")
                await asyncio.sleep(5)
                
        # Shutdown cleanup - En mode Ghost, on ne ferme PAS si on a réussi la mission
        if hasattr(self, 'browser_manager'):
            if self._running: # Si on s'arrête suite à une erreur ou un Ctrl+C
                await asyncio.to_thread(self.browser_manager.stop)
            else:
                logger.info(f"[Worker {self.worker_id}] SUCCESS: Leaving browser open for user interaction.")
        logger.info(f"[Worker {self.worker_id}] Shutdown complete.")
