"""
MCP Tool: compute_match_score
Scores resume vs job description.
Formula: Skills 50% | Experience 30% | Keywords 20%
"""

import re
import logging

from mcp.models import ComputeMatchInput
from mcp.utils import cosine_similarity_score

logger = logging.getLogger("mcp.tools.compute_match")


def _skills_score(resume_skills: list[str], job_skills: list[str]) -> tuple[float, list[str]]:
    if not job_skills:
        return 1.0, []
    resume_set = {s.lower() for s in resume_skills}
    job_set = {s.lower() for s in job_skills}
    matched = list(resume_set & job_set)
    score = len(matched) / len(job_set)
    return min(score, 1.0), matched


def _experience_score(resume_exp: str, job_exp: str) -> float:
    """Compare years of experience numerically."""
    def parse_years(text: str) -> int:
        m = re.search(r"(\d+)", text or "")
        return int(m.group(1)) if m else 0

    resume_years = parse_years(resume_exp)
    job_years = parse_years(job_exp)
    if job_years == 0:
        return 1.0
    return min(resume_years / job_years, 1.0)


def _keyword_score(resume_text: str, job_keywords: list[str]) -> float:
    if not job_keywords or not resume_text:
        return 0.0
    text_lower = resume_text.lower()
    hits = sum(1 for kw in job_keywords if kw.lower() in text_lower)
    return min(hits / len(job_keywords), 1.0)


def _rating(score: int) -> str:
    if score >= 80:
        return "Excellent"
    if score >= 60:
        return "Good"
    if score >= 40:
        return "Moderate"
    return "Weak"


def compute_match_score(inp: ComputeMatchInput) -> dict:
    resume = inp.resume_data
    job = inp.job_data

    skills_s, matched = _skills_score(
        resume.get("skills", []), job.get("skills", [])
    )
    exp_s = _experience_score(
        resume.get("experience", ""), job.get("experience_required", "")
    )
    kw_s = _keyword_score(
        resume.get("resume_text", ""), job.get("keywords", [])
    )

    # Weighted total
    total = (skills_s * 50) + (exp_s * 30) + (kw_s * 20)
    score = round(total)

    logger.info("Match score: %d (skills=%.2f, exp=%.2f, kw=%.2f)", score, skills_s, exp_s, kw_s)

    return {
        "score": score,
        "rating": _rating(score),
        "matched_skills": matched,
        "breakdown": {
            "skills_score": round(skills_s * 50, 1),
            "experience_score": round(exp_s * 30, 1),
            "keyword_score": round(kw_s * 20, 1),
        },
    }
