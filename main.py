"""
Entry point - run by GitHub Actions every morning.
Scrapes all active sources, filters for relevance, dedups against
previous runs, and emails the digest via SendGrid.
"""
from scrapers import ACTIVE_SCRAPERS
from relevance import filter_relevant
from dedup import filter_new
from emailer import send_digest

# Sources considered "secondary tier" - broader telecom/hardware companies
# with a lower expected hit rate for your specific background. Shown
# separately in the email so they don't dilute the primary list.
SECONDARY_TIER_SOURCES = {"Nokia", "BlackBerry", "QNX", "Ciena", "Ericsson"}


def run():
    all_jobs = []

    for scraper in ACTIVE_SCRAPERS:
        source_name = getattr(scraper, "SOURCE_NAME", scraper.__name__)
        try:
            jobs = scraper.scrape()
            print(f"[{source_name}] found {len(jobs)} raw postings")
            if jobs:
                sample_titles = [j["title"] for j in jobs[:5]]
                print(f"[{source_name}] sample titles: {sample_titles}")
            all_jobs.extend(jobs)
        except Exception as e:
            # one broken scraper should never take down the whole run
            print(f"[{source_name}] scraper crashed: {e}")

    relevant = filter_relevant(all_jobs)
    print(f"{len(relevant)} postings passed the relevance filter")

    new_jobs = filter_new(relevant)
    print(f"{len(new_jobs)} are new since the last run")

    jobs_by_tier = {"Primary": [], "Secondary (broader fit)": []}
    for job in new_jobs:
        if job["source"] in SECONDARY_TIER_SOURCES:
            jobs_by_tier["Secondary (broader fit)"].append(job)
        else:
            jobs_by_tier["Primary"].append(job)

    send_digest(jobs_by_tier)


if __name__ == "__main__":
    run()
