"""The library of every solved problem, with search and filters."""
from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
from sqlalchemy import String, cast, func, or_, select

from ..extensions import db
from ..models import Solution

bp = Blueprint("library", __name__)
PER_PAGE = 12


@bp.get("/library")
@login_required
def index():
    tab = "saved" if request.args.get("tab") == "saved" else "all"
    topic = request.args.get("topic", "").strip()
    query = request.args.get("q", "").strip()[:100]
    page = request.args.get("page", 1, type=int)

    # Build the filtered query step by step.
    stmt = select(Solution).where(Solution.user_id == current_user.id)
    if tab == "saved":
        stmt = stmt.where(Solution.starred.is_(True))
    if topic:
        stmt = stmt.where(Solution.topic == topic)
    if query:
        needle = query.lower()
        stmt = stmt.where(or_(
            func.lower(cast(Solution.problems, String)).contains(needle, autoescape=True),
            func.lower(func.coalesce(Solution.prompt, "")).contains(needle, autoescape=True),
        ))
    results = db.paginate(stmt.order_by(Solution.created_at.desc()), page=page, per_page=PER_PAGE, error_out=False)

    topics = db.session.scalars(
        select(Solution.topic).where(Solution.user_id == current_user.id).distinct().order_by(Solution.topic)
    ).all()
    total = db.session.scalar(select(func.count()).select_from(Solution).where(Solution.user_id == current_user.id))
    return render_template("library.html", results=results, tab=tab, topic=topic, query=query, topics=topics, total=total)
