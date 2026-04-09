import sys
import os
import time
from pathlib import Path

# Add project root to sys.path
sys.path.append(os.getcwd())

from sites.fnac.playwright_fnac import fetch_html_playwright
from sites.fnac.http_client import FnacHttpClient
from accounts.cookie_store import CookieStore
from infra.proxy_manager import ProxyManager

proxy = ProxyManager()
store = CookieStore()
url = "https://www.fnac.com/SearchResult/ResultList.aspx?Search=BTS+ARIRANG&sft=1&sa=0"

print("--- TEST 0: Google (via SOCKS5) ---")
try:
    with FnacHttpClient(cookie_store=store, proxy_manager=proxy) as http:
        r = http.get_page("https://www.google.com")
        print(f"Google Status: {r.status_code}")
except Exception as e:
    print(f"Google failed: {e}")

print("\n--- TEST 1: Fnac (via SOCKS5) ---")
try:
    with FnacHttpClient(cookie_store=store, proxy_manager=proxy) as http:
        r = http.get_page(url)
        print(f"Fnac Status: {r.status_code}")
except Exception as e:
    print(f"Fnac failed: {e}")

print("\n--- TEST 2: Playwright (via SOCKS5) ---")
try:
    html, final_url = fetch_html_playwright(
        url,
        cookie_store=store,
        user_agent=None,
        headless=False,
        proxy_manager=proxy
    )
    print(f"Playwright Status: Success")
    print(f"Playwright HTML Length: {len(html)}")
    print(f"Final URL: {final_url}")
    if "fnac.com" in final_url and len(html) > 1000:
        print("SUCCESS: Products page loaded!")
    else:
        print("FAILURE: Still getting empty page or queue.")
except Exception as e:
    print(f"Playwright failed: {e}")
