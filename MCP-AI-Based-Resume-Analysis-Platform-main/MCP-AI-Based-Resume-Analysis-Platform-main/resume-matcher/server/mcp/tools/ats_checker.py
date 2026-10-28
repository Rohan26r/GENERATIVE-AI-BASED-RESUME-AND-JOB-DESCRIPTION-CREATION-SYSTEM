"""
MCP Tool: ats_checker
Checks resume for ATS (Applicant Tracking System) compatibility.
"""

import re
import logging

from mcp.models import ATSCheckerInput

logger = logging.getLogger("mcp.tools.ats_checker")

# Headings that ATS systems expect
EXPECTED_HEADINGS = {"experience", "education", "skills", "summary", "objective", "certifications"}

# Patterns that suggest tables or images (ATS unfriendly)
TABLE_PATTERNS = [r"\|.*\|", r"─{3,}", r"={3,}"]


def _check_missing_keywords(text: str, keywords: list[str]) -> list[str]:
    text_lower = text.lower()
    return [kw for kw in keywords if kw.lower() not in text_lower]


def _check_missing_sections(text: str) -> list[str]:
    text_lower = text.lower()
    return [h for h in EXPECTED_HEADINGS if h not in text_lower]


def _check_weak_headings(text: str) -> bool:
    """Returns True if no standard headings found."""
    text_lower = text.lower()
    return not any(h in text_lower for h in EXPECTED_HEADINGS)


def _check_too_short(text: str) -> bool:
    return len(text.split()) < 200


def _check_table_or_image(text: str) -> bool:
    return any(re.search(p, text) for p in TABLE_PATTERNS)


def ats_checker(inp: ATSCheckerInput) -> dict:
    text = inp.resume_text
    keywords = inp.job_keywords

    issues: list[str] = []
    recommendations: list[str] = []

    # 1. Missing keywords
    missing_kw = _check_missing_keywords(text, keywords)
    if missing_kw:
        issues.append(f"Missing {len(missing_kw)} job keywords: {', '.join(missing_kw[:5])}...")
        recommendations.append("Add these keywords naturally into your experience/skills sections.")

    # 2. Missing sections
    missing_sections = _check_missing_sections(text)
    if missing_sections:
        issues.append(f"Missing sections: {', '.join(missing_sections)}")
        recommendations.append(f"Add clearly labeled sections: {', '.join(missing_sections)}")

    # 3. Weak headings
    if _check_weak_headings(text):
        issues.append("No standard section headings detected.")
        recommendations.append("Use clear headings: Experience, Education, Skills, Summary.")

    # 4. Too short
    if _check_too_short(text):
        issues.append("Resume is too short (under 200 words).")
        recommendations.append("Expand your resume with more detail about your experience.")

    # 5. Table/image indicators
    if _check_table_or_image(text):
        issues.append("Possible table or special formatting detected — ATS may misread this.")
        recommendations.append("Use plain text formatting without tables or columns.")

    # Score: start at 100, deduct per issue
    deduction = len(issues) * 12
    ats_score = max(0, 100 - deduction)

    logger.info("ATS score: %d, issues: %d", ats_score, len(issues))

    return {
        "ats_score": ats_score,
        "issues": issues,
        "recommendations": recommendations,
    }
