"""Practice catalog, quiz rounds and results."""
import re
import secrets

from flask import Blueprint, abort, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import func, select

from .. import mascot, stats
from ..content import courses
from ..extensions import db
from ..models import PracticeAttempt
from ..practice import QUESTIONS_PER_ROUND, build_round
from ..practice.catalog import all_skills, find_skill, score

from ..i18n import gettext as _

bp = Blueprint("practice", __name__, url_prefix="/practice")
SEED = re.compile(r"[0-9a-f]{16}")


def lesson_for(skill_id):
    """Return the first course and lesson that teach a skill."""
    for course in courses():
        for lesson in course.lessons:
            if lesson.skill == skill_id:
                return course, lesson
    return None, None


def parse_answers(raw):
    """Turn a comma separated list into answer positions, using -1 for skipped ones."""
    picks = []
    for part in raw.split(",")[:QUESTIONS_PER_ROUND]:
        try:
            value = int(part)
        except ValueError:
            value = -1
        picks.append(value if -1 <= value <= 3 else -1)
    return picks


def feedback(percent):
    """Return an encouraging headline for a score."""
    if percent == 100:
        return _("Perfect round!")
    if percent >= 80:
        return _("Great work!")
    if percent >= 50:
        return _("Good effort. Review the ones you missed.")
    return _("Keep going. Every round makes it stick.")


@bp.get("/")
@login_required
def index():
    skills = all_skills()
    recent = db.session.scalars(
        select(PracticeAttempt).where(PracticeAttempt.user_id == current_user.id, PracticeAttempt.skill_id.in_(list(skills)))
        .order_by(PracticeAttempt.created_at.desc()).limit(5)
    ).all()
    mine = [skills[i] for i in stats.class_skills(current_user.grade) if i in skills]
    others = [skill for skill in skills.values() if skill not in mine]
    return render_template("practice/index.html", best=stats.best_scores(current_user), recent=recent, skills=skills,
                           mine=mine, others=others)


@bp.get("/<skill_id>")
@login_required
def play(skill_id):
    skill = find_skill(skill_id) or abort(404)
    seed = secrets.token_hex(8)
    questions = [q.__dict__ for q in build_round(skill_id, seed, skill=skill)]
    course, lesson = lesson_for(skill_id)
    return render_template("practice/round.html", skill=skill, seed=seed, questions=questions, course=course, lesson=lesson)


@bp.post("/<skill_id>/finish")
@login_required
def finish(skill_id):
    skill = find_skill(skill_id) or abort(404)
    seed = request.form.get("seed", "")
    if not SEED.fullmatch(seed):
        abort(400)
    questions, picks, correct = score(skill, seed, parse_answers(request.form.get("answers", "")))
    attempt = PracticeAttempt(user_id=current_user.id, skill_id=skill_id, seed=seed, answers=picks,
                              correct=correct, total=len(questions))
    db.session.add(attempt)
    db.session.commit()
    mascot.queue("milestone" if attempt.percent >= 80 else "encourage")
    return redirect(url_for("practice.results", attempt_id=attempt.id))


@bp.get("/results/<int:attempt_id>")
@login_required
def results(attempt_id):
    attempt = db.session.get(PracticeAttempt, attempt_id)
    skill = find_skill(attempt.skill_id) if attempt else None
    if not attempt or attempt.user_id != current_user.id or skill is None:
        abort(404)
    questions, picks, _ = score(skill, attempt.seed, attempt.answers)
    earlier_best = db.session.scalar(
        select(func.max(PracticeAttempt.correct)).where(
            PracticeAttempt.user_id == current_user.id,
            PracticeAttempt.skill_id == attempt.skill_id,
            PracticeAttempt.id < attempt.id,
        )
    )
    course, lesson = lesson_for(attempt.skill_id)
    return render_template(
        "practice/results.html",
        attempt=attempt,
        skill=skill,
        review=list(zip(questions, picks)),
        headline=feedback(attempt.percent),
        new_best=earlier_best is not None and attempt.correct > earlier_best,
        course=course,
        lesson=lesson,
    )
