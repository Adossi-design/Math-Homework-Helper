"""Blueprints for every part of the site."""
from . import admin, auth, curriculum, library, main, practice, settings, solve


def register_blueprints(app):
    """Attach every blueprint to the app."""
    for module in (auth, main, solve, library, curriculum, practice, settings, admin):
        app.register_blueprint(module.bp)
