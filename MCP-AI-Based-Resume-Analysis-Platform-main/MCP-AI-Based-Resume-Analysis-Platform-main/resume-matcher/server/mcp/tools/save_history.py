"""
MCP Tool: save_history
Persists analysis report to Firebase Firestore under users/{uid}/reports.
"""

import logging
from datetime import datetime, timezone

from mcp.models import SaveHistoryInput

logger = logging.getLogger("mcp.tools.save_history")


def save_history(inp: SaveHistoryInput) -> dict:
    from services.firebase import get_firestore

    db = get_firestore()
    # Copy report so we don't mutate the caller's dict
    report = dict(inp.report)
    report["created_at"] = datetime.now(timezone.utc).isoformat()
    report["uid"] = inp.uid

    doc_ref = db.collection("users").document(inp.uid).collection("reports").document()
    doc_ref.set(report)

    logger.info("Saved report %s for user %s", doc_ref.id, inp.uid)

    return {"success": True, "report_id": doc_ref.id}
