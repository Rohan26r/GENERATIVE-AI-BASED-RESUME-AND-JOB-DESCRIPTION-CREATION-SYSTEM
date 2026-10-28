<div align="center">

# 🤖 Resume Matcher MCP

### Agentic AI Resume Analysis Platform

**MCP-first · Multi-Agent · FastAPI · React · Firebase**

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)](https://react.dev)
[![Firebase](https://img.shields.io/badge/Firebase-Firestore-orange?logo=firebase)](https://firebase.google.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

</div>

---

## What is this?

Resume Matcher MCP is a production-ready **Agentic AI** platform that analyzes resumes against job descriptions using a real **Model Context Protocol (MCP)** tool ecosystem backed by specialized AI agents.

Upload a resume → paste a job description → get a full career intelligence report in seconds.

---

## Architecture

```
React Frontend (Vite + Tailwind)
        ↓
FastAPI (REST + MCP endpoints)
        ↓
Supervisor Agent  ←── decision logic
        ↓
┌───────────────────────────────────┐
│  Recruiter Agent                  │
│  ATS Agent                        │
│  Coach Agent                      │
│  Interview Agent                  │
│  Report Agent                     │
└───────────────────────────────────┘
        ↓
MCP Tool Registry (14 tools)
        ↓
┌───────────────────────────────────┐
│  parse_resume                     │
│  analyze_job_description          │
│  compute_match_score              │
│  detect_skill_gap                 │
│  ats_checker                      │
│  improve_resume                   │
│  save_history                     │
│  run_full_analysis                │
│  + 6 agent tool wrappers          │
└───────────────────────────────────┘
        ↓
Firebase Firestore (report history)
```

---

## Features

| Feature | Description |
|---|---|
| **Match Score** | Skills 50% + Experience 30% + Keywords 20% weighted formula |
| **ATS Checker** | Keyword gaps, missing sections, formatting issues |
| **Skill Gap Detection** | Missing skills with curated learning resources |
| **Resume Improvement** | AI-generated summary, experience bullets, skills section |
| **Recruiter Agent** | Hiring probability, strengths, weaknesses analysis |
| **Coach Agent** | 30-day prioritized learning roadmap |
| **Interview Agent** | Technical + HR questions tailored to the role |
| **Final Report** | Readiness level + recommended action |
| **History** | All reports saved to Firestore, accessible anytime |

---

## Project Structure

```
resume-matcher/
├── client/                          # React + Vite + Tailwind
│   ├── src/
│   │   ├── components/
│   │   │   └── Navbar.jsx
│   │   ├── hooks/
│   │   │   └── useAuthState.js
│   │   ├── pages/
│   │   │   ├── Login.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Results.jsx          # 5-tab agent report UI
│   │   │   └── History.jsx
│   │   ├── firebase.js
│   │   ├── App.jsx
│   │   └── index.css
│   ├── .env.example
│   ├── package.json
│   └── vite.config.js
│
├── server/
│   ├── agents/                      # AI Agent layer
│   │   ├── base_agent.py            # Abstract base class
│   │   ├── supervisor.py            # Orchestrator
│   │   ├── recruiter_agent.py
│   │   ├── ats_agent.py
│   │   ├── coach_agent.py
│   │   ├── interview_agent.py
│   │   └── report_agent.py
│   │
│   ├── mcp/                         # MCP core
│   │   ├── registry.py              # Tool registry + executor
│   │   ├── server.py                # Bootstrap loader
│   │   ├── models.py                # Pydantic schemas
│   │   ├── utils.py                 # NLP helpers
│   │   └── tools/
│   │       ├── parse_resume.py
│   │       ├── analyze_job.py
│   │       ├── compute_match.py
│   │       ├── detect_gap.py
│   │       ├── ats_checker.py
│   │       ├── improve_resume.py
│   │       ├── save_history.py
│   │       ├── full_analysis.py
│   │       └── agent_tools.py       # Agent MCP wrappers
│   │
│   ├── api/
│   │   └── routes.py                # All FastAPI routes
│   │
│   ├── services/
│   │   ├── firebase.py              # Firestore client
│   │   ├── parser.py                # File path resolver
│   │   └── nlp.py
│   │
│   ├── main.py                      # FastAPI entry point
│   ├── .env.example
│   └── requirements.txt
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## Quick Start

### Prerequisites

- Python 3.12
- Node.js 18+
- Firebase project (free Spark plan)

### 1. Clone

```bash
git clone https://github.com/YOUR_USERNAME/resume-matcher-mcp.git
cd resume-matcher-mcp
```

### 2. Backend Setup

```bash
cd server

# Create virtual environment
py -3.12 -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt
pip install spacy --prefer-binary
python -m spacy download en_core_web_sm

# Configure environment
cp .env.example .env
# Edit .env — add your Firebase credentials path
```

### 3. Frontend Setup

```bash
cd client
npm install

# Configure environment
cp .env.example .env
# Edit .env — add your Firebase web config values
```

### 4. Firebase Setup

1. Go to [console.firebase.google.com](https://console.firebase.google.com)
2. Create a project (free Spark plan)
3. Enable **Authentication** → Email/Password
4. Enable **Firestore Database** → Start in production mode
5. Go to **Project Settings → Service accounts → Generate new private key**
6. Save the downloaded JSON as `server/serviceAccountKey.json`
7. Go to **Project Settings → Your apps → Web app**
8. Copy the config values into `client/.env`

### 5. Run

```bash
# Terminal 1 — Backend
cd server
venv\Scripts\activate
python -m uvicorn main:app --reload --port 8000

# Terminal 2 — Frontend
cd client
npm run dev
```

Open **http://localhost:5173**

---

## Environment Variables

### `server/.env`

```env
FIREBASE_CREDENTIALS_PATH=./serviceAccountKey.json
ALLOWED_ORIGINS=http://localhost:5173
```

### `client/.env`

```env
VITE_FIREBASE_API_KEY=your_api_key
VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your-project-id
VITE_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
VITE_FIREBASE_APP_ID=your_app_id
```

---

## API Reference

### MCP Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/mcp/tools` | List all 14 registered tools + schemas |
| `POST` | `/mcp/tools` | Same (POST alias) |
| `POST` | `/mcp/execute/{tool_name}` | Execute any tool directly |

### File & Analysis

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/upload-resume` | Upload PDF/DOCX resume |
| `POST` | `/api/full-analysis` | Run basic MCP pipeline |
| `GET` | `/api/history/{uid}` | Fetch user report history |

### Agent Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/agent/full-analysis` | Full supervisor agent pipeline |
| `POST` | `/api/agent/recruiter` | Recruiter agent only |
| `POST` | `/api/agent/ats` | ATS agent only |
| `POST` | `/api/agent/coach` | Coach agent only |
| `POST` | `/api/agent/interview` | Interview agent only |

### Example — Execute a tool directly

```bash
curl -X POST http://localhost:8000/mcp/execute/analyze_job_description \
  -H "Content-Type: application/json" \
  -d '{"payload": {"job_description": "Python developer with 3+ years FastAPI and Docker experience."}}'
```

Response:
```json
{
  "success": true,
  "tool": "analyze_job_description",
  "data": {
    "role": "Python developer with 3+ years FastAPI",
    "skills": ["docker", "fastapi", "python"],
    "experience_required": "3+ years",
    "keywords": ["developer", "docker", "experience", "fastapi", "python"]
  },
  "error": null
}
```

---

## MCP Tools Reference

| Tool | Input | Description |
|---|---|---|
| `parse_resume` | `file_path` | Extract name, skills, experience from PDF/DOCX |
| `analyze_job_description` | `job_description` | Extract role, skills, keywords |
| `compute_match_score` | `resume_data, job_data` | 50/30/20 weighted score |
| `detect_skill_gap` | `resume_skills, job_skills` | Missing skills + learning links |
| `ats_checker` | `resume_text, job_keywords` | ATS compatibility score |
| `improve_resume` | `resume_text, job_description` | AI-improved sections |
| `save_history` | `uid, report` | Persist to Firestore |
| `run_full_analysis` | `file_path, job_description, uid` | Full MCP pipeline |
| `run_supervisor_agent` | `file_path, job_description, uid` | Full agentic pipeline |
| `run_recruiter_agent` | `resume_data, job_data, match_data` | Recruiter review |
| `run_ats_agent` | `resume_data, job_data, job_description` | ATS optimization |
| `run_coach_agent` | `resume_data, job_data` | 30-day roadmap |
| `run_interview_agent` | `resume_data, job_data` | Interview questions |
| `generate_final_agent_report` | `recruiter_review, ats_review, roadmap, ...` | Final verdict |

---

## Agent System

### Supervisor Decision Logic

```
Always run:  RecruiterAgent + ATSAgent
If score < 60 or ATS < 70:  CoachAgent (priority mode)
If score >= 40:  InterviewAgent
Always last:  ReportAgent
```

### Firestore Data Model

```
users/{uid}/
  reports/{reportId}/
    resume:              { name, skills, experience, education }
    job:                 { role, skills, keywords }
    match:               { score, rating, matched_skills, breakdown }
    recruiter_review:    { verdict, hiring_probability, strengths, weaknesses }
    ats_review:          { ats_score, issues, recommendations, improved_summary }
    roadmap:             { missing_skills, roadmap_30_days, learning_resources }
    interview_questions: { technical_questions, hr_questions, mock_tips }
    final_report:        { final_verdict, readiness_level, recommended_action }
    created_at:          ISO timestamp
    analysis_type:       "agentic"
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Vite, Tailwind CSS, Recharts |
| Backend | Python 3.12, FastAPI, Uvicorn |
| MCP Core | Custom Python tool registry + Pydantic |
| AI/NLP | spaCy, sentence-transformers, scikit-learn |
| Resume Parsing | pdfplumber, python-docx |
| Database | Firebase Firestore |
| Auth | Firebase Authentication |
| Storage | Local disk (no cloud storage costs) |

---

## Cost

This project runs **100% free**:

- Firebase Spark plan: free (1GB Firestore, unlimited Auth)
- No OpenAI / paid LLM API required
- No cloud storage (files stored locally)
- Self-hosted backend

---

## License

MIT — free to use, modify, and distribute.

---

<div align="center">
Built with the MCP-first architecture · Agents on top of tools · Zero vendor lock-in
</div>
