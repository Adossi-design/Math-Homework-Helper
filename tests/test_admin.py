"""The admin account and dashboard: access control, users and practice."""
import sqlite3
from html import unescape

from sqlalchemy import select

from mathhelper import create_app, schema
from mathhelper.extensions import db
from mathhelper.models import PracticeAttempt, SavedPractice, Solution, User

STUDENT = {"email": "ama@example.com", "password": "secret123"}
PRACTICE = {
    "title": "Times tables", "blurb": "Quick multiplication facts.", "topic": "Arithmetic", "published": "on",
    "fr_title": "Tables de multiplication",
    "q-0-prompt": "What is $3 \\times 4$?", "q-0-choice-0": "$12$", "q-0-choice-1": "$7$", "q-0-choice-2": "$34$", "q-0-answer": "0",
    "q-0-explanation": "Three groups of four.", "q-0-fr-prompt": "Combien font $3 \\times 4$ ?",
    "q-1-prompt": "What is $5 \\times 5$?", "q-1-choice-0": "$10$", "q-1-choice-1": "$25$", "q-1-answer": "1",
    "q-4-prompt": "What is $2 \\times 9$?", "q-4-choice-0": "$11$", "q-4-choice-2": "$18$", "q-4-choice-3": "$29$", "q-4-answer": "2",
}
PAGES = ["/admin/", "/admin/users", "/admin/practice", "/admin/practice/new", "/admin/practice/slope/edit",
         "/admin/practice/slope/preview"]
STUDENT_PAGES = ["/home", "/solve", "/library", "/curriculum/", "/practice/",
                 "/practice/slope", "/practice/results/1"]


def page(response):
    """Return the readable text of a response."""
    return unescape(response.get_data(as_text=True))


def test_admin_pages_and_actions_are_closed_to_everyone_else(app, admin, logged_in):
    visitor = app.test_client()
    for path in PAGES:
        assert visitor.get(path).status_code == 302 and "/login" in visitor.get(path).location, path
        assert logged_in.get(path).status_code == 403, path
        assert admin.get(path).status_code == 200, path
    actions = ["/admin/users/1/suspend", "/admin/users/1/delete", "/admin/users/1/reactivate", "/admin/practice/new",
               "/admin/practice/slope/edit", "/admin/practice/slope/delete"]
    for path in actions:
        assert logged_in.post(path, data=PRACTICE).status_code == 403, path
        assert visitor.post(path, data=PRACTICE).status_code == 302, path
    with app.app_context():
        assert db.session.scalar(select(SavedPractice)) is None
        assert db.session.scalar(select(User).where(User.email == STUDENT["email"])).is_active
    assert "/admin/" not in logged_in.get("/home").get_data(as_text=True)


def test_the_admin_only_sees_the_dashboard_and_never_the_student_pages(app, admin):
    for path in STUDENT_PAGES:
        response = admin.get(path)
        assert response.status_code == 302 and response.location.endswith("/admin/"), path
    assert admin.get("/").location.endswith("/admin/")
    overview = page(admin.get("/admin/"))
    for link in ['href="/home"', 'href="/solve"', 'href="/library"', 'href="/curriculum/"', 'href="/practice/"', "assignments"]:
        assert link not in overview, link
    for link in ['href="/admin/users"', 'href="/admin/practice"', 'href="/settings/"', "/logout"]:
        assert link in overview, link
    assert '"welcome": false' in overview
    settings = page(admin.get("/settings/"))
    assert 'name="level"' not in settings and 'name="sounds"' not in settings and "Delete account" not in settings
    browser = app.test_client()
    landing = browser.post("/login", data={"email": "boss@example.com", "password": "correct-horse-battery"})
    assert landing.location.endswith("/admin/")


