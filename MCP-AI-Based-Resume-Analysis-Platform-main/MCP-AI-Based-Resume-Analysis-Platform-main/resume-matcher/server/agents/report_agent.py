"""
Report Agent
------------
Combines all agent outputs into one professional final report.
Always runs last in the supervisor pipeline.
"""

from agents.base_agent import BaseAgent


class ReportAgent(BaseAgent):

    def run(self, context: dict) -> dict:
        self.logger.info("ReportAgent generating final report.")

        recruiter = context.get("recruiter_review", {})
        ats = context.get("ats_review", {})
        coach = context.get("roadmap", {})
        interview = context.get("interview_questions", {})
        match_data = context.get("match_data", {})

        score = match_data.get("score", 0)
        ats_score = ats.get("ats_score", 0)
        missing_count = len(coach.get("missing_skills", []))

        # Final verdict logic
        if score >= 80 and ats_score >= 75:
            verdict = "Excellent candidate. Ready to apply — minimal changes needed."
            action = "Apply now and prepare for interviews."
            readiness = "High"
        elif score >= 60 and ats_score >= 60:
            verdict = "Strong candidate after resume optimization. Address ATS issues first."
            action = "Fix ATS issues, then apply within 1–2 weeks."
            readiness = "Medium-High"
        elif score >= 40:
            verdict = "Moderate fit. Skill building + resume rewrite recommended before applying."
            action = f"Complete the 30-day roadmap ({missing_count} skills to learn), then reapply."
            readiness = "Medium"
        else:
            verdict = "Significant gap between profile and role requirements."
            action = "Consider adjacent roles or invest 60+ days in skill development."
            readiness = "Low"

        # Summary bullets
        summary_points = []
        if recruiter.get("hiring_probability"):
            summary_points.append(f"Hiring Probability: {recruiter['hiring_probability']}")
        if ats.get("ats_verdict"):
            summary_points.append(f"ATS Status: {ats['ats_verdict']}")
        if coach.get("coaching_summary"):
            summary_points.append(f"Coach: {coach['coaching_summary']}")
        if interview.get("preparation_note"):
            summary_points.append(f"Interview: {interview['preparation_note']}")

        return {
            "final_verdict": verdict,
            "recommended_action": action,
            "readiness_level": readiness,
            "match_score": score,
            "ats_score": ats_score,
            "summary_points": summary_points,
        }
