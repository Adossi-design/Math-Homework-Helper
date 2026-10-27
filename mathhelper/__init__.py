"""Math Homework Helper, a Flask web app that solves and teaches math."""
import logging

from dotenv import load_dotenv
from flask import Flask, g, render_template, request
from flask_login import current_user
from flask_wtf.csrf import CSRFError
from markupsafe import Markup
from werkzeug.middleware.proxy_fix import ProxyFix

from . import i18n, mailer, mascot, schema
from .config import BASE_DIR, INSTANCE_DIR, STATIC_DIR, load_settings
from .extensions import csrf, db, login_manager, oauth
from .models import User
from .text import plain, rich, rich_inline, tall_fractions
from .i18n import gettext as _
from .timeutil import time_ago, to_local


def icon(name, cls=""):
    """Return an inline SVG icon from the sprite."""
    return Markup(f'<svg class="icon {cls}" aria-hidden="true"><use href="#i-{name}"></use></svg>')


def create_app(overrides=None):
    """Build and configure the Flask application."""
    load_dotenv(BASE_DIR / ".env")
    app = Flask(__name__, instance_path=str(INSTANCE_DIR), static_folder=str(STATIC_DIR), static_url_path="/static")
    app.config.update(load_settings())
    app.config.update(overrides or {})
    if str(INSTANCE_DIR) in app.config["SQLALCHEMY_DATABASE_URI"]:
        INSTANCE_DIR.mkdir(exist_ok=True)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

    if app.config["BEHIND_PROXY"]:
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

    # Extensions and sign in.
    db.init_app(app)
    csrf.init_app(app)
    oauth.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to continue."
    login_manager.localize_callback = _
    login_manager.login_message_category = "info"

    @login_manager.user_loader
    def load_user(user_id):
        """Return the signed in user, or nobody when the account is suspended."""
        user = db.session.get(User, int(user_id))
        return user if user and user.is_active else None

    app.config.setdefault("BERAL_MODEL_FOUND", mascot.model_found())
    google_ready = bool(app.config["GOOGLE_CLIENT_ID"] and app.config["GOOGLE_CLIENT_SECRET"])
    app.config["GOOGLE_READY"] = google_ready
    if google_ready:
        oauth.register(
            "google",
            client_id=app.config["GOOGLE_CLIENT_ID"],
            client_secret=app.config["GOOGLE_CLIENT_SECRET"],
            server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
            client_kwargs={"scope": "openid email profile"},
        )

    from .views import register_blueprints

    register_blueprints(app)
    from .cli import register as register_commands

    register_commands(app)

    # Template helpers.
    app.jinja_env.globals.update(icon=icon, _=_, ngettext=i18n.ngettext)

    @app.before_request
    def choose_language():
        g.lang = i18n.pick_language()
    app.jinja_env.filters.update(rich=rich, rich_inline=rich_inline, plain=plain, ago=time_ago, tall=tall_fractions)
    app.jinja_env.filters["local"] = lambda moment, style="date": i18n.format_date(to_local(moment), style)

    @app.context_processor
    def shared_context():
        theme = current_user.theme if current_user.is_authenticated else "system"
        lang = i18n.language()
        return {"app_name": app.config["APP_NAME"], "google_ready": google_ready, "theme": theme,
                "support_email": app.config["SUPPORT_EMAIL"], "mail_provider": mailer.mail_provider(),
                "lang": lang, "languages": i18n.LANGUAGES,
                "js_strings": i18n.js_strings(),
                "mascot_name": mascot.NAME, "beral_model": mascot.model_url(),
                "mascot_data": lambda: mascot.payload(current_user.is_authenticated and not current_user.is_admin)}

    @app.after_request
    def security_headers(response):
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
        response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        return response

    register_error_pages(app)

    with app.app_context():
        db.create_all()
        schema.upgrade()
        schema.ensure_admin(app.config["ADMIN_EMAIL"], app.config["ADMIN_PASSWORD"])
    return app


def register_error_pages(app):
    """Show friendly pages instead of raw server errors."""
    pages = {
        400: ("Something was off with that request", "Please go back and try again."),
        403: ("You cannot open this page", "Your account does not have access to it."),
        404: ("Page not found", "The page you are looking for does not exist or was deleted."),
        413: ("That file is too big", "Please upload a photo smaller than 12 MB."),
        500: ("Something went wrong on our side", "Please try again in a moment."),
    }

    def render(code):
        title, message = pages[code]
        if request.accept_mimetypes.best == "application/json":
            return {"error": _(message)}, code
        return render_template("error.html", code=code, title=_(title), message=_(message)), code

    for code in pages:
        app.register_error_handler(code, lambda error, code=code: render(code))

    @app.errorhandler(CSRFError)
    def csrf_failed(error):
        if request.accept_mimetypes.best == "application/json":
            return {"error": _("Your session expired. Please refresh the page.")}, 400
        return render_template("error.html", code=400, title=_("Your session expired"),
                               message=_("Please refresh the page and try again.")), 400
