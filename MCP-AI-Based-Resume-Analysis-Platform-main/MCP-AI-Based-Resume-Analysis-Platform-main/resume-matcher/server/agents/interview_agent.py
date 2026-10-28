"""
Interview Agent
---------------
Generates targeted interview questions based on role and skills.
Does not call an MCP tool — uses job_data and resume_data from context.
"""

from agents.base_agent import BaseAgent


# Question bank keyed by skill/topic
_TECH_QUESTIONS: dict[str, list[str]] = {
    "python": [
        "Explain the difference between a list and a tuple in Python.",
        "How does Python's GIL affect multithreading?",
        "What are decorators and how do you use them?",
    ],
    "sql": [
        "Explain the difference between INNER JOIN and LEFT JOIN.",
        "How would you optimize a slow SQL query?",
        "What is database normalization? Explain 1NF, 2NF, 3NF.",
    ],
    "docker": [
        "What is the difference between a Docker image and a container?",
        "How do you reduce Docker image size?",
        "Explain Docker Compose and when you'd use it.",
    ],
    "react": [
        "What is the virtual DOM and how does React use it?",
        "Explain the difference between useEffect and useLayoutEffect.",
        "How do you manage global state in a React app?",
    ],
    "fastapi": [
        "How does FastAPI handle async requests?",
        "What is dependency injection in FastAPI?",
        "How do you implement background tasks in FastAPI?",
    ],
    "aws": [
        "What is the difference between EC2 and Lambda?",
        "Explain S3 storage classes.",
        "How does IAM work in AWS?",
    ],
    "machine learning": [
        "Explain overfitting and how to prevent it.",
        "What is the bias-variance tradeoff?",
        "How do you handle imbalanced datasets?",
    ],
    "git": [
        "What is the difference between git merge and git rebase?",
        "How do you resolve a merge conflict?",
        "Explain git cherry-pick.",
    ],
}

_HR_QUESTIONS = [
    "Tell me about yourself and your career journey.",
    "Why are you interested in this specific role?",
    "Describe a challenging project and how you handled it.",
    "Where do you see yourself in 5 years?",
    "How do you handle tight deadlines and pressure?",
    "Tell me about a time you disagreed with a team member.",
]

_MOCK_TIPS = [
    "Use the STAR method (Situation, Task, Action, Result) for behavioral questions.",
    "Research the company's tech stack and recent projects before the interview.",
    "Prepare 2–3 questions to ask the interviewer about the team and role.",
    "Practice coding problems on LeetCode for technical rounds.",
    "Have concrete metrics ready — e.g., 'improved performance by 40%'.",
]


class InterviewAgent(BaseAgent):

    def run(self, context: dict) -> dict:
        self.logger.info("InterviewAgent running.")

        resume_data: dict = context["resume_data"]
        job_data: dict = context["job_data"]

        all_skills = set(s.lower() for s in (
            resume_data.get("skills", []) + job_data.get("skills", [])
        ))

        # Collect technical questions for matched skills
        tech_questions: list[str] = []
        covered_skills: list[str] = []
        for skill in all_skills:
            if skill in _TECH_QUESTIONS and len(tech_questions) < 9:
                tech_questions.extend(_TECH_QUESTIONS[skill])
                covered_skills.append(skill)

        # Fallback generic questions
        if not tech_questions:
            tech_questions = [
                "Walk me through a recent technical project you're proud of.",
                "How do you approach debugging a production issue?",
                "Describe your development workflow and tools you use.",
            ]

        role = job_data.get("role", "this role")

        return {
            "role": role,
            "technical_questions": tech_questions[:9],
            "hr_questions": _HR_QUESTIONS,
            "mock_tips": _MOCK_TIPS,
            "skills_covered": covered_skills,
            "preparation_note": (
                f"Focus your preparation on: {', '.join(covered_skills[:4]) if covered_skills else 'core fundamentals'}. "
                f"These are the most relevant skills for {role}."
            ),
        }
