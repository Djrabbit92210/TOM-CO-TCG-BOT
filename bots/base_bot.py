from abc import ABC, abstractmethod
from typing import Any

class BaseBot(ABC):
    """Abstract bot: site-agnostic loop; delegates to site adapters."""

    def __init__(self, config: dict[str, Any]):
        self.config = config
        self._running = False

    @abstractmethod
    async def run(self) -> None:
        """Main asynchronous event loop for the bot."""
        raise NotImplementedError

    def stop(self) -> None:
        """Tells the bot to gracefully wind down its run loop."""
        self._running = False
