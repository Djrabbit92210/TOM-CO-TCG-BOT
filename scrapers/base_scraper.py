from abc import ABC, abstractmethod


class BaseScraper(ABC):
    """Shared interface for availability checks."""

    @abstractmethod
    def check_availability(self, product_ref: object) -> bool:
        raise NotImplementedError
