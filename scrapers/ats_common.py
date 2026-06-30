"""
Reusable scrapers for common ATS (Applicant Tracking System) platforms.

Several of the target companies use standard ATS platforms that expose
clean JSON APIs - far more reliable than HTML scraping. This module provides
generic functions each company-specific scraper can call with its own slug.

Platforms covered:
- Lever      (jobs.lever.co)      -> public JSON API at api.lever.co
- Greenhouse (boards.greenhouse.io) -> public JSON API at boards-api.greenhouse.io
- iCIMS      (careers-X.icims.com) -> HTML, needs careful parsing (no clean public API)
"""
from .utils import get_json, make_job, clean_text


def scrape_lever(company_slug, source_name, location_filter=None):
    """
    Lever's public API: https://api.lever.co/v0/postings/<slug>?mode=json
    Returns a clean list of postings. location_filter (list of lowercase
    strings) optionally restricts to matching locations.
    """
    jobs = []
    url = f"https://api.lever.co/v0/postings/{company_slug}?mode=json"
    try:
        data = get_json(url)
    except Exception as e:
        print(f"[{source_name}] Lever API fetch failed: {e}")
        return jobs

    for posting in data:
        title = clean_text(posting.get("text", ""))
        href = posting.get("hostedUrl", "")
        location = ""
        categories = posting.get("categories", {})
        if categories:
            location = clean_text(categories.get("location", ""))

        if not title or not href:
            continue

        if location_filter:
            loc_lower = location.lower()
            if not any(f in loc_lower for f in location_filter):
                continue

        jobs.append(make_job(title=title, url=href, source=source_name,
                             location=location or "See posting"))
    return jobs


def scrape_greenhouse(company_slug, source_name, location_filter=None):
    """
    Greenhouse public API:
    https://boards-api.greenhouse.io/v1/boards/<slug>/jobs
    """
    jobs = []
    url = f"https://boards-api.greenhouse.io/v1/boards/{company_slug}/jobs"
    try:
        data = get_json(url)
    except Exception as e:
        print(f"[{source_name}] Greenhouse API fetch failed: {e}")
        return jobs

    for posting in data.get("jobs", []):
        title = clean_text(posting.get("title", ""))
        href = posting.get("absolute_url", "")
        location = clean_text(posting.get("location", {}).get("name", ""))

        if not title or not href:
            continue

        if location_filter:
            loc_lower = location.lower()
            if not any(f in loc_lower for f in location_filter):
                continue

        jobs.append(make_job(title=title, url=href, source=source_name,
                             location=location or "See posting"))
    return jobs


# Common Canadian/Ottawa location filters reused across sources
OTTAWA_LOCATION_FILTER = ["ottawa", "gatineau", "kanata", "remote", "canada", "ontario"]
