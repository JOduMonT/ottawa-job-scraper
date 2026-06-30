"""
Helper for scraping JS-rendered career pages (Workday, Avature, etc.)
using a headless browser via Playwright.

Only import/use this in scrapers that actually need it - it's much
slower and heavier than plain requests.
"""
from playwright.sync_api import sync_playwright

DEFAULT_WAIT_MS = 4000


def get_rendered_html(url, wait_selector=None, wait_ms=DEFAULT_WAIT_MS, scroll=False):
    """
    Loads a URL in headless Chromium and returns the fully rendered HTML.
    wait_selector: CSS selector to wait for before grabbing HTML (preferred over wait_ms when known)
    scroll: set True for infinite-scroll job boards that lazy-load more postings
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
        )
        page.goto(url, timeout=30000)

        if wait_selector:
            try:
                page.wait_for_selector(wait_selector, timeout=15000)
            except Exception:
                pass  # fall through and grab whatever loaded - caller should handle empty results
        else:
            page.wait_for_timeout(wait_ms)

        if scroll:
            for _ in range(5):
                page.mouse.wheel(0, 2000)
                page.wait_for_timeout(1000)

        html = page.content()
        browser.close()
        return html
