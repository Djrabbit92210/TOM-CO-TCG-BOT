"""Unit tests for Fnac URL parsing, matching, scraping, interface mapping."""

from __future__ import annotations

from orchestrator.config_parser import parse_interface_config
from sites.fnac.interface import fnac_watch_from_interface
from sites.fnac.match import listing_matches, normalize_for_match, overlap_score
from sites.fnac.product_id import extract_product_id_from_html, extract_product_id_from_url
from sites.fnac.scrape import parse_search_results


def test_extract_product_id_from_fnac_url() -> None:
    u = "https://www.fnac.com/a21424410/Pokemon-Whatever"
    assert extract_product_id_from_url(u) == "21424410"


def test_extract_product_id_from_json_blob() -> None:
    html = 'window.x = {"productID":"21424410"};'
    assert extract_product_id_from_html(html) == "21424410"


def test_normalize_for_match_strips_accents() -> None:
    assert "elite" in normalize_for_match("Élite Trainer")


def test_listing_matches_keywords_and_name() -> None:
    assert listing_matches(
        "Pokémon ETB Chaos Rising",
        name_hint="Chaos Rising",
        keyword_groups=[["etb"], ["chaos"]],
    )
    assert not listing_matches(
        "Pokémon ETB Brilliant Stars",
        name_hint="Chaos Rising",
        keyword_groups=[["etb"], ["chaos"]],
    )


def test_listing_exclude() -> None:
    assert not listing_matches(
        "Elite Trainer Brilliant",
        name_hint="elite",
        exclude_substrings=["brilliant"],
    )


def test_overlap_score() -> None:
    assert overlap_score("Chaos Rising ETB", "Pokemon ETB Chaos Rising Box") > 0.2


def test_parse_search_results_finds_article_links() -> None:
    html = """
    <html><body>
    <div>
      <a href="/a21424410/Test-Product" title="Test Product">Test Product</a>
      <span>49,99 €</span>
      <button>Ajouter au panier</button>
    </div>
    </body></html>
    """
    listings = parse_search_results(html)
    assert len(listings) == 1
    assert listings[0].product_id == "21424410"
    assert listings[0].add_to_cart_hint


def test_fnac_watch_from_interface() -> None:
    cfg = fnac_watch_from_interface(
        {
            "site": "fnac",
            "mode": "search",
            "search_query": "pokemon etb",
            "product_name": "Chaos",
            "keyword_groups": [["etb"], ["chaos"]],
            "price_max": 60,
        }
    )
    assert cfg.mode == "search"
    assert "pokemon" in cfg.search_referer_path().lower()
    assert cfg.price_max_eur == 60.0


def test_parse_interface_config_attaches_fnac_watch() -> None:
    raw = {"site": "fnac", "mode": "url", "product_url": "https://www.fnac.com/a1/x"}
    out = parse_interface_config(raw)
    assert "fnac_watch" in out
    assert out["fnac_watch"].product_url == "https://www.fnac.com/a1/x"
