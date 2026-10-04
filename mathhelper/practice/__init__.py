"""Practice skills grouped by level, with fresh questions every round."""
from . import college, elementary, high, middle  # noqa: F401  registers every skill
from .core import LEVEL_ORDER, QUESTIONS_PER_ROUND, SKILLS, Question, Skill, build_round


def skills_by_level():
    """Return skills grouped in level order."""
    return {level: [s for s in SKILLS.values() if s.level == level] for level in LEVEL_ORDER}


def score_round(skill_id, seed, answers):
    """Rebuild a round from its seed and count the correct answers."""
    questions = build_round(skill_id, seed)
    picks = (list(answers) + [-1] * len(questions))[: len(questions)]
    correct = sum(1 for q, a in zip(questions, picks) if a == q.answer)
    return questions, picks, correct


__all__ = ["LEVEL_ORDER", "QUESTIONS_PER_ROUND", "SKILLS", "Question", "Skill", "build_round", "score_round", "skills_by_level"]
# The catalog with the admin's changes lives in practice.catalog, which needs the database.
