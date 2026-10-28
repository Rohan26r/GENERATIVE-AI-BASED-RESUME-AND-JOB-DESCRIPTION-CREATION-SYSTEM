"""
Shared NLP utilities used across MCP tools.
spaCy is optional — all functions fall back to regex if it's not installed.
"""

import re
import logging
from functools import lru_cache

logger = logging.getLogger("mcp.utils")

SKILL_KEYWORDS = {
    "python", "java", "javascript", "typescript", "react", "node", "sql",
    "nosql", "mongodb", "postgresql", "mysql", "docker", "kubernetes", "aws",
    "gcp", "azure", "git", "ci/cd", "rest", "graphql", "fastapi", "django",
    "flask", "machine learning", "deep learning", "nlp", "data analysis",
    "pandas", "numpy", "tensorflow", "pytorch", "scikit-learn", "spark",
    "hadoop", "linux", "bash", "html", "css", "tailwind", "figma", "agile",
    "scrum", "jira", "communication", "leadership", "teamwork",
}

_SPACY_AVAILABLE: bool | None = None  # None = not yet checked


def _spacy_nlp():
    """Return spaCy nlp object or None if unavailable."""
    global _SPACY_AVAILABLE
    if _SPACY_AVAILABLE is False:
        return None
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        _SPACY_AVAILABLE = True
        return nlp
    except Exception:
        _SPACY_AVAILABLE = False
        logger.warning("spaCy not available — using regex fallback for NLP.")
        return None


def extract_skills_from_text(text: str) -> list[str]:
    """Extract skill keywords from free text. Uses spaCy if available."""
    text_lower = text.lower()
    found = {skill for skill in SKILL_KEYWORDS if skill in text_lower}

    nlp = _spacy_nlp()
    if nlp:
        doc = nlp(text)
        for chunk in doc.noun_chunks:
            c = chunk.text.lower().strip()
            if c in SKILL_KEYWORDS:
                found.add(c)

    return sorted(found)


def extract_keywords(text: str) -> list[str]:
    """Extract meaningful keywords from text. Uses spaCy POS tags if available."""
    nlp = _spacy_nlp()
    if nlp:
        doc = nlp(text)
        return sorted({
            token.lemma_.lower()
            for token in doc
            if token.pos_ in ("NOUN", "PROPN") and not token.is_stop and len(token.text) > 2
        })

    # Regex fallback — filter common stopwords
    stopwords = {
        "the", "and", "for", "with", "that", "this", "are", "was",
        "have", "will", "you", "our", "your", "their", "from", "into",
    }
    words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
    return sorted({w for w in words if w not in stopwords})


def cosine_similarity_score(text_a: str, text_b: str) -> float:
    """Semantic similarity via sentence-transformers. Returns 0.0 on failure."""
    try:
        from sentence_transformers import SentenceTransformer, util
        model = SentenceTransformer("all-MiniLM-L6-v2")
        emb_a = model.encode(text_a, convert_to_tensor=True)
        emb_b = model.encode(text_b, convert_to_tensor=True)
        return round(float(util.cos_sim(emb_a, emb_b).item()), 4)
    except Exception:
        logger.warning("sentence-transformers unavailable — returning 0.0 similarity.")
        return 0.0
