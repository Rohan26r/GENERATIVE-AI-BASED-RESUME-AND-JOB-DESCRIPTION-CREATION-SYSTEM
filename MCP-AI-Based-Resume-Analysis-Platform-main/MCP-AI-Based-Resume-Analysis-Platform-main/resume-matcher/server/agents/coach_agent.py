"""
Coach Agent
-----------
Career coach that builds a 30-day learning roadmap from skill gaps.
Uses: detect_skill_gap
"""

from agents.base_agent import BaseAgent


# Priority tiers for common skills
_HIGH_PRIORITY = {"python", "sql", "docker", "git", "javascript", "react", "aws", "fastapi"}
_MED_PRIORITY = {"kubernetes", "typescript", "postgresql", "mongodb", "ci/cd", "linux"}


def _prioritize(skill: str) -> str:
    s = skill.lower()
    if s in _HIGH_PRIORITY:
        return "High"
    if s in _MED_PRIORITY:
        return "Medium"
    return "Low"


def _build_roadmap(missing_skills: list[str]) -> list[dict]:
    """Assign each missing skill to a week in a 30-day plan."""
    roadmap = []
    week_labels = ["Week 1 (Days 1–7)", "Week 2 (Days 8–14)", "Week 3 (Days 15–21)", "Week 4 (Days 22–30)"]

    # Sort by priority: High first
    priority_order = {"High": 0, "Medium": 1, "Low": 2}
    sorted_skills = sorted(missing_skills, key=lambda s: priority_order[_prioritize(s)])

    for i, skill in enumerate(sorted_skills[:8]):  # cap at 8 skills for 30 days
        week = week_labels[min(i // 2, 3)]
        roadmap.append({
            "week": week,
            "skill": skill,
            "priority": _prioritize(skill),
            "action": f"Study {skill} fundamentals, build a small project, add to resume.",
        })
    return roadmap


class CoachAgent(BaseAgent):

    def run(self, context: dict) -> dict:
        self.logger.info("CoachAgent running.")

        resume_data: dict = context["resume_data"]
        job_data: dict = context["job_data"]

        # Run detect_skill_gap via MCP
        gap_data = self.run_tool("detect_skill_gap", {
            "resume_skills": resume_data.get("skills", []),
            "job_skills": job_data.get("skills", []),
        })

        missing: list[str] = gap_data.get("missing_skills", [])
        resources: list[dict] = gap_data.get("recommended_learning", [])

        roadmap = _build_roadmap(missing)

        # Top 3 priorities
        high_priority = [s for s in missing if _prioritize(s) == "High"][:3]
        if not high_priority:
            high_priority = missing[:3]

        coaching_summary = (
            f"Focus on {len(missing)} missing skills. "
            f"Start with: {', '.join(high_priority) if high_priority else 'general skill building'}. "
            "Complete the 30-day roadmap to significantly improve your match score."
        ) if missing else "Great news — no critical skill gaps detected for this role!"

        return {
            "missing_skills": missing,
            "coaching_summary": coaching_summary,
            "top_priorities": high_priority,
            "roadmap_30_days": roadmap,
            "learning_resources": resources,
        }
