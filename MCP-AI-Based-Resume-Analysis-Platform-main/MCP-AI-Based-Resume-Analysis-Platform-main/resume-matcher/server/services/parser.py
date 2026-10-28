"""
File parser service — resolves local resume file paths.
Files are stored on disk via /api/upload-resume (no cloud storage needed).
"""

import os


def resolve_resume_path(file_path: str) -> str:
    """Validate and return the local resume file path."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Resume file not found: {file_path}")
    return file_path
