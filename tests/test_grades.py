"""School classes: choosing one, solving at its level, and lessons and practice chosen for it."""
from html import unescape

from flask import g

from mathhelper import ai
from mathhelper.ai import ask_tutor as real_ask_tutor
from mathhelper.content import COURSES
from mathhelper.extensions import db
from mathhelper.grades import GRADE_IDS, LESSON_GRADES, lesson_grade, lessons_for
from mathhelper.models import SavedLesson, User


def test_every_built_in_lesson_has_a_class_and_every_class_has_lessons():
    keys = {f"{course.id}/{lesson.id}" for course in COURSES for lesson in course.lessons}
    assert keys == set(LESSON_GRADES) and set(LESSON_GRADES.values()) <= set(GRADE_IDS)
    for grade in GRADE_IDS:
        assert lessons_for(COURSES, grade), grade


def test_a_student_without_a_class_is_asked_first(app, client, make_user):
    make_user(grade=None)
    client.post("/login", data={"email": "ama@example.com", "password": "secret123"})
    for path in ["/home", "/solve", "/learn/", "/practice/", "/library", "/settings/"]:
        response = client.get(path)
        assert response.status_code == 302 and "/settings/class" in response.location, path
    page = unescape(client.get("/settings/class").get_data(as_text=True))
    assert "Which class are you in?" in page and "CM1 (Huitième)" in page and "Terminale" in page and "University" in page
    assert client.get("/about").status_code == 200

    wrong = client.post("/settings/class", data={"grade": "Grade 99"}, follow_redirects=True).get_data(as_text=True)
    assert "Choose your class." in wrong
    response = client.post("/settings/class?next=/learn/", data={"grade": "5e"})
    assert response.location.endswith("/learn/")
    with app.app_context():
        assert db.session.scalar(db.select(User.grade)) == "5e"
    assert client.get("/home").status_code == 200


def test_the_class_can_be_changed_in_settings(app, logged_in):
    settings = logged_in.get("/settings/").get_data(as_text=True)
    assert 'name="grade"' in settings and '<option value="4e" selected>' in settings
    response = logged_in.post("/settings/class?next=/settings/%23class", data={"grade": "tle"}, follow_redirects=True)
    assert "Your class is now Terminale." in response.get_data(as_text=True)
    with app.app_context():
        assert db.session.scalar(db.select(User.grade)) == "tle"


def test_the_admin_is_never_asked_for_a_class(admin):
    assert admin.get("/admin/").status_code == 200
    assert 'name="grade"' not in admin.get("/settings/").get_data(as_text=True)


def test_learn_shows_the_lessons_of_the_students_class(logged_in):
    page = unescape(logged_in.get("/learn/").get_data(as_text=True))
    assert "Lessons for your class" in page
    mine, earlier = page.split("Revise earlier classes")
    assert "Solving linear equations" in mine and "The Pythagorean theorem" in mine and "Exponent rules" in mine
    assert "Negative numbers" not in mine and "Negative numbers" in earlier and "Place value" in earlier
    assert "Derivative rules" not in page and "Logarithms" not in page
    assert "Up next in" in page and "Proportions" in page

    other = unescape(logged_in.get("/learn/?class=1ere").get_data(as_text=True))
    assert "Lessons for Première" in other and "Derivative rules" in other and "Solutions still follow your own class" in other
    assert "Solving linear equations" in other.split("Revise earlier classes")[1]
    course = logged_in.get("/learn/calculus-1").get_data(as_text=True)
    assert ">Tle<" in course and ">1ère<" in course


def test_home_and_practice_follow_the_class(logged_in):
    home = unescape(logged_in.get("/home").get_data(as_text=True))
    assert "Proportions" in home and "Whole Numbers" not in home
    practice = unescape(logged_in.get("/practice/").get_data(as_text=True))
    mine, more = practice.split("More practice")
    assert "For your class" in mine and "Linear equations" in mine and "Pythagorean theorem" in mine
    assert "Derivatives" not in mine and "Derivatives" in more


def test_solving_and_the_tutor_get_the_students_class(logged_in, monkeypatch):
    seen = []
    monkeypatch.setattr(ai, "solve_text", lambda text, grade=None: seen.append(grade) or ai.SolveResult(problems=[
        ai.Problem(problem="p", topic="Algebra", answer="a", steps=[])]))
    monkeypatch.setattr(ai, "ask_tutor", lambda problems, history, question, grade=None: seen.append(grade) or "ok")
    response = logged_in.post("/solve", data={"mode": "type", "problem": "3x - 2 = x + 6"})
    logged_in.post(response.location + "/ask", json={"question": "Why?"})
    assert seen == ["4e", "4e"]


def test_the_ai_is_told_the_methods_of_the_class(app, monkeypatch):
    seen = {}

    def fake_run(contents, config, parse):
        seen["instructions"] = config.system_instruction
        return ai.SolveResult(problems=[])

    monkeypatch.setattr(ai, "_run", fake_run)
    with app.test_request_context("/"):
        g.lang = "en"
        ai._solve(["2+2"], "6e")
        text = seen["instructions"]
        assert "Sixième" in text and "French school system" in text and "No negative numbers" in text
        assert "Never use a method from a later class" in text and '"note"' in text and "teachers" not in text
        ai._solve(["2+2"], "1ere")
        assert "discriminant" in seen["instructions"] and "Sixième" not in seen["instructions"]
        ai._solve(["2+2"], None)
        assert "teachers" in seen["instructions"] and "French school system" not in seen["instructions"]
        real_ask_tutor([], [], "Why?", "cm2")
        assert "CM2 (Septième)" in seen["instructions"] and "later class" in seen["instructions"]


def test_the_admin_chooses_the_class_of_a_new_lesson(app, admin, logged_in):
    form = {"course_id": "algebra-1", "skill": "linear-equations", "minutes": "5", "published": "on", "grade": "4e",
            "title": "Equations with brackets", "intro": "i", "points": "p", "problem": "q", "steps": "s",
            "answer": "a", "mistake": "m"}
    assert "Students in this class find the lesson" in admin.get("/admin/lessons/new").get_data(as_text=True)
    admin.post("/admin/lessons/new", data=form)
    with app.app_context():
        row = db.session.scalar(db.select(SavedLesson))
        assert row.grade == "4e" and lesson_grade("algebra-1", row) == "4e"
    assert "Equations with brackets" in logged_in.get("/learn/").get_data(as_text=True).split("Revise earlier classes")[0]
    assert "Equations with brackets" not in logged_in.get("/learn/?class=1ere").get_data(as_text=True).split("Revise")[0]
    assert "Equations with brackets" not in logged_in.get("/learn/?class=6e").get_data(as_text=True)
