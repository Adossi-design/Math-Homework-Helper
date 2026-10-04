"""Small helpers shared by the views."""
import re
from datetime import timedelta
from urllib.parse import urlparse

from flask import abort, request
from flask_login import current_user
from sqlalchemy import func, select

from ..extensions import db
from ..models import Message, Solution, utcnow

EMAIL = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def valid_email(email):
    """Return True for addresses shaped like name@example.com that fit the database column."""
    return len(email) <= 255 and bool(EMAIL.match(email))


def safe_next(target, fallback):
    """Only follow redirects that stay on this site."""
    if target and target.startswith("/") and not target.startswith("//") and not urlparse(target).netloc:
        return target
    return fallback


def wants_json():
    """Return True when the browser asked for JSON."""
    return request.accept_mimetypes.best == "application/json"


def owned_solution(solution_id):
    """Load a solution that belongs to the signed in user or stop with 404."""
    solution = db.session.get(Solution, solution_id)
    if not solution or solution.user_id != current_user.id:
        abort(404)
    return solution


def solves_last_hour(user):
    """Count solutions the user created in the past hour."""
    since = utcnow() - timedelta(hours=1)
    return db.session.scalar(select(func.count()).select_from(Solution).where(Solution.user_id == user.id, Solution.created_at >= since))


def questions_last_hour(user):
    """Count tutor questions the user asked in the past hour."""
    since = utcnow() - timedelta(hours=1)
    return db.session.scalar(
        select(func.count()).select_from(Message).join(Solution)
        .where(Solution.user_id == user.id, Message.role == "user", Message.created_at >= since)
    )
