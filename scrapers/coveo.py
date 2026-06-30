"""
Coveo careers - hosted on Greenhouse (job-boards.greenhouse.io/coveoen).
Uses Greenhouse's clean public JSON API. AI/search SaaS company with major
Quebec City + Montreal presence and Canada-wide remote roles; Glassdoor
reports Software Developer median around $90K - squarely in target range.

Coveo has offices across Canada and many remote-Canada roles. We apply a
Canada/Ottawa/remote location filter to keep relevant postings.
"""
from .ats_common import scrape_greenhouse, OTTAWA_LOCATION_FILTER

SOURCE_NAME = "Coveo"


def scrape():
    return scrape_greenhouse("coveoen", SOURCE_NAME, location_filter=OTTAWA_LOCATION_FILTER)
