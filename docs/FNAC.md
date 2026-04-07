# Fnac bot (Python)

## Setup

```bash
cd TOM-CO-TCG-BOT
pip install -e .
playwright install chromium
```

`data/` is gitignored — cookies and captures stay local (`data/cookies/fnac.json`, `data/fnac_api_capture.json`).

## Commands (from package root)

| Command | Purpose |
|--------|---------|
| `python -m sites.fnac add --product-id <id> [--no-headless] [-v]` | Add to cart (`POST /basket/add`). Uses httpx, falls back to Playwright if Akamai blocks. `-v` prints raw body snippet. |
| `python -m sites.fnac capture --no-headless --duration 180 --out ./data/fnac_api_capture.json` | Records XHR/fetch (+ status/content-type). Keep browser open and do search → product → add → Panier manually. |
| `python -m sites.fnac analyze-capture --in ./data/fnac_api_capture.json` | Summarizes capture (hosts, methods, likely JSON endpoints). |
| `python -m sites.fnac probe --playwright [--no-headless]` | GET `/basket*` via real navigation (not raw `request.get`). |
| `python -m sites.fnac watch --mode url --url <pdp> --dry-run [--no-headless]` | Poll stock/price heuristics without buying. |

## Interface config

If JSON includes `"site": "fnac"`, `parse_interface_config` attaches `fnac_watch` (see `sites/fnac/interface.py`).

## Notes

- **Akamai**: raw HTTP often fails; Playwright session + cookies is the reliable path for now.
- **Product id**: usually the digits in `https://www.fnac.com/a21424410/...` = `productID` for the basket API.
