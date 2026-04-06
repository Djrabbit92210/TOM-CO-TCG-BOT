from abc import ABC, abstractmethod


class BaseBot(ABC):
    """Abstract bot: site-agnostic loop; delegates to site adapters."""

    @abstractmethod
    def run(self) -> None:
        raise NotImplementedError
