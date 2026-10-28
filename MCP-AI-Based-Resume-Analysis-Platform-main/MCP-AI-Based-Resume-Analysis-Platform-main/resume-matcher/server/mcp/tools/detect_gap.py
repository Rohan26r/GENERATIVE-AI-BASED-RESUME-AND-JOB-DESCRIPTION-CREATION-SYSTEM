"""
MCP Tool: detect_skill_gap
Identifies missing skills and recommends learning resources.
"""

import logging

from mcp.models import DetectGapInput

logger = logging.getLogger("mcp.tools.detect_gap")

# Simple curated learning map
LEARNING_MAP: dict[str, str] = {
    "python": "https://docs.python.org/3/tutorial/",
    "machine learning": "https://www.coursera.org/learn/machine-learning",
    "deep learning": "https://www.deeplearning.ai/",
    "docker": "https://docs.docker.com/get-started/",
    "kubernetes": "https://kubernetes.io/docs/tutorials/",
    "aws": "https://aws.amazon.com/training/",
    "react": "https://react.dev/learn",
    "typescript": "https://www.typescriptlang.org/docs/",
    "sql": "https://www.w3schools.com/sql/",
    "git": "https://git-scm.com/doc",
    "fastapi": "https://fastapi.tiangolo.com/tutorial/",
    "spark": "https://spark.apache.org/docs/latest/",
    "tensorflow": "https://www.tensorflow.org/tutorials",
    "pytorch": "https://pytorch.org/tutorials/",
}


def detect_skill_gap(inp: DetectGapInput) -> dict:
    resume_set = {s.lower() for s in inp.resume_skills}
    job_set = {s.lower() for s in inp.job_skills}

    missing = list(job_set - resume_set)

    recommended = []
    for skill in missing:
        url = LEARNING_MAP.get(skill)
        recommended.append({
            "skill": skill,
            "resource": url or f"Search: 'learn {skill}' on Coursera / Udemy",
        })

    logger.info("Skill gap detected: %d missing skills", len(missing))

    return {
        "missing_skills": missing,
        "recommended_learning": recommended,
    }
