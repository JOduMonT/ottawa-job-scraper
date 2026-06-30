"""
Sends the daily job digest via the SendGrid API (plain requests call,
no SDK dependency needed).

The email shows ALL current matching postings (grouped by source/category),
visually flags which ones are new since the last run, and the subject line
counts only the new ones.
"""
import os
import requests
from datetime import date
from collections import defaultdict


SENDGRID_URL = "https://api.sendgrid.com/v3/mail/send"


def build_html(jobs_by_tier, new_count):
    today = date.today().strftime("%B %d, %Y")
    html = [f"<h2>Ottawa Job Digest - {today}</h2>"]

    total = sum(len(v) for v in jobs_by_tier.values())
    if total == 0:
        html.append("<p>No matching postings currently open.</p>")
        return "\n".join(html)

    html.append(
        f"<p style='color:#555'>{new_count} new since last digest &middot; "
        f"{total} total matching postings currently open</p>"
    )

    for tier_name, jobs in jobs_by_tier.items():
        if not jobs:
            continue
        html.append(f"<h3 style='margin-bottom:4px'>{tier_name}</h3>")

        # group postings by source (acts as the "category" within a tier)
        by_source = defaultdict(list)
        for job in jobs:
            by_source[job["source"]].append(job)

        for source in sorted(by_source.keys()):
            source_jobs = by_source[source]
            new_in_source = sum(1 for j in source_jobs if j.get("is_new"))
            label = f"{source} ({len(source_jobs)})"
            if new_in_source:
                label += f" &mdash; {new_in_source} new"
            html.append(f"<h4 style='margin:10px 0 4px 0;color:#333'>{label}</h4>")
            html.append("<ul style='margin-top:0'>")

            # new postings first within each source
            source_jobs.sort(key=lambda j: not j.get("is_new"))
            for job in source_jobs:
                badge = ""
                if job.get("is_new"):
                    badge = (" <span style='background:#c0392b;color:#fff;"
                             "font-size:11px;padding:1px 6px;border-radius:3px;"
                             "margin-left:6px'>NEW</span>")
                html.append(
                    f"<li><a href='{job['url']}'>{job['title']}</a>{badge}</li>"
                )
            html.append("</ul>")

    return "\n".join(html)


def send_digest(jobs_by_tier, new_count=0):
    api_key = os.environ["SENDGRID_API_KEY"]
    to_email = os.environ["EMAIL_TO"]
    from_email = os.environ.get("EMAIL_FROM", to_email)  # must be SendGrid-verified

    total = sum(len(v) for v in jobs_by_tier.values())

    if total == 0:
        subject = "Ottawa Job Digest - no matching postings open"
    elif new_count == 0:
        subject = "Ottawa Job Digest - no new postings today"
    else:
        subject = f"Ottawa Job Digest - {new_count} new posting(s)"

    payload = {
        "personalizations": [{"to": [{"email": to_email}]}],
        "from": {"email": from_email},
        "subject": subject,
        "content": [{"type": "text/html", "value": build_html(jobs_by_tier, new_count)}],
    }

    resp = requests.post(
        SENDGRID_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=20,
    )

    if resp.status_code >= 300:
        print(f"SendGrid error {resp.status_code}: {resp.text}")
        resp.raise_for_status()
    else:
        print(f"Email sent successfully ({new_count} new, {total} total shown).")
