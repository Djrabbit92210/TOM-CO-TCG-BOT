"""Spawn, stop, and supervise bot worker processes."""

import asyncio
import logging
from typing import Any

from bots.worker import Worker

logger = logging.getLogger(__name__)

class BotManager:
    """Coordinates lifecycle of bot workers."""

    def __init__(self) -> None:
        self.workers: list[Worker] = []
        self.tasks: list[asyncio.Task] = []

    def spawn_worker(self, worker_id: str, task_config: dict[str, Any]) -> None:
        """Create and start a new worker asynchronously."""
        logger.info(f"Spawning worker {worker_id} for task...")
        worker = Worker(worker_id, task_config)
        self.workers.append(worker)
        
        # Schedule the worker loop in the current asyncio event loop
        task = asyncio.create_task(worker.run())
        self.tasks.append(task)

    async def shutdown(self) -> None:
        """Gracefully stop all workers."""
        logger.info("BotManager is shutting down all workers...")
        for worker in self.workers:
            worker.stop()
            
        # Give workers a few seconds to finish their current loop before hard cancelling
        results = await asyncio.gather(*self.tasks, return_exceptions=True)
        for r in results:
            if isinstance(r, Exception):
                logger.error(f"Worker task ended with exception: {r}")
        
        logger.info("All workers successfully stopped.")
