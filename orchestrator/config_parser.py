"""Parse and validate configuration from the interface / API."""

from __future__ import annotations

from typing import Any

from scrapers.product_match import normalize_product_match_block
from sites.fnac.interface import fnac_watch_from_interface, is_fnac_job


def parse_interface_config(raw: dict[str, Any]) -> dict[str, Any]:
    """
    Normalize interface payload; validates ``products[].match`` (keyword groups + excludes).

    Expected product shape (interface → API):

    .. code-block:: json

        {
          "products": [
            {
              "display_name": "ETB Chaos Rising",
              "match": {
                "required_groups": [
                  ["etb", "elite trainer box"],
                  ["chaos rising"]
                ],
                "exclude": ["ascended heroes"]
              }
            }
          ]
        }
    """
    out = dict(raw)
    products = out.get("products")
    if isinstance(products, list):
        out["products"] = [normalize_product_match_block(dict(p)) for p in products]
    if is_fnac_job(raw):
        out["fnac_watch"] = fnac_watch_from_interface(raw)
    return out
