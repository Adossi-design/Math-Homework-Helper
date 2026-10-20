"""Small database upgrades and the admin account, both applied when the app starts."""
import hashlib
import hmac
import logging

from flask import current_app
from sqlalchemy import delete, inspect, select, text, update
from sqlalchemy.exc import SQLAlchemyError

from .extensions import db
from .models import LoginAttempt, Setting, User

log = logging.getLogger(__name__)
MIN_PASSWORD = 8

# Columns added after the first release, written for Postgres and for SQLite.
NEW_COLUMNS = {
    "user": {
        "is_admin": ("BOOLEAN NOT NULL DEFAULT FALSE", "BOOLEAN NOT NULL DEFAULT 0"),
        "suspended_at": ("TIMESTAMP", "DATETIME"),
        "grade": ("VARCHAR(10)", "VARCHAR(10)"),
    },
    "saved_lesson": {
        "grade": ("VARCHAR(10)", "VARCHAR(10)"),
    },
}


RETIRED_TABLES = ["assignment_completion", "assignment"]


def retire_tables():
    """Drop tables of removed features, but only while they are empty so no data is lost."""
    for table in RETIRED_TABLES:
        if table not in inspect(db.engine).get_table_names():
            continue
        try:
            with db.engine.begin() as connection:
                if connection.execute(text(f'SELECT COUNT(*) FROM "{table}"')).scalar() == 0:
                    connection.execute(text(f'DROP TABLE "{table}"'))
        except SQLAlchemyError:
            log.warning("Could not drop the retired table %s.", table)


def upgrade():
    """Add any column that an older database is missing, and retire unused tables."""
    retire_tables()
    postgres = db.engine.dialect.name == "postgresql"
    inspector = inspect(db.engine)
    for table, columns in NEW_COLUMNS.items():
        present = {column["name"] for column in inspector.get_columns(table)}
        for name, (postgres_type, sqlite_type) in columns.items():
            if name in present:
                continue
            guard, kind = ("IF NOT EXISTS ", postgres_type) if postgres else ("", sqlite_type)
            try:
                with db.engine.begin() as connection:
                    connection.execute(text(f'ALTER TABLE "{table}" ADD COLUMN {guard}{name} {kind}'))
            except SQLAlchemyError:
                # Another server instance may have added the column at the same moment.
                log.warning("Could not add %s.%s, it may already exist.", table, name)


def password_mark(password):
    """Return a keyed fingerprint of a password, so the app can tell when ADMIN_PASSWORD changed without storing it."""
    secret = current_app.config["SECRET_KEY"].encode()
    return hmac.new(secret, password.encode(), hashlib.sha256).hexdigest()


def ensure_admin(email, password):
    """Make the configured address the one admin account, and apply ADMIN_PASSWORD whenever it changes."""
    if not email:
        return
    try:
        db.session.execute(update(User).where(User.is_admin.is_(True), User.email != email).values(is_admin=False))
        user = db.session.scalar(select(User).where(User.email == email))
        usable = len(password) >= MIN_PASSWORD
        if not usable:
            log.warning("ADMIN_PASSWORD needs at least %s characters, so it was not applied.", MIN_PASSWORD)
        if user is None and usable:
            user = User(name="Admin", email=email)
            db.session.add(user)
        if user is not None:
            user.is_admin, user.suspended_at = True, None
        applied = db.session.get(Setting, "admin_password")
        mark = password_mark(password) if usable else None
        # A new value in ADMIN_PASSWORD replaces the current one once, so a password changed in Settings is kept until then.
        if user is not None and mark and (applied is None or applied.value != mark):
            user.set_password(password)
            db.session.execute(delete(LoginAttempt).where(LoginAttempt.email == email))
            if applied is None:
                db.session.add(Setting(key="admin_password", value=mark))
            else:
                applied.value = mark
        db.session.commit()
    except SQLAlchemyError:
        # Another server instance may have created the account at the same moment.
        db.session.rollback()
