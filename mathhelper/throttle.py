"""Limits on failed logins, to slow down password guessing."""
import hashlib
import hmac
from datetime import timedelta
from math import ceil

from flask import current_app, request
from sqlalchemy import delete, select

from .extensions import db
from .models import LoginAttempt, utcnow


def network_key():
    """Return a scrambled form of the visitor's network address, so the raw address is never stored."""
    secret = current_app.config["SECRET_KEY"].encode()
    return hmac.new(secret, (request.remote_addr or "unknown").encode(), hashlib.sha256).hexdigest()[:32]


def minutes_locked(email):
    """Return how many minutes this login is blocked for, or 0 when it is allowed."""
    config = current_app.config
    window = timedelta(minutes=config["LOGIN_WINDOW_MINUTES"])
    since, key = utcnow() - window, network_key()
    recent = LoginAttempt.created_at >= since
    rules = [
        (config["LOGIN_ATTEMPTS"], (LoginAttempt.email == email, LoginAttempt.network == key)),
        (config["LOGIN_ATTEMPTS"] * 3, (LoginAttempt.email == email,)),
        (config["LOGIN_ATTEMPTS"] * 6, (LoginAttempt.network == key,)),
    ]
    wait = 0
    for limit, filters in rules:
        times = db.session.scalars(select(LoginAttempt.created_at).where(recent, *filters)).all()
        if len(times) >= limit:
            seconds = (min(times) + window - utcnow()).total_seconds()
            wait = max(wait, ceil(max(seconds, 1) / 60))
    return wait


def record_failure(email):
    """Remember a failed login and drop records that are more than a day old."""
    db.session.execute(delete(LoginAttempt).where(LoginAttempt.created_at < utcnow() - timedelta(days=1)))
    db.session.add(LoginAttempt(email=email[:255], network=network_key()))
    db.session.commit()


def clear_failures(email):
    """Forget failed logins for an address after a successful login or password reset."""
    db.session.execute(delete(LoginAttempt).where(LoginAttempt.email == email))
