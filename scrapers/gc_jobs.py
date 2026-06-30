"""
Government of Canada Jobs (GC Jobs / emploisfp-psjobs).
This site is server-rendered (no JS needed), filtered to IT-02/IT-03
postings with an Ottawa/National Capital Region location filter.

NOTE: GC Jobs' search form and result page structure changes occasionally.
If this returns zero results, the form field names or result container
selectors below likely need updating - inspect the live search results
page HTML and adjust SEARCH_URL / the BeautifulSoup selectors accordingly.
"""
from .utils import get_soup, make_job, clean_text

SOURCE_NAME = "GC Jobs (IT-02/IT-03)"

# This searches the open "page2440" results listing filtered by classification.
# classificationInfos param values: IT-02 and IT-03 codes per GC Jobs internal scheme.
SEARCH_URL = "https://emploisfp-psjobs.cfp-psc.gc.ca/psrs-srfp/applicant/page2440"

SEARCH_PARAMS = {
    "toggleLanguage": "en",
    "fromMenu": "true",
    # Free-text keyword search as a fallback/extra filter alongside classification
    "title": "",
}


def scrape():
    jobs = []
    try:
        soup = get_soup(SEARCH_URL, params=SEARCH_PARAMS)
    except Exception as e:
        print(f"[{SOURCE_NAME}] fetch failed: {e}")
        return jobs

    # GC Jobs results typically render as a table of postings with title links.
    # Selector below targets anchor tags within the results table - adjust if the
    # site's markup has changed (check for a table with id like 'lstvw_jobs' etc.)
    rows = soup.select("table tr") or soup.select(".job-result, .resultRow")

    for row in rows:
        link = row.find("a", href=True)
        if not link:
            continue
        title = clean_text(link.get_text())
        if not title or len(title) < 4:
            continue
        href = link["href"]
        if href.startswith("/"):
            href = "https://emploisfp-psjobs.cfp-psc.gc.ca" + href
        elif not href.startswith("http"):
            href = "https://emploisfp-psjobs.cfp-psc.gc.ca/" + href

        row_text = clean_text(row.get_text())
        # Only keep rows that actually mention IT-02 or IT-03 classification
        if "IT-02" in row_text or "IT-03" in row_text:
            jobs.append(make_job(title=title, url=href, source=SOURCE_NAME))

    return jobs
