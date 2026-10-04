"""Sign up, log in, log out and optional Google sign in."""
from authlib.integrations.base_client import OAuthError
from flask import Blueprint, abort, current_app, flash, g, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user, user_logged_in
from sqlalchemy import select

from .. import mailer, throttle
from ..extensions import db, oauth
from ..models import User
from ..i18n import gettext as _
from ..i18n import ngettext
from ..timeutil import is_valid_zone
from .helpers import safe_next, valid_email

bp = Blueprint("auth", __name__)
RETURNING = "returning"


@user_logged_in.connect
def note_sign_in(sender, **extra):
    """Flag this request as one where somebody signed in."""
    g.signed_in = True


@bp.after_app_request
def remember_visitor(response):
    """Mark this browser as known, so the login page can say welcome back next time."""
    if g.pop("signed_in", False):
        response.set_cookie(RETURNING, "1", max_age=2 * 365 * 24 * 3600, httponly=True, samesite="Lax",
                            secure=current_app.config["SESSION_COOKIE_SECURE"])
    return response


def remember_zone(user):
    """Store the browser time zone sent with the form, when it is valid."""
    zone = request.form.get("timezone", "")
    if is_valid_zone(zone):
        user.timezone = zone


def too_many_attempts(minutes):
    """Tell the visitor how long to wait after too many failed logins."""
    return ngettext("Too many attempts. Please wait {n} minute or reset your password.",
                    "Too many attempts. Please wait {n} minutes or reset your password.", minutes)


def suspended_notice():
    """Tell a suspended user why they cannot sign in."""
    return _("This account is suspended. Please contact support.")


def find_by_email(email):
    """Return the user with this email, or None."""
    return db.session.scalar(select(User).where(User.email == email))


@bp.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form, errors = {"name": "", "email": ""}, {}
    if request.method == "POST":
        form = {key: request.form.get(key, "").strip() for key in form}
        form["email"] = form["email"].lower()
        password = request.form.get("password", "")
        if not form["name"]:
            errors["name"] = _("Please tell us your name.")
        elif len(form["name"]) > 80:
            errors["name"] = _("Please use a shorter name.")
        if not valid_email(form["email"]):
            errors["email"] = _("Enter a valid email address.")
        elif find_by_email(form["email"]):
            errors["email"] = _("An account with this email already exists. Try logging in instead.")
        if len(password) < 8:
            errors["password"] = _("Use at least 8 characters.")
        if not errors:
            user = User(name=form["name"], email=form["email"])
            user.set_password(password)
            remember_zone(user)
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            return redirect(url_for("main.home"))
    return render_template("auth/signup.html", form=form, errors=errors)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    email, error, status = "", None, 200
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()[:255]
        wait = throttle.minutes_locked(email)
        user = find_by_email(email)
        if wait:
            error, status = too_many_attempts(wait), 429
        elif user and user.check_password(request.form.get("password", "")) and not user.is_active:
            error, status = suspended_notice(), 403
        elif user and user.check_password(request.form.get("password", "")):
            remember_zone(user)
            throttle.clear_failures(email)
            db.session.commit()
            login_user(user, remember=bool(request.form.get("remember")))
            return redirect(safe_next(request.args.get("next"), url_for("admin.index" if user.is_admin else "main.home")))
        elif user and not user.password_hash:
            error = _("This account signs in with Google. Use the Google button below.")
        else:
            throttle.record_failure(email)
            wait = throttle.minutes_locked(email)
            error = too_many_attempts(wait) if wait else _("That email and password do not match. Please try again.")
    returning = bool(request.cookies.get(RETURNING))
    return render_template("auth/login.html", email=email, error=error, returning=returning), status


@bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for("settings.index") + "#security")
    email, error, sent = "", None, False
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        user = find_by_email(email) if valid_email(email) else None
        if not valid_email(email):
            error = _("Enter a valid email address.")
        elif not mailer.mail_ready():
            error = _("Password reset by email is not set up yet. Please contact support.")
        elif user is None:
            error = _("No account uses that email. Check the spelling or create an account.")
        else:
            sent = True
            if mailer.recent_emails(email, "reset") < current_app.config["RESET_EMAILS_PER_HOUR"]:
                try:
                    mailer.send_password_reset(user)
                except mailer.MailError:
                    sent, error = False, _("We could not send the email. Please try again in a few minutes.")
    return render_template("auth/forgot.html", email=email, error=error, sent=sent, minutes=mailer.RESET_MINUTES)


@bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    user = mailer.user_from_reset_token(token)
    if user is None:
        flash(_("That link has expired. Please request a new one."), "error")
        return redirect(url_for("auth.forgot_password"))
    error = None
    if request.method == "POST":
        password = request.form.get("password", "")
        if len(password) < 8:
            error = _("Use at least 8 characters.")
        elif password != request.form.get("confirm", ""):
            error = _("The two passwords do not match.")
        else:
            user.set_password(password)
            throttle.clear_failures(user.email)
            db.session.commit()
            logout_user()
            if not login_user(user, remember=True):
                flash(suspended_notice(), "error")
                return redirect(url_for("auth.login"))
            flash(_("Your password was updated and you are logged in."), "success")
            return redirect(url_for("main.home"))
    return render_template("auth/reset.html", error=error, email=user.email)


@bp.post("/logout")
@login_required
def logout():
    logout_user()
    flash(_("You have been logged out. See you soon!"), "info")
    return redirect(url_for("main.landing"))


@bp.get("/login/google")
def google_login():
    client = oauth.create_client("google") if current_app.config["GOOGLE_READY"] else None
    if client is None:
        abort(404)
    return client.authorize_redirect(url_for("auth.google_callback", _external=True))


@bp.get("/login/google/callback")
def google_callback():
    client = oauth.create_client("google") if current_app.config["GOOGLE_READY"] else None
    if client is None:
        abort(404)
    try:
        token = client.authorize_access_token()
    except OAuthError:
        flash(_("Google sign in was cancelled or failed. Please try again."), "error")
        return redirect(url_for("auth.login"))

    # Link by Google id first, then by verified email, otherwise create a new account.
    info = token.get("userinfo") or {}
    google_id, email = info.get("sub"), (info.get("email") or "").lower()
    if not google_id or not email or not info.get("email_verified"):
        flash(_("Google did not share a verified email address, so we could not sign you in."), "error")
        return redirect(url_for("auth.login"))
    user = db.session.scalar(select(User).where(User.google_id == google_id)) or find_by_email(email)
    if user is None:
        user = User(name=(info.get("name") or email.split("@")[0])[:80], email=email)
        db.session.add(user)
    user.google_id = google_id
    db.session.commit()
    if not login_user(user, remember=True):
        flash(suspended_notice(), "error")
        return redirect(url_for("auth.login"))
    return redirect(url_for("main.home"))
