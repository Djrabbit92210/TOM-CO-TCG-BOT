from scrapers.base_scraper import BaseScraper


class BrowserScraper(BaseScraper):
    """Playwright-based detection (to be implemented)."""

    def check_availability(self, product_ref: object) -> bool:
        return False
