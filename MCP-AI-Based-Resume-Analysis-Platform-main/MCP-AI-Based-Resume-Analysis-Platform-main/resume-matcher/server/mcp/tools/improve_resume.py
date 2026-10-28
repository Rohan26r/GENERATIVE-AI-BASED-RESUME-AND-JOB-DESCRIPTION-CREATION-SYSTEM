"""
MCP Tool: improve_resume
Generates improved resume sections based on job description.
Uses rule-based enhancement (LLM-ready placeholder architecture).
"""

import re
import logging

from mcp.models import ImproveResumeInput
from mcp.utils import extract_skills_from_text, extract_keywords

logger = logging.getLogger("mcp.tools.improve_resume")


def _improve_summary(resume_text: str, job_description: str) -> str:
    """
    Generate an improved professional summary.
    Plug in an LLM call here (OpenAI, Bedrock, etc.) for production.
    """
    job_keywords = extract_keywords(job_description)[:5]
    skills = extract_skills_from_text(resume_text)[:4]

    keyword_str = ", ".join(job_keywords)
    skill_str = ", ".join(skills) if skills else "relevant technologies"

    return (
        f"Results-driven professional with hands-on experience in {skill_str}. "
        f"Proven ability to deliver impactful solutions aligned with {keyword_str}. "
        "Passionate about continuous learning and contributing to high-performing teams."
    )


def _improve_experience(resume_text: str) -> list[str]:
    """
    Extract experience bullet points and rewrite them with action verbs.
    LLM-ready: replace this with an LLM prompt for richer output.
    """
    lines = [l.strip() for l in resume_text.splitlines() if len(l.strip()) > 40]
    improved = []
    action_verbs = ["Developed", "Implemented", "Optimized", "Led", "Designed", "Delivered"]

    for i, line in enumerate(lines[:5]):
        verb = action_verbs[i % len(action_verbs)]
        # Strip leading bullets/dashes
        clean = re.sub(r"^[-•*]\s*", "", line)
        improved.append(f"{verb} {clean[0].lower()}{clean[1:]}" if clean else line)

    return improved or ["Add quantified achievements to each role."]


def _improve_skills(resume_text: str, job_description: str) -> list[str]:
    """Merge resume skills with job-required skills for a complete skills section."""
    resume_skills = set(extract_skills_from_text(resume_text))
    job_skills = set(extract_skills_from_text(job_description))
    combined = resume_skills | job_skills
    return sorted(combined)


def improve_resume(inp: ImproveResumeInput) -> dict:
    return {
        "improved_summary": _improve_summary(inp.resume_text, inp.job_description),
        "improved_experience": _improve_experience(inp.resume_text),
        "improved_skills": _improve_skills(inp.resume_text, inp.job_description),
    }
