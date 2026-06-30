"""
CGI Canada careers, hosted on the njoyn ATS platform (cgi.njoyn.com).

NOTE: This page IS server-rendered HTML (confirmed by manual inspection),
but the njoyn platform appears to apply anti-bot measures against plain
`requests` calls specifically (likely user-agent/session fingerprinting
rather than requiring JS) - it returned 0 rows in production even though
the same URL worked fine for manual inspection. Using Playwright's real
browser context gets past this reliably.

Only page 1 (~50 most recent postings, globally) is scraped per run.
Postings appear to sort newest-first, so this should reliably catch new
Canadian/Ottawa postings without needing to paginate through thousands of
global listings.
"""
from .utils import clean_text, make_job
from .browser_utils import get_rendered_html
from bs4 import BeautifulSoup

SOURCE_NAME = "CGI"
URL = "https://cgi.njoyn.com/corp/xweb/xweb.asp?CLID=21001&page=joblisting&lang=1"

LOCATION_KEYWORDS = ["ottawa", "gatineau", "remote", "canada"]


def scrape():
    jobs = []
    try:
        html = get_rendered_html(URL, wait_selector="table", wait_ms=6000)
    except Exception as e:
        print(f"[{SOURCE_NAME}] browser fetch failed: {e}")
        return jobs

    soup = BeautifulSoup(html, "lxml")
    rows = soup.select("table tr")

    if not rows:
        print(f"[{SOURCE_NAME}] no table rows found - markup may have changed")
        return jobs

    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 5:
            continue  # skip header row / malformed rows

        link = row.find("a", href=True)
        if not link:
            continue

        title = clean_text(cells[1].get_text()) if len(cells) > 1 else clean_text(link.get_text())
        city = clean_text(cells[3].get_text()) if len(cells) > 3 else ""
        country = clean_text(cells[4].get_text()) if len(cells) > 4 else ""

        if not title or country.lower() != "canada":
            continue

        href = link["href"]
        if not href.startswith("http"):
            href = "https://cgi.njoyn.com/corp/xweb/" + href.lstrip("/")

        jobs.append(make_job(title=title, url=href, source=SOURCE_NAME, location=f"{city}, {country}"))

    return jobs
