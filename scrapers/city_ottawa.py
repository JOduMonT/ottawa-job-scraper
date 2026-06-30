"""
City of Ottawa careers (SuccessFactors-based career site).
Filters to the "Information Technology jobs" category.

URL and matching pattern confirmed correct via live inspection - the issue
is plain `requests` returning 0 results in production (same anti-bot
pattern seen with CGI's njoyn platform: works fine for a one-off manual
fetch but gets blocked on repeated/non-browser traffic). Switched to
Playwright's real browser context to get past this.
"""
import re
from .utils import clean_text, make_job
from .browser_utils import get_rendered_html
from bs4 import BeautifulSoup

SOURCE_NAME = "City of Ottawa"
URL = "https://jobs-emplois.ottawa.ca/city-jobs/go/Information-Technology-jobs/8649547/"

# Real job posting URLs look like: /city-jobs/job/<slug>/<numeric-id>/
JOB_URL_PATTERN = re.compile(r"/city-jobs/job/")


def scrape():
    jobs = []
    try:
        html = get_rendered_html(URL, wait_selector="a[href*='/city-jobs/job/']", wait_ms=6000)
    except Exception as e:
        print(f"[{SOURCE_NAME}] browser fetch failed: {e}")
        return jobs

    soup = BeautifulSoup(html, "lxml")
    links = soup.find_all("a", href=True)
    seen_urls = set()

    for link in links:
        href = link["href"]
        if not JOB_URL_PATTERN.search(href):
            continue

        title = clean_text(link.get_text())
        if not title or len(title) < 5:
            continue

        if href.startswith("/"):
            href = "https://jobs-emplois.ottawa.ca" + href

        if href in seen_urls:
            continue
        seen_urls.add(href)

        jobs.append(make_job(title=title, url=href, source=SOURCE_NAME))

    if not jobs:
        print(f"[{SOURCE_NAME}] no job links found - could genuinely mean 0 postings right now, or markup changed")

    return jobs
