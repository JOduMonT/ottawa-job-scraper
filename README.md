# Ottawa Job Scraper

Scrapes 4 sources (first batch) every morning, filters for relevance, and emails a digest via SendGrid.

## Sources in this first batch

- GC Jobs (IT-02/IT-03 only) - simple HTML, no browser needed
- City of Ottawa - JS-rendered (Avature), uses Playwright
- Hydro Ottawa - JS-rendered (Workday), uses Playwright
- CGI - server-rendered (njoyn ATS)

## One-time setup

1. Add these repo secrets (Settings → Secrets and variables → Actions):
   - `SENDGRID_API_KEY` - your SendGrid API key
   - `EMAIL_TO` - the email address you want the digest sent to
   - `EMAIL_FROM` - **must be a SendGrid-verified sender** (Settings → Sender Authentication in SendGrid). Can be the same as EMAIL_TO if you verify your own address.

2. Push these files to your `ottawa-job-scraper` repo, keeping the folder structure as-is.

3. The workflow runs daily at 11:00 UTC (~7am Eastern). You can also trigger it manually any time from the repo's **Actions** tab → "Daily Job Scraper" → **Run workflow** - use this to test without waiting for tomorrow morning.

## Important: this needs a live test pass

I wrote the scrapers based on inspecting each site's structure, but I could not render JavaScript-heavy pages in my own sandbox to verify the exact CSS selectors. **Expect City of Ottawa, Hydro Ottawa, and possibly CGI to need selector adjustments after the first run.**

How to debug a scraper that returns 0 results:
1. Go to the Actions tab → click the latest run → expand "Run scraper and send email"
2. Look for a line like `[City of Ottawa] no job cards found - selectors likely need updating`
3. Open the source URL in a real browser, right-click a job listing → Inspect
4. Find the actual CSS class/structure wrapping each job title and send it to me - I'll update the selector

This is normal for the first pass on any scraper - career sites don't expose clean APIs, so we're reverse-engineering their HTML. Once each one is confirmed working, it should keep working until the company redesigns their careers page (which happens occasionally - if a source silently goes to 0 results after weeks of working, that's the signal to check it again).

## Adding the rest of the 20 sources

Once this batch is confirmed working end-to-end, we'll add: Bank of Canada, NRC, EDC, Canada Post, CMHC, Nav Canada, Versaterm, Kinaxis, Calian Group, Mitel/Ribbon, BDO Canada, Telesat, Nokia, BlackBerry/QNX, Ciena, Ericsson - following the same pattern (new file in `scrapers/`, registered in `scrapers/__init__.py`).

## Adjusting relevance filtering

Edit `config.py` - `KEYWORDS` dict controls keyword weights, `RELEVANCE_THRESHOLD` controls how many points a posting needs to clear the bar.
