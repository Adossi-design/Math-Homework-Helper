"""Progress numbers for the dashboard, practice and learn pages."""
from datetime import timedelta

from sqlalchemy import func, select

from .content import courses, lesson_key
from .extensions import db
from .grades import GRADES, find_grade, lessons_for, rank
from .i18n import day_label
from .models import LessonCompletion, PracticeAttempt, Solution
from .practice.catalog import all_skills
from .timeutil import local_now, to_local


def active_days(user):
    """Return every local date on which the user solved, practiced or studied."""
    stamps = []
    for model in (Solution, PracticeAttempt, LessonCompletion):
        stamps += db.session.scalars(select(model.created_at).where(model.user_id == user.id)).all()
    return {to_local(stamp, user).date() for stamp in stamps}


def streak(days, today):
    """Count active days in a row, ending today or yesterday."""
    day = today if today in days else today - timedelta(days=1)
    count = 0
    while day in days:
        count += 1
        day -= timedelta(days=1)
    return count


def week(days, today):
    """Return the last seven days, oldest first, with activity flags."""
    dates = [today - timedelta(days=offset) for offset in range(6, -1, -1)]
    return [{"label": day_label(d), "active": d in days, "today": d == today} for d in dates]


def completed_keys(user):
    """Return the keys of every lesson the user finished."""
    return set(db.session.scalars(select(LessonCompletion.lesson_key).where(LessonCompletion.user_id == user.id)))


def best_scores(user):
    """Return the best score and number of rounds for each practiced skill."""
    rows = db.session.execute(
        select(PracticeAttempt.skill_id, func.max(PracticeAttempt.correct), func.count(), func.max(PracticeAttempt.total))
        .where(PracticeAttempt.user_id == user.id)
        .group_by(PracticeAttempt.skill_id)
    ).all()
    return {skill_id: {"best": best, "rounds": rounds, "total": total or 10} for skill_id, best, rounds, total in rows}


def summary(user):
    """Collect the headline numbers shown on the dashboard."""
    days = active_days(user)
    today = local_now(user).date()
    problem_lists = db.session.scalars(select(Solution.problems).where(Solution.user_id == user.id)).all()
    correct, total, rounds = db.session.execute(
        select(func.coalesce(func.sum(PracticeAttempt.correct), 0), func.coalesce(func.sum(PracticeAttempt.total), 0), func.count())
        .where(PracticeAttempt.user_id == user.id)
    ).one()
    done = completed_keys(user)
    return {
        "streak": streak(days, today),
        "week": week(days, today),
        "problems": sum(len(p or []) for p in problem_lists),
        "accuracy": round(100 * correct / total) if total else None,
        "rounds": rounds,
        "lessons": sum(course_progress(course, done) for course in courses()),
    }


def next_lesson(done, grade=None):
    """Return the first unfinished lesson of the student's class, then of the classes after it.

    Without a class, return the first unfinished lesson from the basics up.
    """
    if find_grade(grade):
        for later in [item.id for item in GRADES if rank(item.id) >= rank(grade)]:
            for course, lessons in lessons_for(courses(), later):
                for lesson in lessons:
                    if lesson_key(course, lesson) not in done:
                        return course, lesson
        return None, None
    for course in courses():
        for lesson in course.lessons:
            if lesson_key(course, lesson) not in done:
                return course, lesson
    return None, None


def class_skills(grade, earlier=False):
    """Return the ids of practice skills taught by the lessons of a class, and of earlier classes when asked."""
    if not find_grade(grade):
        return []
    grades = [item.id for item in GRADES if rank(item.id) < rank(grade)] if earlier else []
    ids = []
    for item in [grade, *reversed(grades)]:
        for _course, lessons in lessons_for(courses(), item):
            ids += [lesson.skill for lesson in lessons]
    return list(dict.fromkeys(ids))


def suggested_skill(best, preferred=None, allowed=None):
    """Pick a practice set: a weak one already tried, else the one for the next lesson, else a new one.

    When allowed is given, only those skills are picked from.
    """
    skills = list(all_skills().values())
    if allowed:
        skills = [s for s in skills if s.id in allowed] or skills
    if not skills:
        return None
    score = lambda s: best[s.id]["best"] / best[s.id]["total"]
    weak = [s for s in skills if s.id in best and score(s) < 0.8]
    if weak:
        return min(weak, key=score)
    match = next((s for s in skills if s.id == preferred), None)
    if match:
        return match
    untried = [s for s in skills if s.id not in best]
    return untried[0] if untried else min(skills, key=score)


def course_progress(course, done):
    """Return how many lessons of a course are finished."""
    return sum(1 for lesson in course.lessons if lesson_key(course, lesson) in done)
