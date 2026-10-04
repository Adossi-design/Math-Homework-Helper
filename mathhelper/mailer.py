"""Email delivery through Gmail or Resend, plus the password reset message."""
import hashlib
import hmac
import logging
import smtplib
from datetime import timedelta
from email.message import EmailMessage
from email.utils import formataddr, formatdate, make_msgid

import requests
from flask import current_app, render_template, url_for
from itsdangerous import BadSignature, URLSafeTimedSerializer
from sqlalchemy import func, select

from .extensions import db
from .i18n import gettext as _
from .models import EmailLog, User, utcnow

log = logging.getLogger(__name__)
RESEND_URL = "https://api.resend.com/emails"
RESET_MINUTES = 60


class MailError(Exception):
    """Raised when an email could not be sent."""


def smtp_ready():
    """Return True when a mailbox login such as Gmail is configured."""
    return bool(current_app.config["SMTP_USER"] and current_app.config["SMTP_PASSWORD"])


def mail_ready():
    """Return True when some way of sending email is configured."""
    return smtp_ready() or bool(current_app.config["RESEND_API_KEY"])


def mail_provider():
    """Name the service that delivers email, for the privacy page."""
    if not smtp_ready():
        return "Resend"
    return "Gmail" if "gmail" in current_app.config["SMTP_HOST"] else _("Our email provider")


def _send_smtp(to, subject, html, text):
    """Send one email through the configured mailbox, Gmail by default."""
    config = current_app.config
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = formataddr((config["APP_NAME"], config["SMTP_USER"]))
    message["To"] = to
    message["Date"] = formatdate()
    message["Message-ID"] = make_msgid(domain=config["SMTP_USER"].rpartition("@")[2])
    if config["SUPPORT_EMAIL"]:
        message["Reply-To"] = config["SUPPORT_EMAIL"]
    message.set_content(text)
    message.add_alternative(html, subtype="html")
    try:
        if config["SMTP_PORT"] == 465:
            server = smtplib.SMTP_SSL(config["SMTP_HOST"], config["SMTP_PORT"], timeout=15)
        else:
            server = smtplib.SMTP(config["SMTP_HOST"], config["SMTP_PORT"], timeout=15)
            server.starttls()
        with server:
            server.login(config["SMTP_USER"], config["SMTP_PASSWORD"])
            server.send_message(message)
    except (smtplib.SMTPException, OSError) as exc:
        log.warning("The mailbox refused an email: %s", exc)
        raise MailError("The email service refused the message.") from exc


def _send_resend(to, subject, html, text):
    """Send one email through Resend."""
    payload = {"from": current_app.config["MAIL_FROM"], "to": [to], "subject": subject, "html": html, "text": text}
    headers = {"Authorization": f"Bearer {current_app.config['RESEND_API_KEY']}"}
    try:
        response = requests.post(RESEND_URL, json=payload, headers=headers, timeout=15)
    except requests.RequestException as exc:
        raise MailError("Could not reach the email service.") from exc
    if response.status_code >= 400:
        log.warning("Resend refused an email with status %s: %s", response.status_code, response.text[:300])
        raise MailError("The email service refused the message.")


def send_email(to, subject, html, text):
    """Send one email, preferring the mailbox login over Resend."""
    if smtp_ready():
        _send_smtp(to, subject, html, text)
    elif current_app.config["RESEND_API_KEY"]:
        _send_resend(to, subject, html, text)
    else:
        raise MailError("Email is not set up yet.")


def _serializer():
    """Return the signer used for password reset links."""
    return URLSafeTimedSerializer(current_app.config["SECRET_KEY"], salt="password-reset")


def _stamp(user):
    """Fingerprint the current password so a link stops working once it changes."""
    return hashlib.sha256((user.password_hash or "no-password").encode()).hexdigest()[:16]


def make_reset_token(user):
    """Create a signed, time limited reset token for a user."""
    return _serializer().dumps({"id": user.id, "stamp": _stamp(user)})


def user_from_reset_token(token):
    """Return the user a reset token belongs to, or None when it is invalid or expired."""
    try:
        data = _serializer().loads(token, max_age=RESET_MINUTES * 60)
    except BadSignature:
        return None
    user = db.session.get(User, data.get("id")) if isinstance(data, dict) else None
    if user and hmac.compare_digest(str(data.get("stamp")), _stamp(user)):
        return user
    return None


def recent_emails(email, kind):
    """Count emails of one kind sent to an address in the past hour."""
    since = utcnow() - timedelta(hours=1)
    return db.session.scalar(
        select(func.count()).select_from(EmailLog).where(EmailLog.email == email, EmailLog.kind == kind, EmailLog.created_at >= since)
    )


def send_password_reset(user):
    """Email a reset link to the user and record that it was sent."""
    link = url_for("auth.reset_password", token=make_reset_token(user), _external=True)
    context = {"user": user, "link": link, "minutes": RESET_MINUTES}
    send_email(
        user.email,
        _("Reset your {name} password", name=current_app.config["APP_NAME"]),
        render_template("email/reset.html", **context),
        render_template("email/reset.txt", **context),
    )
    db.session.add(EmailLog(email=user.email, kind="reset"))
    db.session.commit()
