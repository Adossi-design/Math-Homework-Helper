"""Practice skills as students see them: the built in ones with the admin's changes, plus the admin's own sets."""
from dataclasses import replace

from flask import g, has_app_context
from sqlalchemy import select

from ..extensions import db
from ..i18n import language, polish
from ..models import SavedPractice
from ..text import mark_math
from .core import LEVEL_ORDER, SKILLS, Question, Skill, build_round


def stored_practice():
    """Return every practice set the admin wrote or changed, read once per request."""
    if not has_app_context():
        return []
    if "practice_rows" not in g:
        g.practice_rows = db.session.scalars(select(SavedPractice).order_by(SavedPractice.id)).all()
    return g.practice_rows


def forget_practice():
    """Drop the cached practice sets after the admin changes one."""
    g.pop("practice_rows", None)
    g.pop("skill_cache", None)


def local_text(row, lang, name):
    """Return one text field in a language, using English where the other language is empty."""
    local = row.content.get(lang, {}).get(name) if lang != "en" else None
    return polish(local or row.content.get("en", {}).get(name, ""), lang)


def written_questions(row, lang):
    """Turn the admin's stored questions into questions in one language."""
    questions = []
    for item in row.questions or []:
        english, local = item["en"], item.get(lang, {}) if lang != "en" else {}
        choices = local.get("choices") if len(local.get("choices") or []) == len(english["choices"]) else english["choices"]
        text = lambda value: mark_math(polish(value, lang))
        questions.append(Question(text(local.get("prompt") or english["prompt"]), [text(c) for c in choices],
                                  item["answer"], text(local.get("explanation") or english.get("explanation", ""))))
    return tuple(questions)


def skill_from_row(row, lang):
    """Build the skill a stored row describes, in one language."""
    base = SKILLS.get(row.skill_id)
    if base is not None and not row.content:
        return base
    title, blurb = local_text(row, lang, "title"), local_text(row, lang, "blurb")
    if base is not None:
        return replace(base, title=title or base.title, blurb=blurb or base.blurb, level=row.level or base.level,
                       topic=row.topic or base.topic)
    return Skill(row.skill_id, title, row.level, row.topic, blurb, None, written_questions(row, lang))


def all_skills(hidden=False):
    """Return every practice skill by id in the current language, leaving out hidden ones unless asked."""
    lang = language()
    cache = g.setdefault("skill_cache", {}) if has_app_context() else {}
    if (lang, hidden) in cache:
        return cache[lang, hidden]
    rows = {row.skill_id: row for row in stored_practice()}
    result = {}
    for skill_id, skill in SKILLS.items():
        row = rows.pop(skill_id, None)
        if row is None:
            result[skill_id] = skill
        elif hidden or row.visible:
            result[skill_id] = skill_from_row(row, lang)
    for row in rows.values():
        if hidden or row.visible:
            result[row.skill_id] = skill_from_row(row, lang)
    # Keep a steady order from the basics up, with the admin's own sets at the end.
    rank = {name: i for i, name in enumerate(LEVEL_ORDER)}
    result = dict(sorted(result.items(), key=lambda item: rank.get(item[1].level, len(rank))))
    cache[lang, hidden] = result
    return result


def find_skill(skill_id, hidden=False):
    """Return one skill by id, or None."""
    return all_skills(hidden).get(skill_id)


def score(skill, seed, answers):
    """Rebuild a round from its seed and count the correct answers."""
    questions = build_round(skill.id, seed, skill=skill)
    picks = (list(answers) + [-1] * len(questions))[: len(questions)]
    return questions, picks, sum(1 for q, a in zip(questions, picks) if a == q.answer)
