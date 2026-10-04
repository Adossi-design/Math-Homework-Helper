"""Settings read from environment variables."""
import os
import secrets
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INSTANCE_DIR = BASE_DIR / "instance"
STATIC_DIR = BASE_DIR / "public" / "static"


def _database_url():
    """Return the database URL, defaulting to a local SQLite file."""
    url = os.getenv("DATABASE_URL", "").strip()
    if not url:
        return f"sqlite:///{INSTANCE_DIR / 'app.db'}"
    for prefix in ("postgres://", "postgresql://"):
        if url.startswith(prefix):
            return "postgresql+psycopg://" + url[len(prefix):]
    return url


def _engine_options(url):
    """Return connection settings that suit the database in use."""
    if url.startswith("postgresql"):
        return {"pool_pre_ping": True, "pool_recycle": 280, "pool_size": 3, "max_overflow": 2,
                "connect_args": {"prepare_threshold": None}}
    return {"pool_pre_ping": True}


def _flag(name, default="0"):
    """Read an on or off switch from the environment."""
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "on"}


def load_settings():
    """Collect every setting the app needs into one dictionary."""
    app_name = os.getenv("APP_NAME", "Math Homework Helper")
    database_url = _database_url()
    hosted = bool(os.getenv("VERCEL"))
    return {
        "APP_NAME": app_name,
        "SECRET_KEY": os.getenv("SECRET_KEY") or secrets.token_hex(32),
        "SQLALCHEMY_DATABASE_URI": database_url,
        "SQLALCHEMY_ENGINE_OPTIONS": _engine_options(database_url),
        "MAX_CONTENT_LENGTH": 12 * 1024 * 1024,
        "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY", "").strip(),
        "GEMINI_MODEL": os.getenv("GEMINI_MODEL", "gemini-flash-latest").strip(),
        "GEMINI_FALLBACK_MODEL": os.getenv("GEMINI_FALLBACK_MODEL", "gemini-flash-lite-latest").strip(),
        "SOLVES_PER_HOUR": int(os.getenv("SOLVES_PER_HOUR", "30")),
        "QUESTIONS_PER_HOUR": int(os.getenv("QUESTIONS_PER_HOUR", "60")),
        "GOOGLE_CLIENT_ID": os.getenv("GOOGLE_CLIENT_ID", "").strip(),
        "GOOGLE_CLIENT_SECRET": os.getenv("GOOGLE_CLIENT_SECRET", "").strip(),
        "RESEND_API_KEY": os.getenv("RESEND_API_KEY", "").strip(),
        "MAIL_FROM": os.getenv("MAIL_FROM", "").strip() or f"{app_name} <onboarding@resend.dev>",
        "SMTP_HOST": os.getenv("SMTP_HOST", "smtp.gmail.com").strip(),
        "SMTP_PORT": int(os.getenv("SMTP_PORT", "465")),
        "SMTP_USER": os.getenv("SMTP_USER", "").strip(),
        "SMTP_PASSWORD": os.getenv("SMTP_PASSWORD", "").replace(" ", ""),
        "SUPPORT_EMAIL": os.getenv("SUPPORT_EMAIL", "").strip(),
        "BERAL_MODEL_URL": os.getenv("BERAL_MODEL_URL", "").strip(),
        "ADMIN_EMAIL": os.getenv("ADMIN_EMAIL", "").strip().lower(),
        "ADMIN_PASSWORD": os.getenv("ADMIN_PASSWORD", ""),
        "LOGIN_ATTEMPTS": int(os.getenv("LOGIN_ATTEMPTS", "5")),
        "LOGIN_WINDOW_MINUTES": int(os.getenv("LOGIN_WINDOW_MINUTES", "15")),
        "RESET_EMAILS_PER_HOUR": int(os.getenv("RESET_EMAILS_PER_HOUR", "3")),
        "SUPABASE_URL": os.getenv("SUPABASE_URL", "").strip(),
        "SUPABASE_ANON_KEY": os.getenv("SUPABASE_ANON_KEY", "").strip(),
        "SESSION_COOKIE_HTTPONLY": True,
        "SESSION_COOKIE_SAMESITE": "Lax",
        "SESSION_COOKIE_SECURE": _flag("SECURE_COOKIES", "1" if hosted else "0"),
        "REMEMBER_COOKIE_SECURE": _flag("SECURE_COOKIES", "1" if hosted else "0"),
        "BEHIND_PROXY": _flag("BEHIND_PROXY", "1" if hosted else "0"),
        "WTF_CSRF_TIME_LIMIT": None,
    }
