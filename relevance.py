"""
Keyword-weighted relevance scoring - approximates a "good enough fit"
filter without requiring an exact title/resume match.
"""
from config import KEYWORDS, RELEVANCE_THRESHOLD


def score_job(job):
    text = f"{job['title']} {job.get('location', '')}".lower()
    score = 0
    matched = []
    for keyword, weight in KEYWORDS.items():
        if keyword in text:
            score += weight
            matched.append(keyword)
    return score, matched


def is_relevant(job):
    score, _ = score_job(job)
    return score >= RELEVANCE_THRESHOLD


def filter_relevant(jobs):
    relevant = []
    for job in jobs:
        score, matched = score_job(job)
        if score >= RELEVANCE_THRESHOLD:
            job["score"] = score
            job["matched_keywords"] = matched
            relevant.append(job)
    # highest relevance first
    relevant.sort(key=lambda j: j["score"], reverse=True)
    return relevant
