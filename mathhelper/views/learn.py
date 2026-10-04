"""Course catalog, course pages and lessons."""
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import delete, select

from .. import mascot, stats
from ..content import courses, find_course, find_lesson, lesson_key
from ..extensions import db
from ..models import LessonCompletion
from ..practice.catalog import find_skill

from ..i18n import gettext as _

bp = Blueprint("learn", __name__, url_prefix="/learn")


def load(course_id, lesson_id=None):
    """Return the course and lesson for a URL or stop with 404."""
    course = find_course(course_id)
    if course is None:
        abort(404)
    if lesson_id is None:
        return course, None, -1
    lesson, index = find_lesson(course, lesson_id)
    if lesson is None:
        abort(404)
    return course, lesson, index


@bp.get("/")
@login_required
def index():
    done = stats.completed_keys(current_user)
    progress = {c.id: stats.course_progress(c, done) for c in courses()}
    course, lesson = stats.next_lesson(done)
    return render_template("learn/index.html", courses=courses(), progress=progress, next_course=course, next_lesson=lesson)


@bp.get("/<course_id>")
@login_required
def course(course_id):
    course, _, _ = load(course_id)
    done = stats.completed_keys(current_user)
    skills = [s for s in (find_skill(i) for i in dict.fromkeys(lesson.skill for lesson in course.lessons)) if s]
    resume = next((item for item in course.lessons if lesson_key(course, item) not in done), None)
    return render_template("learn/course.html", course=course, done=done, key=lesson_key, resume=resume,
                           finished=stats.course_progress(course, done), skills=skills)


@bp.get("/<course_id>/<lesson_id>")
@login_required
def lesson(course_id, lesson_id):
    course, lesson, index = load(course_id, lesson_id)
    done = stats.completed_keys(current_user)
    previous = course.lessons[index - 1] if index > 0 else None
    upcoming = course.lessons[index + 1] if index + 1 < len(course.lessons) else None
    return render_template("learn/lesson.html", course=course, lesson=lesson, index=index,
                           previous=previous, upcoming=upcoming, skill=find_skill(lesson.skill),
                           is_done=lesson_key(course, lesson) in done)


@bp.post("/<course_id>/<lesson_id>/complete")
@login_required
def complete(course_id, lesson_id):
    course, lesson, index = load(course_id, lesson_id)
    key = lesson_key(course, lesson)
    existing = db.session.scalar(
        select(LessonCompletion).where(LessonCompletion.user_id == current_user.id, LessonCompletion.lesson_key == key)
    )
    if existing:
        db.session.execute(delete(LessonCompletion).where(LessonCompletion.id == existing.id))
        db.session.commit()
        flash(_("Marked as not done."), "info")
        return redirect(url_for("learn.lesson", course_id=course.id, lesson_id=lesson.id))

    db.session.add(LessonCompletion(user_id=current_user.id, lesson_key=key))
    db.session.commit()
    mascot.queue("completed")
    if index + 1 < len(course.lessons):
        return redirect(url_for("learn.lesson", course_id=course.id, lesson_id=course.lessons[index + 1].id))
    return redirect(url_for("learn.course", course_id=course.id))