def test_there_is_exactly_one_admin_and_a_new_admin_password_setting_is_applied_once(app, make_user):
    make_user()
    with app.app_context():
        schema.ensure_admin("boss@example.com", "short")
        assert db.session.scalar(select(User).where(User.email == "boss@example.com")) is None
        schema.ensure_admin("boss@example.com", "correct-horse-battery")
        boss = db.session.scalar(select(User).where(User.email == "boss@example.com"))
        assert boss.is_admin and boss.check_password("correct-horse-battery")
        boss.set_password("changed-in-settings")
        db.session.commit()
        schema.ensure_admin("boss@example.com", "correct-horse-battery")
        assert boss.check_password("changed-in-settings")
        schema.ensure_admin("boss@example.com", "new-pass-11")
        assert boss.check_password("new-pass-11")
        student = db.session.scalar(select(User).where(User.email == STUDENT["email"]))
        student.is_admin = True
        db.session.commit()
        schema.ensure_admin("boss@example.com", "correct-horse-battery")
        assert [user.email for user in db.session.scalars(select(User).where(User.is_admin.is_(True)))] == ["boss@example.com"]


def test_a_new_admin_password_also_lifts_a_login_lockout(app, admin):
    for _attempt in range(6):
        app.test_client().post("/login", data={"email": "boss@example.com", "password": "wrong-guess"})
    browser = app.test_client()
    assert browser.post("/login", data={"email": "boss@example.com", "password": "correct-horse-battery"}).status_code == 429
    with app.app_context():
        schema.ensure_admin("boss@example.com", "fresh-password")
    assert browser.post("/login", data={"email": "boss@example.com", "password": "fresh-password"}).status_code == 302


def test_an_older_database_gets_the_new_columns(tmp_path):
    path = tmp_path / "old.db"
    old = sqlite3.connect(path)
    old.execute('CREATE TABLE "user" (id INTEGER PRIMARY KEY, name VARCHAR(80) NOT NULL, email VARCHAR(255) NOT NULL UNIQUE, '
                "password_hash VARCHAR(255), google_id VARCHAR(64), level VARCHAR(20) NOT NULL, theme VARCHAR(10) NOT NULL, "
                "expand_steps BOOLEAN NOT NULL, sounds BOOLEAN NOT NULL, timezone VARCHAR(64) NOT NULL, created_at DATETIME NOT NULL)")
    old.execute("INSERT INTO user VALUES (1, 'Old Timer', 'old@example.com', NULL, NULL, 'College', 'system', 1, 1, 'UTC', '2026-01-01 00:00:00')")
    old.commit()
    old.close()
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": f"sqlite:///{path}", "WTF_CSRF_ENABLED": False,
                      "ADMIN_EMAIL": "boss@example.com", "ADMIN_PASSWORD": "correct-horse-battery"})
    with app.app_context():
        veteran = db.session.scalar(select(User).where(User.email == "old@example.com"))
        assert veteran.is_admin is False and veteran.suspended_at is None
        assert db.session.scalar(select(User).where(User.email == "boss@example.com")).is_admin
    browser = app.test_client()
    assert browser.post("/login", data={"email": "boss@example.com", "password": "correct-horse-battery"}).status_code == 302
    assert browser.get("/admin/users").status_code == 200


def test_retired_assignment_tables_are_dropped_only_when_empty(tmp_path):
    for rows, kept in ((0, False), (1, True)):
        path = tmp_path / f"retired{rows}.db"
        old = sqlite3.connect(path)
        old.execute("CREATE TABLE assignment (id INTEGER PRIMARY KEY, title VARCHAR(120))")
        old.execute("CREATE TABLE assignment_completion (id INTEGER PRIMARY KEY, user_id INTEGER, assignment_id INTEGER)")
        if rows:
            old.execute("INSERT INTO assignment VALUES (1, 'Week 1')")
            old.execute("INSERT INTO assignment_completion VALUES (1, 1, 1)")
        old.commit()
        old.close()
        app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": f"sqlite:///{path}", "ADMIN_EMAIL": "", "ADMIN_PASSWORD": ""})
        with app.app_context():
            names = set(db.inspect(db.engine).get_table_names())
            assert ({"assignment", "assignment_completion"} <= names) == kept
            if kept:
                user = User(name="Old", email="old@example.com")
                db.session.add(user)
                db.session.commit()
                from mathhelper.accounts import delete_user
                delete_user(user)
                db.session.commit()
                assert db.session.get(User, user.id) is None


