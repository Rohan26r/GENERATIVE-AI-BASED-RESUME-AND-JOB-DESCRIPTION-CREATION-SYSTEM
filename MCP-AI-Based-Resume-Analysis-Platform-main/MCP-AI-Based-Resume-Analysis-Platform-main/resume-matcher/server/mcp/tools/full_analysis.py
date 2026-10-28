"""
MCP Tool: run_full_analysis
Pipeline tool — runs all 7 tools in sequence and returns a unified report.
"""

import logging

from mcp.models import FullAnalysisInput
from mcp.registry import execute_tool

logger = logging.getLogger("mcp.tools.full_analysis")


def run_full_analysis(inp: FullAnalysisInput) -> dict:
    report: dict = {}

    # Step 1: Parse resume
    r1 = execute_tool("parse_resume", {"file_path": inp.file_path})
    if not r1.success:
        raise RuntimeError(f"parse_resume failed: {r1.error}")
    resume_data: dict = r1.data
    report["resume"] = resume_data

    # Step 2: Analyze job description
    r2 = execute_tool("analyze_job_description", {"job_description": inp.job_description})
    if not r2.success:
        raise RuntimeError(f"analyze_job_description failed: {r2.error}")
    job_data: dict = r2.data
    report["job"] = job_data

    # Step 3: Compute match score
    r3 = execute_tool("compute_match_score", {
        "resume_data": resume_data,
        "job_data": job_data,
    })
    if not r3.success:
        raise RuntimeError(f"compute_match_score failed: {r3.error}")
    report["match"] = r3.data

    # Step 4: Detect skill gap
    r4 = execute_tool("detect_skill_gap", {
        "resume_skills": resume_data.get("skills", []),
        "job_skills": job_data.get("skills", []),
    })
    if not r4.success:
        raise RuntimeError(f"detect_skill_gap failed: {r4.error}")
    report["gap"] = r4.data

    # Step 5: ATS check
    r5 = execute_tool("ats_checker", {
        "resume_text": resume_data.get("resume_text", ""),
        "job_keywords": job_data.get("keywords", []),
    })
    if not r5.success:
        raise RuntimeError(f"ats_checker failed: {r5.error}")
    report["ats"] = r5.data

    # Step 6: Improve resume
    r6 = execute_tool("improve_resume", {
        "resume_text": resume_data.get("resume_text", ""),
        "job_description": inp.job_description,
    })
    if not r6.success:
        raise RuntimeError(f"improve_resume failed: {r6.error}")
    report["improvements"] = r6.data

    # Step 7: Save history
    r7 = execute_tool("save_history", {"uid": inp.uid, "report": report})
    if not r7.success:
        logger.warning("save_history failed (non-fatal): %s", r7.error)
    else:
        report["report_id"] = r7.data.get("report_id")

    logger.info("Full analysis complete for uid=%s", inp.uid)
    return report
