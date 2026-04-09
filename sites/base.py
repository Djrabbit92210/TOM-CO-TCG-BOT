from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class SiteAdapter(Protocol):
    """Contract each retailer implements for replication across sites."""

    site_id: str
    supports_api: bool

    def search_products(self, query: str) -> list[dict[str, Any]]:
        """Return candidate products (ids, urls, titles, prices if known)."""
        ...

    def get_product(self, url: str) -> dict[str, Any]:
        """Normalize product details for orchestrator (stub shape)."""
        ...

    def buy(self, product: dict[str, Any], account: Any, payment: Any) -> bool:
        """Cart through checkout; return True on confirmed purchase."""
        ...
