"""Command line helpers for the server owner."""
import random
import secrets

import click

from .curriculum.catalog import CHAPTERS
from .curriculum.translate import localize

ASSESSMENT_SAMPLES = 8


def chapter_trees(chapter):
    """Return every piece of a chapter that students read, shaped like the pages build them."""
    from .views.curriculum import chapter_view, exercise_view, section_view

    trees = [chapter_view(chapter), section_trees(chapter, section_view),
             {"exercises": [exercise_view(e) for e in chapter.practice]}, {"blocks": chapter.summary}]
    for _ in range(ASSESSMENT_SAMPLES):
        trees.append({"questions": [exercise_view(q) for q in chapter.assessment(random.Random(secrets.token_hex(4)))]})
    return trees


def section_trees(chapter, section_view):
    """Return all sections of a chapter."""
    return {"sections": [section_view(section) for section in chapter.sections]}


def register(app):
    """Add the commands to the app."""

    @app.cli.command("warm-translations")
    @click.option("--lang", default="", help="Only this target language, en or fr.")
    def warm_translations(lang):
        """Translate every curriculum lesson now, so the first student does not wait for it."""
        failed = 0
        for chapter in CHAPTERS:
            target = lang or ("en" if chapter.language == "fr" else "fr")
            if target == chapter.language:
                continue
            for tree in chapter_trees(chapter):
                failed += localize(tree, chapter.language, target).fallback
            click.echo(f"{chapter.id}: translated into {target}")
        click.echo("Some text could not be translated, run the command again." if failed else "All text is translated and stored.")
        raise SystemExit(1 if failed else 0)
