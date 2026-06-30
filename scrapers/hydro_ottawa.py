"""
Hydro Ottawa careers (Workday-based, JS-rendered).

NOTE: Workday sites are notoriously selector-heavy and change per-tenant.
This targets the standard Workday job posting list structure
(data-automation-id attributes are Workday's own testing hooks and tend
to be more stable than CSS classes - prefer those if you need to adjust this).
"""
from .utils import clean_text, make_job
from .browser_utils import get_rendered_html
from bs4 import BeautifulSoup

SOURCE_NAME = "Hydro Ottawa"
URL = "https://hydroottawa.wd3.myworkdayjobs.com/hydro_ottawa_careersite"

SELECTOR_CARD = "li[class*='css'] a[data-automation-id='jobTitle']"


def scrape():
    jobs = []
    try:
        html = get_rendered_html(URL, wait_selector="a[data-automation-id='jobTitle']", scroll=True)
    except Exception as e:
        print(f"[{SOURCE_NAME}] browser fetch failed: {e}")
        return jobs

    soup = BeautifulSoup(html, "lxml")
    links = soup.select("a[data-automation-id='jobTitle']")

    if not links:
        print(f"[{SOURCE_NAME}] no job links found - selectors likely need updating")
        return jobs

    for link in links:
        title = clean_text(link.get_text())
        href = link.get("href", "")
        if not title or not href:
            continue
        if href.startswith("/"):
            href = "https://hydroottawa.wd3.myworkdayjobs.com" + href
        jobs.append(make_job(title=title, url=href, source=SOURCE_NAME))

    return jobs
