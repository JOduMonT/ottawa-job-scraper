"""
City of Ottawa careers (SuccessFactors-based career site).
Filters to the "Information Technology jobs" category.

CORRECTED: the previous URL (.../viewalljobs/?category=...) only shows a
category MENU page, not actual postings - that's why nav links like
"Cybersecurity" and "OC Transpo" were being scraped instead of real jobs.
The actual category listing page is at a different URL pattern
(.../city-jobs/go/<Category-Name>/<id>/), confirmed via live inspection.

Also confirmed this page is plain server-rendered HTML - no JS/Playwright
needed, which makes this faster and more reliable than the browser-based
approach used for Hydro Ottawa/CGI.
"""
import re
from .utils import get_soup, clean_text, make_job

SOURCE_NAME = "City of Ottawa"
URL = "https://jobs-emplois.ottawa.ca/city-jobs/go/Information-Technology-jobs/8649547/"

# Real job posting URLs look like: /city-jobs/job/<slug>/<numeric-id>/
JOB_URL_PATTERN = re.compile(r"/city-jobs/job/")


def scrape():
    jobs = []
    try:
        soup = get_soup(URL)
    except Exception as e:
        print(f"[{SOURCE_NAME}] fetch failed: {e}")
        return jobs

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
