"""
Registry of active scrapers. Add new entries here as we expand to the
full 20-source list. Each module must expose a scrape() function that
returns a list of job dicts (see utils.make_job).
"""
from . import gc_jobs
from . import city_ottawa
from . import hydro_ottawa
from . import cgi

ACTIVE_SCRAPERS = [
    gc_jobs,
    city_ottawa,
    hydro_ottawa,
    cgi,
]
