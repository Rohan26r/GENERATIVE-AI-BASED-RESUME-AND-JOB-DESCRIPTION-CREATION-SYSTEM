"""
MCP Tool: analyze_job_description
Extracts role, required skills, experience, and keywords from a job posting.
"""

import re
import logging

from mcp.models import AnalyzeJobInput
from mcp.utils import extract_skills_from_text, extract_keywords

logger = logging.getLogger("mcp.tools.analyze_job")


def _extract_role(text: str) -> str:
    """Try to find job title from common patterns."""
    patterns = [
        r"(?:job title|position|role)[:\s]+([^\n]+)",
        r"^([^\n]{5,60})",  # fallback: first line
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            return match.group(1).strip()
    return "Not specified"


def _extract_experience_required(text: str) -> str:
    match = re.search(r"(\d+)\+?\s*years?\s*(of\s*)?experience", text, re.IGNORECASE)
    if match:
        return f"{match.group(1)}+ years"
    return "Not specified"


def analyze_job_description(inp: AnalyzeJobInput) -> dict:
    text = inp.job_description

    return {
        "role": _extract_role(text),
        "skills": extract_skills_from_text(text),
        "experience_required": _extract_experience_required(text),
        "keywords": extract_keywords(text),
    }
