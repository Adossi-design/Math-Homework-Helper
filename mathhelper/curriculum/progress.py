"""A student's progress through a chapter: lessons done, exercises solved, assessment results and what to revise."""
from sqlalchemy import select

from ..extensions import db
from ..models import ChapterAttempt, ExerciseResult
from .checker import check
from .context import done_keys, section_key

PASS_MARK = 70
WEAK_MARK = 60
STRUGGLE_ATTEMPTS = 3


def chapter_progress(user, chapter):
    """Collect what the student has done in a chapter, and what they should revise."""
    done = done_keys(user)
    sections_done = [s.id for s in chapter.sections if section_key(chapter.id, s.id) in done]
    exercises = chapter.exercises()
    results = {
        r.exercise_id: r for r in db.session.scalars(
            select(ExerciseResult).where(ExerciseResult.user_id == user.id, ExerciseResult.exercise_id.like(f"{chapter.id}/%")))
    }
    solved = {i for i, r in results.items() if r.solved and i in exercises}
    attempts = list(db.session.scalars(
        select(ChapterAttempt).where(ChapterAttempt.user_id == user.id, ChapterAttempt.chapter_id == chapter.id).order_by(ChapterAttempt.id.desc())))
    return {
        "sections_done": sections_done,
        "solved": solved,
        "practice_total": len(chapter.practice),
        "practice_solved": sum(1 for e in chapter.practice if e.id in solved),
        "attempts": attempts,
        "best": max((a.percent for a in attempts), default=None),
        "last": attempts[0] if attempts else None,
        "revise": revision(chapter, results, attempts[0] if attempts else None),
        "prerequisites": prerequisites(chapter, done),
    }


def revision(chapter, results, last):
    """List the concepts to review: weak in the latest assessment, or an exercise tried three times without success."""
    weak = {}
    if last:
        for concept, (right, total) in last.by_concept.items():
            if total and 100 * right / total < WEAK_MARK:
                weak[concept] = f"{right}/{total}"
    exercises = chapter.exercises()
    for exercise_id, result in results.items():
        exercise = exercises.get(exercise_id)
        if exercise and not result.solved and result.attempts >= STRUGGLE_ATTEMPTS:
            weak.setdefault(exercise.concept, "")
    out = []
    for concept in chapter.concepts:
        section = chapter.concept_section(concept)
        if concept in weak and section:
            out.append({"concept": concept, "name": chapter.concepts[concept][0], "section": section.id, "score": weak[concept]})
    return out


def prerequisites(chapter, done):
    """Return each prerequisite of the chapter, a lesson or another chapter, with whether the student has finished it."""
    from .catalog import find_chapter

    out = []
    for item in chapter.prerequisites:
        if "chapter" in item:
            earlier = find_chapter(item["chapter"])
            finished = bool(earlier) and all(section_key(earlier.id, s.id) in done for s in earlier.sections)
        else:
            finished = f"{item['course']}/{item['lesson']}" in done
        out.append({**item, "done": finished})
    return out


def grade(exercises, answers):
    """Grade assessment answers, returning one verdict per question and the score for each concept."""
    verdicts, by_concept = [], {}
    for exercise, given in zip(exercises, answers):
        status = "blank" if not str(given).strip() else check(exercise.answer, given).status
        verdicts.append(status)
        right, total = by_concept.get(exercise.concept, (0, 0))
        by_concept[exercise.concept] = (right + (status == "correct"), total + 1)
    return verdicts, {concept: list(score) for concept, score in by_concept.items()}