def test_admin_can_suspend_reactivate_and_delete_a_user(app, admin, logged_in):
    with app.app_context():
        student = db.session.scalar(select(User.id).where(User.email == STUDENT["email"]))
        boss = db.session.scalar(select(User.id).where(User.is_admin.is_(True)))
    logged_in.post("/solve", data={"mode": "type", "problem": "2x + 3 = 11"})
    listing = page(admin.get("/admin/users?q=ama"))
    assert "ama@example.com" in listing and "Ama Mensah" in listing and "1 solution" in listing and "High School" not in listing

    notice = page(admin.post(f"/admin/users/{student}/suspend", follow_redirects=True))
    assert "can no longer sign in" in notice and "Reactivate" in notice
    assert logged_in.get("/home").status_code == 302
    blocked = logged_in.post("/login", data=STUDENT)
    assert blocked.status_code == 403 and "This account is suspended" in page(blocked)
    assert "ama@example.com" in page(admin.get("/admin/users?status=suspended"))
    assert "ama@example.com" not in page(admin.get("/admin/users?status=active"))

    admin.post(f"/admin/users/{student}/reactivate")
    assert logged_in.post("/login", data=STUDENT).status_code == 302 and logged_in.get("/home").status_code == 200

    assert admin.post(f"/admin/users/{boss}/suspend").status_code == 403 and admin.post(f"/admin/users/{boss}/delete").status_code == 403
    assert admin.post("/admin/users/99/delete").status_code == 404
    assert "all of their data were deleted" in page(admin.post(f"/admin/users/{student}/delete", follow_redirects=True))
    with app.app_context():
        assert db.session.get(User, student) is None and db.session.scalar(select(Solution)) is None
    assert logged_in.get("/home").status_code == 302


def test_admin_cannot_delete_or_rename_the_admin_account_in_settings(app, admin):
    assert "cannot be deleted" in page(admin.post("/settings/delete-account", data={"password": "correct-horse-battery"}, follow_redirects=True))
    admin.post("/settings/profile", data={"name": "Boss", "email": "other@example.com"})
    with app.app_context():
        assert db.session.scalar(select(User).where(User.is_admin.is_(True))).email == "boss@example.com"


