"""
Sends the daily job digest via the SendGrid API (plain requests call,
no SDK dependency needed).
"""
import os
import requests
from datetime import date

SENDGRID_URL = "https://api.sendgrid.com/v3/mail/send"


def build_html(jobs_by_tier):
    """jobs_by_tier: dict like {'Primary': [...], 'Secondary': [...]}"""
    today = date.today().strftime("%B %d, %Y")
    html = [f"<h2>Ottawa Job Digest - {today}</h2>"]

    for tier_name, jobs in jobs_by_tier.items():
        if not jobs:
            continue
        html.append(f"<h3>{tier_name}</h3>")
        html.append("<ul>")
        for job in jobs:
            title = job["title"]
            url = job["url"]
            source = job["source"]
            html.append(
                f"<li><a href='{url}'>{title}</a> — <i>{source}</i></li>"
            )
        html.append("</ul>")

    if not any(jobs_by_tier.values()):
        html.append("<p>No new matching postings today.</p>")

    return "\n".join(html)


def send_digest(jobs_by_tier):
    api_key = os.environ["SENDGRID_API_KEY"]
    to_email = os.environ["EMAIL_TO"]
    from_email = os.environ.get("EMAIL_FROM", to_email)  # must be SendGrid-verified

    total = sum(len(v) for v in jobs_by_tier.values())
    if total == 0:
        subject = "Ottawa Job Digest - no new matches today"
    else:
        subject = f"Ottawa Job Digest - {total} new posting(s)"

    payload = {
        "personalizations": [{"to": [{"email": to_email}]}],
        "from": {"email": from_email},
        "subject": subject,
        "content": [{"type": "text/html", "value": build_html(jobs_by_tier)}],
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
        print(f"Email sent successfully ({total} new postings).")
