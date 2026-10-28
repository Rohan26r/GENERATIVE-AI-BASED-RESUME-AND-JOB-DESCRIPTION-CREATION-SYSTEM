"""
ATS Agent
---------
Focuses on ATS compatibility and resume keyword optimization.
Uses: ats_checker, improve_resume
"""

from agents.base_agent import BaseAgent


class ATSAgent(BaseAgent):

    def run(self, context: dict) -> dict:
        self.logger.info("ATSAgent running.")

        resume_data: dict = context["resume_data"]
        job_data: dict = context["job_data"]
        job_description: str = context["job_description"]

        # Run ats_checker via MCP
        ats_data = self.run_tool("ats_checker", {
            "resume_text": resume_data.get("resume_text", ""),
            "job_keywords": job_data.get("keywords", []),
        })

        # Run improve_resume via MCP
        improvement_data = self.run_tool("improve_resume", {
            "resume_text": resume_data.get("resume_text", ""),
            "job_description": job_description,
        })

        ats_score: int = ats_data.get("ats_score", 0)

        # ATS verdict
        if ats_score >= 80:
            ats_verdict = "Resume is ATS-friendly. Good keyword coverage."
        elif ats_score >= 60:
            ats_verdict = "Resume passes basic ATS filters but needs keyword improvements."
        else:
            ats_verdict = "Resume likely to be rejected by ATS. Significant fixes needed."

        return {
            "ats_score": ats_score,
            "ats_verdict": ats_verdict,
            "issues": ats_data.get("issues", []),
            "recommendations": ats_data.get("recommendations", []),
            "improved_summary": improvement_data.get("improved_summary", ""),
            "improved_skills": improvement_data.get("improved_skills", []),
            "improved_experience": improvement_data.get("improved_experience", []),
        }
