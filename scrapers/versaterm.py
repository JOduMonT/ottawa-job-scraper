"""
Versaterm careers - hosted on Greenhouse (job-boards.greenhouse.io/versaterm).
Uses Greenhouse's clean public JSON API. Ottawa-HQ'd public safety software
company; good stylistic fit given government/legislative systems background.
"""
from .ats_common import scrape_greenhouse, OTTAWA_LOCATION_FILTER

SOURCE_NAME = "Versaterm"


def scrape():
    # Versaterm has remote/Ottawa roles; apply Canada/Ottawa location filter
    return scrape_greenhouse("versaterm", SOURCE_NAME, location_filter=OTTAWA_LOCATION_FILTER)
