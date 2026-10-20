"""Profile, preferences, password and account controls."""
from flask import Blueprint, current_app, flash, g, redirect, render_template, request, url_for
from flask_login import current_user, login_required, logout_user
from sqlalchemy import select

from ..accounts import delete_user, remove_solutions
from ..curriculum import COUNTRIES, available_levels, valid_choice
from ..extensions import db
from ..models import THEMES, User
from ..timeutil import is_valid_zone
from .helpers import valid_email

from ..i18n import COOKIE, LANGUAGES
from ..i18n import gettext as _

bp = Blueprint("settings", __name__, url_prefix="/settings")


def back(section):
    """Redirect to a section of the settings page."""
    return redirect(url_for("settings.index") + f"#{section}")


@bp.get("/")
@login_required
def index():
    return render_template("settings.html", themes=THEMES, countries=COUNTRIES, offered=available_levels())


@bp.post("/profile")
@login_required
def profile():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    if not name or len(name) > 80:
        flash(_("Please enter a name up to 80 characters."), "error")
        return back("profile")
    if not valid_email(email):
        flash(_("Enter a valid email address."), "error")
        return back("profile")
    if current_user.is_admin and email != current_user.email:
        flash(_("The admin email is set in the server settings and cannot be changed here."), "error")
        return back("profile")
    taken = db.session.scalar(select(User).where(User.email == email, User.id != current_user.id))
    if taken:
        flash(_("Another account already uses that email."), "error")
        return back("profile")
    current_user.name, current_user.email = name, email
    db.session.commit()
    flash(_("Profile updated."), "success")
    return back("profile")


@bp.post("/preferences")
@login_required
def preferences():
    theme = request.form.get("theme", "system")
    current_user.theme = theme if theme in THEMES else "system"
    if not current_user.is_admin:
        current_user.expand_steps = request.form.get("expand_steps") == "on"
        current_user.sounds = request.form.get("sounds") == "on"
    db.session.commit()
    chosen = request.form.get("language", "")
    if chosen in LANGUAGES:
        g.lang = chosen
    flash(_("Preferences saved."), "success")
    response = back("preferences")
    if chosen in LANGUAGES:
        response.set_cookie(COOKIE, chosen, max_age=365 * 24 * 3600, samesite="Lax", secure=current_app.config["SESSION_COOKIE_SECURE"])
    return response


@bp.post("/curriculum")
@login_required
def curriculum():
    place, _sep, stage = request.form.get("curriculum", "").partition(":")
    if current_user.is_admin or not valid_choice(place, stage) or bool(place) != bool(stage):
        flash(_("Choose a country and a level from the list."), "error")
        return back("curriculum")
    current_user.country, current_user.grade = place or None, stage or None
    db.session.commit()
    flash(_("Your curriculum was saved. Your language stays the same."), "success")
    return back("curriculum")


@bp.post("/password")
@login_required
def password():
    new, confirm = request.form.get("new_password", ""), request.form.get("confirm_password", "")
    if current_user.password_hash and not current_user.check_password(request.form.get("current_password", "")):
        flash(_("Your current password is not right."), "error")
    elif len(new) < 8:
        flash(_("Your new password needs at least 8 characters."), "error")
    elif new != confirm:
        flash(_("The two new passwords do not match."), "error")
    else:
        current_user.set_password(new)
        db.session.commit()
        flash(_("Password updated."), "success")
    return back("security")


@bp.post("/timezone")
@login_required
def timezone():
    zone = (request.get_json(silent=True) or {}).get("timezone", "")
    if not is_valid_zone(zone):
        return {"ok": False}, 400
    current_user.timezone = zone
    db.session.commit()
    return {"ok": True}


@bp.post("/clear-history")
@login_required
def clear_history():
    remove_solutions(current_user)
    db.session.commit()
    flash(_("Your solution history was cleared."), "info")
    return back("data")


@bp.post("/delete-account")
@login_required
def delete_account():
    if current_user.is_admin:
        flash(_("The admin account cannot be deleted."), "error")
        return back("data")
    confirmed = (
        current_user.check_password(request.form.get("password", ""))
        if current_user.password_hash
        else request.form.get("email", "").strip().lower() == current_user.email
    )
    if not confirmed:
        flash(_("That confirmation did not match, so your account was kept."), "error")
        return back("data")
    user = db.session.get(User, current_user.id)
    logout_user()
    delete_user(user)
    db.session.commit()
    flash(_("Your account and all of its data were deleted."), "info")
    return redirect(url_for("main.landing"))
