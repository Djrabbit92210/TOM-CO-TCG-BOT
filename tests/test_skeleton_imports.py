"""Smoke import of skeleton packages (run from repo root)."""


def test_import_orchestrator() -> None:
    import orchestrator  # noqa: F401


def test_import_sites_base() -> None:
    from sites.base import SiteAdapter

    assert SiteAdapter is not None


def test_keyword_engine() -> None:
    from scrapers.keyword_engine import matches_keywords

    assert matches_keywords("ETB Chaos Rising Elite Trainer", [["etb"], ["chaos"]])
