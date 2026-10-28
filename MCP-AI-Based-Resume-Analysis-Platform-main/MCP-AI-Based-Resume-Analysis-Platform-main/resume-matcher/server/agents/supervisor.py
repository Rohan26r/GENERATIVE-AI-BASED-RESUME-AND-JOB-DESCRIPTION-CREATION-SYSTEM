"""
Supervisor Agent
----------------
Main coordinator. Decides which agents to run based on scores,
calls them in the right order, and assembles the final report.
"""

import logging
from datetime import datetime, timezone

from mcp.registry import execute_tool
from agents.recruiter_agent import RecruiterAgent
from agents.ats_agent import ATSAgent
from agents.coach_agent import CoachAgent
from agents.interview_agent import InterviewAgent
from agents.report_agent import ReportAgent

logger = logging.getLogger("agents.supervisor")


class SupervisorAgent:

    def run(self, file_path: str, job_description: str, uid: str) -> dict:
        logger.info("Supervisor starting for uid=%s", uid)

        # ── Step 1: Parse resume via MCP ──────────────────────────────────────
        r1 = execute_tool("parse_resume", {"file_path": file_path})
        if not r1.success:
            raise RuntimeError(f"parse_resume failed: {r1.error}")
        resume_data: dict = r1.data

        # ── Step 2: Analyze job description via MCP ───────────────────────────
        r2 = execute_tool("analyze_job_description", {"job_description": job_description})
        if not r2.success:
            raise RuntimeError(f"analyze_job_description failed: {r2.error}")
        job_data: dict = r2.data

        # ── Step 3: Compute match score via MCP ───────────────────────────────
        r3 = execute_tool("compute_match_score", {
            "resume_data": resume_data,
            "job_data": job_data,
        })
        if not r3.success:
            raise RuntimeError(f"compute_match_score failed: {r3.error}")
        match_data: dict = r3.data

        match_score: int = match_data.get("score", 0)

        # ── Shared context passed to all agents ───────────────────────────────
        context: dict = {
            "resume_data": resume_data,
            "job_data": job_data,
            "job_description": job_description,
            "match_data": match_data,
        }

        # ── Step 4: Supervisor decision logic ────────────────────────────────
        # Always run Recruiter
        logger.info("Running RecruiterAgent (score=%d)", match_score)
        context["recruiter_review"] = RecruiterAgent().run(context)

        # Always run ATS Agent
        logger.info("Running ATSAgent")
        context["ats_review"] = ATSAgent().run(context)

        ats_score: int = context["ats_review"].get("ats_score", 0)

        # Coach Agent: prioritized when match < 60 or ATS < 70
        if match_score < 60 or ats_score < 70:
            logger.info("Running CoachAgent (match=%d, ats=%d)", match_score, ats_score)
            context["roadmap"] = CoachAgent().run(context)
        else:
            # Still run it — just less critical
            logger.info("Running CoachAgent (supplementary)")
            context["roadmap"] = CoachAgent().run(context)

        # Interview Agent: run when profile is decent (score >= 40)
        if match_score >= 40:
            logger.info("Running InterviewAgent")
            context["interview_questions"] = InterviewAgent().run(context)
        else:
            logger.info("Skipping InterviewAgent — score too low (%d)", match_score)
            context["interview_questions"] = {
                "preparation_note": "Build core skills first before focusing on interview prep.",
                "technical_questions": [],
                "hr_questions": [],
                "mock_tips": [],
            }

        # ── Step 5: Report Agent always runs last ─────────────────────────────
        logger.info("Running ReportAgent")
        context["final_report"] = ReportAgent().run(context)

        # ── Step 6: Persist to Firestore ──────────────────────────────────────
        full_report = {
            "resume": resume_data,
            "job": job_data,
            "match": match_data,
            "recruiter_review": context["recruiter_review"],
            "ats_review": context["ats_review"],
            "roadmap": context["roadmap"],
            "interview_questions": context["interview_questions"],
            "final_report": context["final_report"],
            "created_at": datetime.now(timezone.utc).isoformat(),
            "uid": uid,
            "analysis_type": "agentic",
        }

        save_result = execute_tool("save_history", {"uid": uid, "report": full_report})
        if save_result.success:
            full_report["report_id"] = save_result.data.get("report_id")
            logger.info("Report saved: %s", full_report.get("report_id"))
        else:
            logger.warning("save_history failed (non-fatal): %s", save_result.error)

        return full_report
