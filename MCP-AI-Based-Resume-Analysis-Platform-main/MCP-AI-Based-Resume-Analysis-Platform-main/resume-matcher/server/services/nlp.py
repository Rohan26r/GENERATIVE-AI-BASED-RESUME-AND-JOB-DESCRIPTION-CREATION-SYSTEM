"""
NLP service — thin wrapper around mcp/utils for use outside MCP tools.
"""

from mcp.utils import extract_skills_from_text, extract_keywords, cosine_similarity_score

__all__ = ["extract_skills_from_text", "extract_keywords", "cosine_similarity_score"]
