"""
City of Ottawa careers (Avature-based, JS-rendered).
Filters to the "Information Technology jobs" category.

NOTE: This is a best-effort selector set written without being able to
render the live JS in dev. After the first GitHub Actions run, check the
workflow logs - if zero jobs come back, open the URL below in a real
browser, inspect the job card elements, and update SELECTOR_* below.
"""
from .utils import clean_text, make_job
from .browser_utils import get_rendered_html
from bs4 import BeautifulSoup

SOURCE_NAME = "City of Ottawa"
URL = "https://jobs-emplois.ottawa.ca/city-jobs/viewalljobs/?category=Information+Technology+jobs"

# Avature career sites commonly use job-tile classes like these.
# Update if inspection of the live page shows different class names.
SELECTOR_CARD = "div.jobList__item, li.job-tile, div[class*='jobResult']"
SELECTOR_TITLE = "a"


def scrape():
    jobs = []
    try:
        html = get_rendered_html(URL, wait_selector=SELECTOR_CARD)
    except Exception as e:
        print(f"[{SOURCE_NAME}] browser fetch failed: {e}")
        return jobs

    soup = BeautifulSoup(html, "lxml")
    cards = soup.select(SELECTOR_CARD)

    if not cards:
        print(f"[{SOURCE_NAME}] no job cards found - selectors likely need updating")
        return jobs

    for card in cards:
        link = card.select_one(SELECTOR_TITLE)
        if not link or not link.get("href"):
            continue
        title = clean_text(link.get_text())
        if not title:
            continue
        href = link["href"]
        if href.startswith("/"):
            href = "https://jobs-emplois.ottawa.ca" + href
        jobs.append(make_job(title=title, url=href, source=SOURCE_NAME))

    return jobs
