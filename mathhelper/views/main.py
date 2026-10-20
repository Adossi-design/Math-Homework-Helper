"""Landing page, dashboard and private photo delivery."""
from flask import Blueprint, Response, abort, current_app, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import select

from .. import stats
from ..extensions import db
from ..images import load_image
from ..models import Solution
from ..i18n import COOKIE, LANGUAGES, format_date, language
from ..timeutil import greeting, local_now
from .helpers import safe_next

bp = Blueprint("main", __name__)


@bp.get("/")
def landing():
    if current_user.is_authenticated:
        return redirect(url_for("admin.index" if current_user.is_admin else "main.home"))
    return render_template("landing.html")


@bp.get("/language/<code>")
def set_language(code):
    response = redirect(safe_next(request.args.get("next"), url_for("main.landing")))
    if code in LANGUAGES:
        response.set_cookie(COOKIE, code, max_age=365 * 24 * 3600, samesite="Lax", secure=current_app.config["SESSION_COOKIE_SECURE"])
    return response


@bp.get("/about")
def about():
    return render_template("about.html")


@bp.get("/privacy")
def privacy():
    return render_template("legal/privacy_fr.html" if language() == "fr" else "legal/privacy.html")


@bp.get("/terms")
def terms():
    return render_template("legal/terms_fr.html" if language() == "fr" else "legal/terms.html")


@bp.get("/home")
@login_required
def home():
    recent = db.session.scalars(
        select(Solution).where(Solution.user_id == current_user.id).order_by(Solution.created_at.desc()).limit(4)
    ).all()
    done = stats.completed_keys(current_user)
    best = stats.best_scores(current_user)
    course, lesson = stats.next_lesson(done, current_user.grade)
    return render_template(
        "home.html",
        greeting=greeting(),
        today=format_date(local_now(), "day"),
        numbers=stats.summary(current_user),
        recent=recent,
        next_course=course,
        next_lesson=lesson,
        suggestion=stats.suggested_skill(best, lesson.skill if lesson else None,
                                         stats.class_skills(current_user.grade, earlier=True)),
        best=best,
    )


@bp.get("/uploads/<name>")
@login_required
def upload(name):
    owner = db.session.scalar(select(Solution.user_id).where(Solution.image_name == name))
    data = load_image(name) if owner == current_user.id else None
    if data is None:
        abort(404)
    return Response(data, mimetype="image/jpeg", headers={"Cache-Control": "private, max-age=86400"})
