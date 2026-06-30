"""
Foci Solutions careers - hosted on BambooHR (foci.bamboohr.com).
Uses BambooHR's clean public jobs feed. Ottawa-based software consultancy
that explicitly hires C#/.NET developers for government clients - one of
the strongest stylistic fits for your background.
"""
from .ats_common import scrape_bamboohr, OTTAWA_LOCATION_FILTER

SOURCE_NAME = "Foci Solutions"


def scrape():
    # Foci is Ottawa-based; most roles are Ottawa/remote-Canada. Apply the
    # standard location filter (empty-location postings are kept by the helper).
    return scrape_bamboohr("foci", SOURCE_NAME, location_filter=OTTAWA_LOCATION_FILTER)
