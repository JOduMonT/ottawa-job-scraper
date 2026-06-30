"""
CGI Canada careers, hosted on the njoyn ATS platform (cgi.njoyn.com).
This is an older server-rendered platform (classic ASP-style), so plain
requests + BeautifulSoup should work without a headless browser.

NOTE: njoyn search requires a location/keyword query - adjust SEARCH_PARAMS
if results come back empty or unfiltered. Check the live search URL's
querystring in your browser if the site's search form changes.
"""
from .utils import get_soup, make_job, clean_text

SOURCE_NAME = "CGI"
URL = "https://cgi.njoyn.com/CGI/xweb/xweb.asp"

SEARCH_PARAMS = {
    "page": "joblisting",
    "CLID": "21001",
    "CountryID": "CA",
    "keywords": "developer OR software OR .NET OR C# OR programmer",
    "location": "Ottawa",
}


def scrape():
    jobs = []
    try:
        soup = get_soup(URL, params=SEARCH_PARAMS)
    except Exception as e:
        print(f"[{SOURCE_NAME}] fetch failed: {e}")
        return jobs

    # njoyn job listing rows are typically table rows or list items with a
    # title link - adjust selector if the live markup differs.
    rows = soup.select("table tr") or soup.select(".jobListItem, .job-listing-row")

    for row in rows:
        link = row.find("a", href=True)
        if not link:
            continue
        title = clean_text(link.get_text())
        if not title or len(title) < 4:
            continue
        href = link["href"]
        if href.startswith("xweb.asp") or not href.startswith("http"):
            href = "https://cgi.njoyn.com/CGI/xweb/" + href.lstrip("/")
        jobs.append(make_job(title=title, url=href, source=SOURCE_NAME))

    return jobs
