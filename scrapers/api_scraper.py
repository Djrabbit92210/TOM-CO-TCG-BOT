from scrapers.base_scraper import BaseScraper


class ApiScraper(BaseScraper):
    """HTTP/API-based stock and price checks (to be implemented)."""

    def check_availability(self, product_ref: object) -> bool:
        return False
