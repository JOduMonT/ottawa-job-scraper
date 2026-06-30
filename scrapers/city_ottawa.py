"""
City of Ottawa careers (Avature-based, JS-rendered).
Filters to the "Information Technology jobs" category.

First pass matched on broad URL patterns and picked up navigation links
(language switcher, "View Jobs" menu item, category list links) instead of
actual postings. Real job postings on Avature career sites carry a unique
numeric posting ID in the URL - nav links don't - so we require that as
the matching signal instead.
"""
import re
from .utils import clean_text, make_job
from .browser_utils import get_rendered_html
from bs4 import BeautifulSoup

SOURCE_NAME = "City of Ottawa"
URL = "https://jobs-emplois.ottawa.ca/city-jobs/viewalljobs/?category=Information+Technology+jobs"

WAIT_SELECTOR = "a[href]"

# Matches job detail URLs like .../city-jobs/JobDetail/something/12345
# or any path segment that's purely numeric (the posting ID).
JOB_ID_PATTERN = re.compile(r"/\d{4,}(/|$|\?)")

# Known nav/menu link text to explicitly exclude even if a stray ID matches
EXCLUDE_TITLES = {
    "english (united kingdom)", "français (canada)", "view jobs",
    "apply now", "view job", "learn more", "search/apply for jobs",
    "frequently asked questions", "technical faqs", "working here",
    "why us?", "core behaviours", "leadership competencies", "language",
    "candidate profile", "employee profile", "home",
}


def scrape():
    jobs = []
    try:
        html = get_rendered_html(URL, wait_selector=WAIT_SELECTOR, wait_ms=6000)
    except Exception as e:
        print(f"[{SOURCE_NAME}] browser fetch failed: {e}")
        return jobs

    soup = BeautifulSoup(html, "lxml")
    links = soup.find_all("a", href=True)

    seen_urls = set()
    for link in links:
        href = link["href"]

        if not JOB_ID_PATTERN.search(href):
            continue

        title = clean_text(link.get_text())
        if not title or len(title) < 8:
            continue
        if title.lower() in EXCLUDE_TITLES:
            continue

        if href.startswith("/"):
            href = "https://jobs-emplois.ottawa.ca" + href

        if href in seen_urls:
            continue
        seen_urls.add(href)

        jobs.append(make_job(title=title, url=href, source=SOURCE_NAME))

    if not jobs:
        print(f"[{SOURCE_NAME}] no job links found - page structure may differ from expected, needs live inspection")

    return jobs
