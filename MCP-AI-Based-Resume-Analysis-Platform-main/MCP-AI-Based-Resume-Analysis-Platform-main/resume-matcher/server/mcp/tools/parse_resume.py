"""
MCP Tool: parse_resume
Extracts structured data from PDF or DOCX resume files.
"""

import re
import logging
from pathlib import Path

from mcp.models import ParseResumeInput
from mcp.utils import extract_skills_from_text

logger = logging.getLogger("mcp.tools.parse_resume")


def _read_pdf(path: str) -> str:
    import pdfplumber
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += (page.extract_text() or "") + "\n"
    return text.strip()


def _read_docx(path: str) -> str:
    from docx import Document
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs).strip()


def _extract_name(text: str) -> str:
    """Heuristic: first non-empty line is usually the candidate's name."""
    for line in text.splitlines():
        line = line.strip()
        if line and len(line.split()) <= 5:
            return line
    return "Unknown"


def _extract_experience(text: str) -> str:
    """Look for years of experience pattern."""
    match = re.search(r"(\d+)\+?\s*years?\s*(of\s*)?experience", text, re.IGNORECASE)
    if match:
        return f"{match.group(1)} years"
    return "Not specified"


def _extract_education(text: str) -> list[str]:
    degrees = re.findall(
        r"(Bachelor|Master|PhD|B\.?Sc|M\.?Sc|B\.?E|M\.?E|MBA|Associate)[^\n]*",
        text, re.IGNORECASE
    )
    return list(set(d.strip() for d in degrees)) or ["Not found"]


def _extract_certifications(text: str) -> list[str]:
    certs = re.findall(
        r"(AWS Certified|Google Cloud|Azure|PMP|CPA|CFA|Certified[^\n,]*)",
        text, re.IGNORECASE
    )
    return list(set(c.strip() for c in certs))


def parse_resume(inp: ParseResumeInput) -> dict:
    path = inp.file_path
    suffix = Path(path).suffix.lower()

    if suffix == ".pdf":
        text = _read_pdf(path)
    elif suffix in (".docx", ".doc"):
        text = _read_docx(path)
    else:
        raise ValueError(f"Unsupported file type: {suffix}. Use PDF or DOCX.")

    return {
        "name": _extract_name(text),
        "skills": extract_skills_from_text(text),
        "experience": _extract_experience(text),
        "education": _extract_education(text),
        "certifications": _extract_certifications(text),
        "resume_text": text,
    }
