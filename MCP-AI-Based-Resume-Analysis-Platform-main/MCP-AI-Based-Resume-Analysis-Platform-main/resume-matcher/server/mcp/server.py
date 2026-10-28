"""
MCP Server Bootstrap
--------------------
Loads and registers all tools into the registry at startup.
"""

import logging

from mcp.registry import register_tool
from mcp.models import (
    ParseResumeInput, AnalyzeJobInput, ComputeMatchInput,
    DetectGapInput, ATSCheckerInput, ImproveResumeInput,
    SaveHistoryInput, FullAnalysisInput,
    SupervisorInput, RecruiterAgentInput, ATSAgentInput,
    CoachAgentInput, InterviewAgentInput, ReportAgentInput,
)

logger = logging.getLogger("mcp.server")


def load_tools() -> None:
    """Import tool functions and register them with their schemas."""
    from mcp.tools.parse_resume import parse_resume
    from mcp.tools.analyze_job import analyze_job_description
    from mcp.tools.compute_match import compute_match_score
    from mcp.tools.detect_gap import detect_skill_gap
    from mcp.tools.ats_checker import ats_checker
    from mcp.tools.improve_resume import improve_resume
    from mcp.tools.save_history import save_history
    from mcp.tools.full_analysis import run_full_analysis

    register_tool("parse_resume", parse_resume, ParseResumeInput)
    register_tool("analyze_job_description", analyze_job_description, AnalyzeJobInput)
    register_tool("compute_match_score", compute_match_score, ComputeMatchInput)
    register_tool("detect_skill_gap", detect_skill_gap, DetectGapInput)
    register_tool("ats_checker", ats_checker, ATSCheckerInput)
    register_tool("improve_resume", improve_resume, ImproveResumeInput)
    register_tool("save_history", save_history, SaveHistoryInput)
    register_tool("run_full_analysis", run_full_analysis, FullAnalysisInput)

    # ── Agent tools ───────────────────────────────────────────────────────────
    from mcp.tools.agent_tools import (
        run_supervisor_agent, run_recruiter_agent, run_ats_agent,
        run_coach_agent, run_interview_agent, generate_final_agent_report,
    )
    register_tool("run_supervisor_agent", run_supervisor_agent, SupervisorInput)
    register_tool("run_recruiter_agent", run_recruiter_agent, RecruiterAgentInput)
    register_tool("run_ats_agent", run_ats_agent, ATSAgentInput)
    register_tool("run_coach_agent", run_coach_agent, CoachAgentInput)
    register_tool("run_interview_agent", run_interview_agent, InterviewAgentInput)
    register_tool("generate_final_agent_report", generate_final_agent_report, ReportAgentInput)

    logger.info("All MCP tools loaded (8 core + 6 agent).")
