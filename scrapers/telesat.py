"""
Telesat careers - hosted on Lever (jobs.lever.co/telesat).
Uses Lever's clean public JSON API. Telesat is Ottawa-HQ'd so most
postings are Ottawa-based; we still apply a light location filter to
drop any non-Canadian roles.

Note: Telesat skews heavily toward senior/satellite-systems engineering
roles, so the seniority filter will exclude many of these - expect a
lower hit rate here.
"""
from .ats_common import scrape_lever, OTTAWA_LOCATION_FILTER

SOURCE_NAME = "Telesat"


def scrape():
    return scrape_lever("telesat", SOURCE_NAME, location_filter=OTTAWA_LOCATION_FILTER)
