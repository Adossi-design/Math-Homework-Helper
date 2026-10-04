"""French support: language choice, complete translations and translated content."""
import re
from html import unescape
from pathlib import Path

from flask import g

from mathhelper import ai
from mathhelper.content.courses import COURSES, LOCALIZED
from mathhelper.i18n import JS_KEYS
from mathhelper.models import LEVELS
from mathhelper.practice import SKILLS, build_round
from mathhelper.translations.fr import FR
from mathhelper.views.solve import EXAMPLES

ROOT = Path(__file__).resolve().parent.parent / "mathhelper"
FRENCH = {"Accept-Language": "fr-FR,fr;q=0.9,en;q=0.5"}
CALL = re.compile(r'\b(?:_|ngettext)\(\s*"((?:[^"\\]|\\.)*)"(?:\s*,\s*"((?:[^"\\]|\\.)*)")?')


def source_strings():
    """Collect every literal passed to the translation functions in templates and Python code."""
    found = set()
    for path in [*ROOT.rglob("*.html"), *ROOT.rglob("*.txt"), *ROOT.rglob("*.py")]:
        if path.name in {"fr.py", "i18n.py"}:
            continue
        text = path.read_text(encoding="utf-8")
        for match in CALL.finditer(text):
            first, second = match.group(1).replace('\\"', '"'), match.group(2)
            if "ngettext" in match.group(0):
                found.update({first, second})
            elif second is not None and "{" not in second and len(second) < 12:
                found.add(f"{first}|{second}")
            else:
                found.add(first)
    return {s for s in found if s}


def test_every_translated_string_has_french_text():
    dynamic = set(JS_KEYS) | set(LEVELS) | set(ai.TOPICS) | set(EXAMPLES) | {"Math"}
    dynamic |= {"Home", "Solve", "Library", "Learn", "Practice", "System", "Light", "Dark"}
    for skill in SKILLS.values():
        dynamic |= {skill.title, skill.blurb, skill.topic}
    missing = sorted((source_strings() | dynamic) - set(FR))
    assert missing == []


def test_french_text_keeps_the_same_placeholders():
    for english, french in FR.items():
        assert sorted(re.findall(r"\{\w+\}", english)) == sorted(re.findall(r"\{\w+\}", french)), english


def test_browser_language_picks_french_and_the_switch_overrides_it(client):
    assert "Bloqué sur un problème de maths" in client.get("/", headers=FRENCH).get_data(as_text=True)
    assert "Stuck on a math problem?" in client.get("/").get_data(as_text=True)

    response = client.get("/language/fr?next=/login")
    assert response.location.endswith("/login") and "lang=fr" in response.headers["Set-Cookie"]
    page = client.get("/login").get_data(as_text=True)
    assert '<html lang="fr"' in page and "<h1>Bienvenue</h1>" in page and "Mot de passe oublié" in page

    client.get("/language/en")
    assert "<h1>Welcome</h1>" in client.get("/login", headers=FRENCH).get_data(as_text=True)
    assert client.get("/language/fr?next=https://evil.example").location.endswith("/")


def test_app_pages_render_in_french(logged_in):
    logged_in.get("/language/fr")
    home = logged_in.get("/home").get_data(as_text=True)
    assert "Solutions récentes" in home and "Accueil" in home and "Exercices" in home
    learn = logged_in.get("/learn/").get_data(as_text=True)
    assert "Nombres entiers" in learn and "Whole Numbers" not in learn
    lesson = unescape(logged_in.get("/learn/algebra-1/systems").get_data(as_text=True))
    assert "Systèmes d'équations" in lesson and "Idées clés" in lesson and "Exemple corrigé" in lesson
    practice = unescape(logged_in.get("/practice/").get_data(as_text=True))
    assert "Équations du second degré" in practice and "Pas encore essayé" in practice
    for path in ["/solve", "/library", "/settings/", "/privacy", "/terms", "/about", "/forgot-password"]:
        assert logged_in.get(path, follow_redirects=True).status_code == 200
    assert "Politique de confidentialité" in logged_in.get("/privacy").get_data(as_text=True)
    assert "Page introuvable" in logged_in.get("/nope").get_data(as_text=True)


def test_language_can_be_changed_in_settings(logged_in):
    response = logged_in.post("/settings/preferences", data={"theme": "system", "language": "fr"})
    assert "lang=fr" in response.headers["Set-Cookie"]
    page = logged_in.get("/settings/").get_data(as_text=True)
    assert "Préférences enregistrées." in page and "Paramètres" in page


def test_french_messages_and_reset_email(client, make_user, outbox):
    make_user()
    client.get("/language/fr")
    wrong = client.post("/login", data={"email": "ama@example.com", "password": "nope"}).get_data(as_text=True)
    assert "ne correspondent pas" in wrong
    sent = client.post("/forgot-password", data={"email": "ama@example.com"}).get_data(as_text=True)
    assert "Vérifie tes e-mails" in sent
    assert "Réinitialise ton mot de passe" in outbox[0]["subject"] and "Bonjour Ama" in outbox[0]["html"]


def test_practice_and_courses_are_translated(app):
    with app.test_request_context("/"):
        g.lang = "fr"
        question = build_round("add-subtract", "demo")[0]
        assert question.prompt.startswith("Combien font")
    assert build_round("add-subtract", "demo")[0].prompt.startswith("What is")
    assert [c.id for c in LOCALIZED["fr"]] == [c.id for c in COURSES]
    for english_course, french_course in zip(COURSES, LOCALIZED["fr"]):
        assert french_course.title != "" and len(french_course.lessons) == len(english_course.lessons)


def test_ai_is_told_to_answer_in_french(app, monkeypatch):
    seen = {}

    def fake_run(contents, config, parse):
        seen["instructions"] = config.system_instruction
        return ai.SolveResult(problems=[])

    monkeypatch.setattr(ai, "_run", fake_run)
    with app.test_request_context("/"):
        g.lang = "fr"
        ai._solve(["2+2"])
        assert "in French" in seen["instructions"]
        g.lang = "en"
        ai._solve(["2+2"])
        assert "in French" not in seen["instructions"]


def test_language_switch_is_on_every_screen_and_keeps_the_page(client, logged_in):
    for path in ["/home", "/solve", "/library?q=x", "/learn/", "/practice/", "/settings/", "/about"]:
        page = unescape(logged_in.get(path).get_data(as_text=True))
        assert 'class="lang-toggle' in page and ">English<" in page and ">Français<" in page, path
    assert "/language/fr?next=/library?q%3Dx" in logged_in.get("/library?q=x").get_data(as_text=True).replace("%3F", "?")
    logged_in.post("/logout")
    for path in ["/", "/login", "/signup", "/forgot-password", "/privacy"]:
        assert 'class="lang-toggle' in client.get(path).get_data(as_text=True), path
    french = client.get("/language/fr?next=/login")
    assert french.location.endswith("/login")
    page = client.get("/login").get_data(as_text=True)
    assert '<span class="is-active" aria-current="true"><span class="full">Français</span>' in page and "/language/en?next=/login" in page
