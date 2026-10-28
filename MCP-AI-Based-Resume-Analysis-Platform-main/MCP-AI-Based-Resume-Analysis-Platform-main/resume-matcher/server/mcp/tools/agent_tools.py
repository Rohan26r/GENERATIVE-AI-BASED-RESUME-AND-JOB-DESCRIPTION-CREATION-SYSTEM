"""
MCP Agent Tool Wrappers
-----------------------
Exposes each agent as a registered MCP tool.
Thin wrappers only — all logic lives in agents/.
"""

from mcp.models import (
    SupervisorInput, RecruiterAgentInput, ATSAgentInput,
    CoachAgentInput, InterviewAgentInput, ReportAgentInput,
)


def run_supervisor_agent(inp: SupervisorInput) -> dict:
    """Full agentic pipeline via Supervisor."""
    from agents.supervisor import SupervisorAgent
    return SupervisorAgent().run(
        file_path=inp.file_path,
        job_description=inp.job_description,
        uid=inp.uid,
    )


def run_recruiter_agent(inp: RecruiterAgentInput) -> dict:
    """Run only the Recruiter Agent on pre-parsed data."""
    from agents.recruiter_agent import RecruiterAgent
    return RecruiterAgent().run({
        "resume_data": inp.resume_data,
        "job_data": inp.job_data,
        "match_data": inp.match_data,
    })


def run_ats_agent(inp: ATSAgentInput) -> dict:
    """Run only the ATS Agent."""
    from agents.ats_agent import ATSAgent
    return ATSAgent().run({
        "resume_data": inp.resume_data,
        "job_data": inp.job_data,
        "job_description": inp.job_description,
    })


def run_coach_agent(inp: CoachAgentInput) -> dict:
    """Run only the Coach Agent."""
    from agents.coach_agent import CoachAgent
    return CoachAgent().run({
        "resume_data": inp.resume_data,
        "job_data": inp.job_data,
    })


def run_interview_agent(inp: InterviewAgentInput) -> dict:
    """Run only the Interview Agent."""
    from agents.interview_agent import InterviewAgent
    return InterviewAgent().run({
        "resume_data": inp.resume_data,
        "job_data": inp.job_data,
    })


def generate_final_agent_report(inp: ReportAgentInput) -> dict:
    """Run only the Report Agent on pre-collected context."""
    from agents.report_agent import ReportAgent
    return ReportAgent().run({
        "recruiter_review": inp.recruiter_review,
        "ats_review": inp.ats_review,
        "roadmap": inp.roadmap,
        "interview_questions": inp.interview_questions,
        "match_data": inp.match_data,
    })
