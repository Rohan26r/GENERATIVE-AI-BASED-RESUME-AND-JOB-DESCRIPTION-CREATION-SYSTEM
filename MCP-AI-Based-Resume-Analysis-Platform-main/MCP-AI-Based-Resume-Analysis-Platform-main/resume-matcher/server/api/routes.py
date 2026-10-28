"""
FastAPI routes — MCP endpoints + convenience API endpoints.
"""

import os
import logging
from typing import Any

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel

from mcp.registry import execute_tool, list_tools
from mcp.models import MCPResponse

logger = logging.getLogger("api.routes")

router = APIRouter()


# ── MCP endpoints ─────────────────────────────────────────────────────────────

@router.get("/mcp/tools", response_model=list[dict])
def get_tools():
    """List all registered MCP tools and their input schemas."""
    return list_tools()


class ExecuteRequest(BaseModel):
    payload: dict[str, Any] = {}


@router.post("/mcp/tools", response_model=MCPResponse)
def list_tools_post():
    """POST alias for listing tools (MCP spec compatibility)."""
    return MCPResponse(success=True, tool="list_tools", data=list_tools())


@router.post("/mcp/execute/{tool_name}", response_model=MCPResponse)
def execute(tool_name: str, body: ExecuteRequest):
    """Execute any registered MCP tool by name."""
    result = execute_tool(tool_name, body.payload)
    if not result.success:
        raise HTTPException(status_code=400, detail=result.error)
    return result


# ── Convenience API endpoints ─────────────────────────────────────────────────

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/api/upload-resume")
async def upload_resume(file: UploadFile = File(...), uid: str = Form(...)):
    """
    Save uploaded resume to local disk.
    Returns the local file path for use in /api/full-analysis.
    """
    suffix = os.path.splitext(file.filename or "resume")[-1].lower()
    if suffix not in (".pdf", ".docx"):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported.")

    # Sanitize filename and store under uploads/{uid}/
    user_dir = os.path.join(UPLOAD_DIR, uid)
    os.makedirs(user_dir, exist_ok=True)

    safe_name = f"{uid}_{file.filename}"
    local_path = os.path.join(user_dir, safe_name)

    contents = await file.read()
    with open(local_path, "wb") as f:
        f.write(contents)

    logger.info("Saved resume for uid=%s -> %s", uid, local_path)
    return {"success": True, "file_path": local_path}


class FullAnalysisRequest(BaseModel):
    file_path: str       # local path returned by /api/upload-resume
    job_description: str
    uid: str


@router.post("/api/full-analysis", response_model=MCPResponse)
def full_analysis(body: FullAnalysisRequest):
    """Run the full MCP pipeline on an already-uploaded local resume file."""
    if not os.path.exists(body.file_path):
        raise HTTPException(status_code=404, detail="Resume file not found. Please upload again.")

    result = execute_tool("run_full_analysis", {
        "file_path": body.file_path,
        "job_description": body.job_description,
        "uid": body.uid,
    })

    if not result.success:
        raise HTTPException(status_code=400, detail=result.error)
    return result


@router.get("/api/history/{uid}")
def get_history(uid: str):
    """Fetch all analysis reports for a user from Firestore."""
    from services.firebase import get_firestore

    db = get_firestore()
    docs = db.collection("users").document(uid).collection("reports") \
              .order_by("created_at", direction="DESCENDING").limit(20).stream()

    reports = [{"id": doc.id, **doc.to_dict()} for doc in docs]
    return {"success": True, "reports": reports}


# ── Agent routes ──────────────────────────────────────────────────────────────

class AgentAnalysisRequest(BaseModel):
    file_path: str
    job_description: str
    uid: str


@router.post("/api/agent/full-analysis", response_model=MCPResponse)
def agent_full_analysis(body: AgentAnalysisRequest):
    """
    Run the full Supervisor Agent pipeline.
    Returns recruiter review, ATS review, roadmap, interview prep, and final verdict.
    """
    if not os.path.exists(body.file_path):
        raise HTTPException(status_code=404, detail="Resume file not found. Please upload again.")

    result = execute_tool("run_supervisor_agent", {
        "file_path": body.file_path,
        "job_description": body.job_description,
        "uid": body.uid,
    })
    if not result.success:
        raise HTTPException(status_code=400, detail=result.error)
    return result


class AgentContextRequest(BaseModel):
    """Shared request body for single-agent endpoints that need pre-parsed data."""
    resume_data: dict
    job_data: dict
    job_description: str = ""
    match_data: dict = {}


@router.post("/api/agent/recruiter", response_model=MCPResponse)
def agent_recruiter(body: AgentContextRequest):
    """Run only the Recruiter Agent."""
    result = execute_tool("run_recruiter_agent", {
        "resume_data": body.resume_data,
        "job_data": body.job_data,
        "match_data": body.match_data,
    })
    if not result.success:
        raise HTTPException(status_code=400, detail=result.error)
    return result


@router.post("/api/agent/ats", response_model=MCPResponse)
def agent_ats(body: AgentContextRequest):
    """Run only the ATS Agent."""
    result = execute_tool("run_ats_agent", {
        "resume_data": body.resume_data,
        "job_data": body.job_data,
        "job_description": body.job_description,
    })
    if not result.success:
        raise HTTPException(status_code=400, detail=result.error)
    return result


@router.post("/api/agent/coach", response_model=MCPResponse)
def agent_coach(body: AgentContextRequest):
    """Run only the Coach Agent."""
    result = execute_tool("run_coach_agent", {
        "resume_data": body.resume_data,
        "job_data": body.job_data,
    })
    if not result.success:
        raise HTTPException(status_code=400, detail=result.error)
    return result


@router.post("/api/agent/interview", response_model=MCPResponse)
def agent_interview(body: AgentContextRequest):
    """Run only the Interview Agent."""
    result = execute_tool("run_interview_agent", {
        "resume_data": body.resume_data,
        "job_data": body.job_data,
    })
    if not result.success:
        raise HTTPException(status_code=400, detail=result.error)
    return result
