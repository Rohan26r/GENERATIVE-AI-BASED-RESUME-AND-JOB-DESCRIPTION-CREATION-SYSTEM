"""
Recruiter Agent
---------------
Acts like an HR recruiter reviewing the resume against the job.
Uses: parse_resume, analyze_job_description, compute_match_score
"""

from agents.base_agent import BaseAgent


class RecruiterAgent(BaseAgent):

    def run(self, context: dict) -> dict:
        self.logger.info("RecruiterAgent running.")

        resume_data: dict = context["resume_data"]
        job_data: dict = context["job_data"]
        match_data: dict = context["match_data"]

        score: int = match_data.get("score", 0)
        matched: list = match_data.get("matched_skills", [])
        rating: str = match_data.get("rating", "Weak")

        # Hiring probability heuristic
        if score >= 80:
            probability = "High (80–100%)"
            verdict = "Strong candidate. Likely to pass initial screening."
        elif score >= 60:
            probability = "Moderate (50–79%)"
            verdict = "Decent profile. Resume needs minor improvements to stand out."
        elif score >= 40:
            probability = "Low (25–49%)"
            verdict = "Significant gaps exist. Focus on skill building and resume rewrite."
        else:
            probability = "Very Low (<25%)"
            verdict = "Profile does not match this role well. Consider adjacent roles."

        # Strengths: matched skills + experience
        strengths = []
        if matched:
            strengths.append(f"Matched {len(matched)} required skills: {', '.join(matched[:5])}")
        exp = resume_data.get("experience", "Not specified")
        if exp != "Not specified":
            strengths.append(f"Has {exp} of experience")
        certs = resume_data.get("certifications", [])
        if certs:
            strengths.append(f"Holds certifications: {', '.join(certs[:3])}")
        if not strengths:
            strengths.append("Resume submitted — no strong signals detected yet.")

        # Weaknesses: missing skills
        job_skills = set(s.lower() for s in job_data.get("skills", []))
        resume_skills = set(s.lower() for s in resume_data.get("skills", []))
        missing = list(job_skills - resume_skills)
        weaknesses = []
        if missing:
            weaknesses.append(f"Missing key skills: {', '.join(missing[:5])}")
        if score < 60:
            weaknesses.append("Overall match score is below recruiter threshold (60).")
        if not resume_data.get("certifications"):
            weaknesses.append("No certifications listed — consider adding relevant ones.")
        if not weaknesses:
            weaknesses.append("No major weaknesses detected.")

        return {
            "score": score,
            "rating": rating,
            "hiring_probability": probability,
            "verdict": verdict,
            "strengths": strengths,
            "weaknesses": weaknesses,
        }
