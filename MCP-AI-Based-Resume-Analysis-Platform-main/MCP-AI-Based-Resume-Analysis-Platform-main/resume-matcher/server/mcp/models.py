"""Pydantic models for MCP tool inputs/outputs and standard responses."""

from typing import Any
from pydantic import BaseModel


# ── Standard MCP envelope ────────────────────────────────────────────────────

class MCPResponse(BaseModel):
    success: bool
    tool: str
    data: Any = None
    error: str | None = None


# ── Tool input schemas ────────────────────────────────────────────────────────

class ParseResumeInput(BaseModel):
    file_path: str


class AnalyzeJobInput(BaseModel):
    job_description: str


class ComputeMatchInput(BaseModel):
    resume_data: dict
    job_data: dict


class DetectGapInput(BaseModel):
    resume_skills: list[str]
    job_skills: list[str]


class ATSCheckerInput(BaseModel):
    resume_text: str
    job_keywords: list[str]


class ImproveResumeInput(BaseModel):
    resume_text: str
    job_description: str


class SaveHistoryInput(BaseModel):
    uid: str
    report: dict


class FullAnalysisInput(BaseModel):
    file_path: str
    job_description: str
    uid: str


# ── Agent tool input schemas ──────────────────────────────────────────────────

class SupervisorInput(BaseModel):
    file_path: str
    job_description: str
    uid: str


class RecruiterAgentInput(BaseModel):
    resume_data: dict
    job_data: dict
    match_data: dict


class ATSAgentInput(BaseModel):
    resume_data: dict
    job_data: dict
    job_description: str


class CoachAgentInput(BaseModel):
    resume_data: dict
    job_data: dict


class InterviewAgentInput(BaseModel):
    resume_data: dict
    job_data: dict


class ReportAgentInput(BaseModel):
    recruiter_review: dict
    ats_review: dict
    roadmap: dict
    interview_questions: dict
    match_data: dict
