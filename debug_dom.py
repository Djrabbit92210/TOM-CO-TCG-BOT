from playwright.sync_api import sync_playwright

url = "https://www.fnac.com/SearchResult/ResultList.aspx?Search=BTS+ARIRANG&sft=1&sa=0"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url, wait_until="domcontentloaded")
    html = page.content()
    
    # Check what kind of product links are found:
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    found = []
    for a in soup.find_all("a", href=True):
        if "/a" in a["href"].lower():
            found.append(a["href"])
            
    print(f"Total links with '/a': {len(found)}")
    if found:
        print("Sample:", found[:3])
    else:
        print("No '/a' links found! FNAC changed their DOM.")
    browser.close()