def test_admin_writes_edits_and_deletes_practice_sets_that_students_play(app, admin, logged_in):
    assert "at least 3 questions" in page(admin.post("/admin/practice/new", data={**PRACTICE, "q-4-prompt": "", "q-4-choice-0": "",
                                                                                     "q-4-choice-2": "", "q-4-choice-3": ""}))
    broken = page(admin.post("/admin/practice/new", data={**PRACTICE, "q-1-answer": "3"}))
    assert "Question 2 needs" in broken and "What is $5 \\times 5$?" in broken
    assert "English title and description" in page(admin.post("/admin/practice/new", data={**PRACTICE, "blurb": ""}))
    assert "Practice set published" in page(admin.post("/admin/practice/new", data=PRACTICE, follow_redirects=True))
    with app.app_context():
        row = db.session.scalar(select(SavedPractice))
        assert row.skill_id == "set-times-tables" and len(row.questions) == 3
        assert row.questions[2]["en"]["choices"] == ["$11$", "$18$", "$29$"] and row.questions[2]["answer"] == 1

    catalog = page(logged_in.get("/practice/"))
    assert "Times tables" in catalog and "Quick multiplication facts." in catalog
    round_page = page(logged_in.get("/practice/set-times-tables"))
    assert "Three groups of four." in round_page and round_page.count('"answer":') == 3
    seed = "0123456789abcdef"
    with app.test_request_context():
        from mathhelper.practice import build_round
        from mathhelper.practice.catalog import find_skill
        questions = build_round("set-times-tables", seed, skill=find_skill("set-times-tables"))
    perfect = ",".join(str(q.answer) for q in questions)
    result = logged_in.post("/practice/set-times-tables/finish", data={"seed": seed, "answers": perfect}, follow_redirects=True)
    assert "3/3" in page(result)
    assert "Best 3/3 in 1 round" in page(logged_in.get("/practice/"))
    logged_in.get("/language/fr")
    french = page(logged_in.get("/practice/"))
    assert "Tables de multiplication" in french and "Quick multiplication facts." in french
    assert "Combien font" in page(logged_in.get("/practice/set-times-tables"))
    logged_in.get("/language/en")

    preview = page(admin.get("/admin/practice/set-times-tables/preview"))
    assert "What is $3 \\times 4$?" in preview and preview.count("preview-choice is-correct") == 3
    form = page(admin.get("/admin/practice/set-times-tables/edit"))
    assert 'value="$25$"' in form and "Tables de multiplication" in form
    changed = {**PRACTICE, "title": "Times tables, harder", "published": ""}
    assert "Practice set updated" in page(admin.post("/admin/practice/set-times-tables/edit", data=changed, follow_redirects=True))
    assert logged_in.get("/practice/set-times-tables").status_code == 404
    assert "Quick multiplication facts." not in page(logged_in.get("/practice/"))
    admin.post("/admin/practice/set-times-tables/edit", data=PRACTICE)

    assert "Practice set deleted" in page(admin.post("/admin/practice/set-times-tables/delete", follow_redirects=True))
    assert logged_in.get("/practice/set-times-tables").status_code == 404
    with app.app_context():
        assert db.session.scalar(select(SavedPractice)) is None and db.session.scalar(select(PracticeAttempt)) is None
    assert admin.post("/admin/practice/set-times-tables/delete").status_code == 404


def test_admin_renames_hides_and_restores_a_built_in_practice_set(admin, logged_in):
    form = page(admin.get("/admin/practice/slope/edit"))
    assert "Slope" in form and "makes new questions automatically" in form and "q-0-prompt" not in form
    renamed = {"title": "Slopes of lines", "blurb": "Rise over run.", "topic": "Functions", "published": "on"}
    assert "Practice set updated" in page(admin.post("/admin/practice/slope/edit", data=renamed, follow_redirects=True))
    assert "Slopes of lines" in page(logged_in.get("/practice/"))
    assert logged_in.get("/practice/slope").status_code == 200
    admin.post("/admin/practice/slope/delete")
    assert logged_in.get("/practice/slope").status_code == 404 and "Slopes of lines" not in page(logged_in.get("/practice/"))
    assert logged_in.get("/home").status_code == 200
    admin.post("/admin/practice/slope/restore")
    restored = page(logged_in.get("/practice/"))
    assert "Slope" in restored and "Slopes of lines" not in restored


def test_admin_dashboard_shows_the_numbers_in_french_too(admin, logged_in):
    logged_in.post("/solve", data={"mode": "type", "problem": "2x + 3 = 11"})
    overview = page(admin.get("/admin/"))
    assert "Newest users" in overview and "ama@example.com" in overview and "Quick actions" in overview and "This week" in overview
    listing = page(admin.get("/admin/users"))
    assert listing.count('<div class="admin-row') == 1 and "ama@example.com" in listing
    admin.get("/language/fr")
    for path in PAGES:
        assert admin.get(path).status_code == 200, path
    french = page(admin.get("/admin/"))
    assert "Vue d'ensemble" in french and "Utilisateurs" in french and "Derniers inscrits" in french
