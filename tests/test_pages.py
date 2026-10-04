"""Learn pages, settings, the dashboard and text helpers."""
from datetime import date

from mathhelper.content import COURSES
from mathhelper.practice import SKILLS
from mathhelper.stats import streak
from mathhelper.text import plain, rich, rich_inline


def test_every_course_and_lesson_page_renders(logged_in):
    for course in COURSES:
        assert logged_in.get(f"/learn/{course.id}").status_code == 200
        for lesson in course.lessons:
            assert lesson.skill in SKILLS
            assert logged_in.get(f"/learn/{course.id}/{lesson.id}").status_code == 200
    assert logged_in.get("/learn/nope").status_code == 404


def test_completing_a_lesson_moves_to_the_next(logged_in):
    response = logged_in.post("/learn/algebra-1/solving-equations/complete")
    assert response.location.endswith("/learn/algebra-1/slope-lines")
    assert "1 of 3 done" in logged_in.get("/learn/").get_data(as_text=True)
    logged_in.post("/learn/algebra-1/solving-equations/complete")
    assert "0 of 3 done" in logged_in.get("/learn/").get_data(as_text=True)


def test_dashboard_shows_progress(logged_in):
    logged_in.post("/solve", data={"mode": "type", "problem": "2x + 3 = 11"})
    html = logged_in.get("/home").get_data(as_text=True)
    assert "Ama" in html and "Recent solutions" in html and "2x + 3 = 11" in html


def test_settings_update_profile_preferences_and_password(logged_in):
    logged_in.post("/settings/profile", data={"name": "Ama K", "email": "ama.k@example.com"})
    logged_in.post("/settings/preferences", data={"theme": "dark", "sounds": "on"})
    page = logged_in.get("/settings/").get_data(as_text=True)
    assert 'data-theme="dark"' in page and "ama.k@example.com" in page and 'name="level"' not in page

    logged_in.post("/settings/password", data={"current_password": "secret123", "new_password": "newpass99", "confirm_password": "newpass99"})
    logged_in.post("/logout")
    assert logged_in.post("/login", data={"email": "ama.k@example.com", "password": "newpass99"}).location.endswith("/home")


def test_delete_account_needs_the_password(logged_in):
    logged_in.post("/settings/delete-account", data={"password": "wrong"})
    assert logged_in.get("/home").status_code == 200
    logged_in.post("/settings/delete-account", data={"password": "secret123"})
    assert logged_in.get("/home").status_code == 302
    assert "do not match" in logged_in.post("/login", data={"email": "ama@example.com", "password": "secret123"}).get_data(as_text=True)


def test_rich_text_keeps_math_and_blocks_html():
    html = str(rich("**Bold** and $a_1 * b_2$ <script>alert(1)</script>"))
    assert "<strong>Bold</strong>" in html and "$a_1 * b_2$" in html and "<script>" not in html
    assert str(rich_inline("$x < 3$")) == "$x &lt; 3$"
    assert plain(r"Solve $\frac{3}{4} + x^2$") == "Solve 3/4 + x^2"


def test_latex_written_without_dollar_signs_still_renders_as_math():
    assert str(rich_inline(r"x = \frac{13}{6}")) == r"$x = \frac{13}{6}$"
    assert str(rich_inline(r"**Answer:** x = \frac{13}{6} or about 2.17")) == r"<strong>Answer:</strong> $x = \frac{13}{6}$ or about 2.17"
    assert str(rich_inline(r"The answer is \frac{13}{6}.")) == r"The answer is $\frac{13}{6}$."
    assert str(rich_inline(r"Réponse : x = \frac{13}{6}")) == r"Réponse : $x = \frac{13}{6}$"
    assert str(rich_inline(r"$\\frac{13}{6}$")) == r"$\frac{13}{6}$"
    assert str(rich_inline(r"\sqrt{2} and x^2 + 1")) == r"$\sqrt{2}$ and $x^2 + 1$"
    assert str(rich_inline("Add 2 to both sides, then divide.")) == "Add 2 to both sides, then divide."
    assert str(rich_inline(r"$\frac{1}{2}$ is already fine")) == r"$\frac{1}{2}$ is already fine"


def test_a_saved_answer_with_a_bare_fraction_is_shown_as_math(app, logged_in):
    from mathhelper.extensions import db
    from mathhelper.models import Solution
    with app.app_context():
        db.session.add(Solution(user_id=1, source="type", prompt="13/6", topic="Fractions", problems=[
            {"problem": "Write 13 over 6", "topic": "Fractions", "answer": r"\frac{13}{6}",
             "steps": [{"title": "Write it", "result": r"\frac{13}{6}", "work": r"Put 13 over 6 to get \frac{13}{6}."}], "tip": ""}]))
        db.session.commit()
    page = logged_in.get("/solutions/1").get_data(as_text=True)
    assert r'<div class="value">$\dfrac{13}{6}$</div>' in page and r"to get $\frac{13}{6}$." in page
    assert r'<div class="step-result">$\dfrac{13}{6}$</div>' in page


def test_streak_counts_consecutive_days():
    today = date(2026, 10, 1)
    days = {date(2026, 9, 29), date(2026, 9, 30), date(2026, 10, 1), date(2026, 9, 20)}
    assert streak(days, today) == 3
    assert streak(days - {today}, today) == 2
    assert streak(set(), today) == 0


def test_privacy_and_terms_are_public(client):
    privacy = client.get("/privacy").get_data(as_text=True)
    assert "Privacy Policy" in privacy and "Google Gemini" in privacy and "Delete your account" in privacy
    assert "Terms of Service" in client.get("/terms").get_data(as_text=True)
    landing = client.get("/").get_data(as_text=True)
    assert 'href="/privacy"' in landing and 'href="/terms"' in landing
    assert 'href="/privacy"' in client.get("/signup").get_data(as_text=True)


def test_deleting_an_account_also_removes_its_email_records(app, logged_in, outbox):
    from mathhelper.extensions import db
    from mathhelper.models import EmailLog
    logged_in.post("/logout")
    logged_in.post("/forgot-password", data={"email": "ama@example.com"})
    logged_in.post("/login", data={"email": "ama@example.com", "password": "secret123"})
    with app.app_context():
        assert db.session.scalar(db.select(db.func.count()).select_from(EmailLog)) == 1
    logged_in.post("/settings/delete-account", data={"password": "secret123"})
    with app.app_context():
        assert db.session.scalar(db.select(db.func.count()).select_from(EmailLog)) == 0


def test_about_page_is_public_and_linked_from_the_landing_page(client):
    about = client.get("/about").get_data(as_text=True)
    assert "Snap and solve" in about and "How it works" in about
    assert 'href="/about"' in client.get("/").get_data(as_text=True)


def test_there_is_no_level_anywhere_for_students(client, logged_in):
    for path in ["/learn/", "/practice/", "/settings/", "/solve", "/home", "/learn/algebra-1"]:
        page = logged_in.get(path).get_data(as_text=True)
        assert 'name="level"' not in page and "?level=" not in page and "High School" not in page and "College<" not in page, path
    learn = logged_in.get("/learn/").get_data(as_text=True)
    assert learn.index("Whole Numbers") < learn.index("Algebra I") < learn.index("Linear Algebra")
    practice = logged_in.get("/practice/").get_data(as_text=True)
    assert practice.index("Adding and subtracting") < practice.index("Derivatives")
    logged_in.post("/logout")
    signup = client.get("/signup").get_data(as_text=True)
    assert 'name="level"' not in signup and "Your level" not in signup
