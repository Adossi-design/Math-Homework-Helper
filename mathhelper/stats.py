"""Progress numbers for the dashboard, practice and learning."""
from datetime import timedelta

from sqlalchemy import func, select, union_all

from .extensions import db
from .i18n import day_label
from .models import LessonCompletion, PracticeAttempt, Solution
from .practice.catalog import all_skills
from .timeutil import local_now, to_local


def active_days(user):
    """Return every local date on which the user solved, practiced or studied."""
    query = union_all(*(select(model.created_at).where(model.user_id == user.id) for model in (Solution, PracticeAttempt, LessonCompletion)))
    return {to_local(stamp, user).date() for stamp in db.session.scalars(select(query.subquery().c.created_at))}


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


def summary(user, done=None):
    """Collect the headline numbers shown on the dashboard."""
    days = active_days(user)
    today = local_now(user).date()
    problem_lists = db.session.scalars(select(Solution.problems).where(Solution.user_id == user.id)).all()
    correct, total, rounds = db.session.execute(
        select(func.coalesce(func.sum(PracticeAttempt.correct), 0), func.coalesce(func.sum(PracticeAttempt.total), 0), func.count())
        .where(PracticeAttempt.user_id == user.id)
    ).one()
    done = completed_keys(user) if done is None else done
    return {
        "streak": streak(days, today),
        "week": week(days, today),
        "problems": sum(len(p or []) for p in problem_lists),
        "accuracy": round(100 * correct / total) if total else None,
        "rounds": rounds,
        "lessons": sum(1 for key in done if key.startswith("cur:")),
    }


def suggested_skill(best):
    """Pick a practice set: a weak one already tried, else a new one."""
    skills = list(all_skills().values())
    if not skills:
        return None
    score = lambda s: best[s.id]["best"] / best[s.id]["total"]
    weak = [s for s in skills if s.id in best and score(s) < 0.8]
    if weak:
        return min(weak, key=score)
    untried = [s for s in skills if s.id not in best]
    return untried[0] if untried else min(skills, key=score)
