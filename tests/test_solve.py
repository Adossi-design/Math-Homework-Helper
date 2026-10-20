"""Solving, the library, saving, deleting and the tutor chat."""
import io

from mathhelper import ai
from mathhelper.extensions import db
from mathhelper.models import Solution

JSON = {"Accept": "application/json"}


def solve_typed(client, text="Solve 2x + 3 = 11"):
    return client.post("/solve", data={"mode": "type", "problem": text})


def test_typed_problem_is_solved_and_saved(app, logged_in):
    response = solve_typed(logged_in)
    assert response.status_code == 302 and "/solutions/" in response.location
    page = logged_in.get(response.location).get_data(as_text=True)
    assert "Subtract 3" in page and "$x = 4$" in page and "Undo addition" in page
    with app.app_context():
        solution = db.session.scalar(db.select(Solution))
        assert solution.topic == "Algebra" and solution.prompt == "Solve 2x + 3 = 11"


def test_empty_typed_problem_is_rejected(logged_in):
    response = logged_in.post("/solve", data={"mode": "type", "problem": " "})
    assert response.status_code == 400
    assert "Type the problem" in response.get_data(as_text=True)


def test_photo_is_stored_and_only_owner_can_see_it(app, logged_in, client, make_user, png_bytes):
    response = logged_in.post("/solve", data={"mode": "photo", "photo": (io.BytesIO(png_bytes), "hw.png")},
                              content_type="multipart/form-data")
    assert response.status_code == 302
    with app.app_context():
        name = db.session.scalar(db.select(Solution.image_name))
    photo = logged_in.get(f"/uploads/{name}")
    assert photo.status_code == 200 and photo.mimetype == "image/jpeg"

    stranger = app.test_client()
    make_user(email="other@example.com")
    stranger.post("/login", data={"email": "other@example.com", "password": "secret123"})
    assert stranger.get(f"/uploads/{name}").status_code == 404
    assert stranger.get("/solutions/1").status_code == 404


def test_non_image_upload_gets_a_friendly_error(logged_in):
    response = logged_in.post("/solve", data={"mode": "photo", "photo": (io.BytesIO(b"not an image"), "notes.txt")},
                              content_type="multipart/form-data")
    assert response.status_code == 400
    assert "does not look like a photo" in response.get_data(as_text=True)


def test_ai_failure_keeps_the_typed_text(logged_in, monkeypatch):
    def broken(text, profile=""):
        raise ai.AIError("The AI service is very busy right now.")
    monkeypatch.setattr(ai, "solve_text", broken)
    response = solve_typed(logged_in, "Solve 9x = 18")
    html = response.get_data(as_text=True)
    assert response.status_code == 503 and "very busy" in html and "Solve 9x = 18" in html


def test_no_problem_found_is_not_saved(app, logged_in, monkeypatch):
    monkeypatch.setattr(ai, "solve_text", lambda text, profile="": ai.SolveResult(problems=[], note="That is not a math question."))
    response = solve_typed(logged_in, "What is the capital of Ghana?")
    assert response.status_code == 422 and "not a math question" in response.get_data(as_text=True)
    with app.app_context():
        assert db.session.scalar(db.select(db.func.count()).select_from(Solution)) == 0


def test_hourly_limit(app, logged_in):
    app.config["SOLVES_PER_HOUR"] = 1
    solve_typed(logged_in)
    assert solve_typed(logged_in).status_code == 429


def test_star_delete_and_library_filters(logged_in):
    solve_typed(logged_in)
    assert logged_in.post("/solutions/1/star", headers=JSON).get_json() == {"starred": True}
    assert "Solve 2x" in logged_in.get("/library?tab=saved").get_data(as_text=True)
    assert "Solve 2x" in logged_in.get("/library?q=2x").get_data(as_text=True)
    assert "Nothing matches" in logged_in.get("/library?q=integral").get_data(as_text=True)
    assert "Nothing matches" in logged_in.get("/library?topic=Calculus").get_data(as_text=True)
    assert logged_in.post("/solutions/1/delete").status_code == 302
    assert logged_in.get("/solutions/1").status_code == 404


def test_tutor_chat_saves_both_turns(app, logged_in):
    solve_typed(logged_in)
    reply = logged_in.post("/solutions/1/ask", json={"question": "Why subtract first?"}, headers=JSON)
    html = reply.get_json()["html"]
    assert "Why subtract first?" in html and "<strong>Why subtract first?</strong>" in html and "$x^2$" in html
    with app.app_context():
        assert len(db.session.get(Solution, 1).messages) == 2
    assert logged_in.post("/solutions/1/ask", json={"question": ""}, headers=JSON).status_code == 400


def test_solution_shows_the_full_working_then_each_line_with_its_explanation(app, logged_in):
    logged_in.post("/solve", data={"mode": "type", "problem": "2x + 3 = 11"})
    page = logged_in.get("/solutions/1").get_data(as_text=True)
    working = page[page.index('class="working"'):page.index("steps-label")]
    assert [line in working for line in ("$2x + 3 = 11$", "$2x = 8$", "$x = 4$")] == [True, True, True]
    assert working.index("$2x + 3 = 11$") < working.index("$2x = 8$") < working.index("$x = 4$")
    steps = page[page.index('<ol class="steps">'):]
    assert steps.index('class="step-result">$2x = 8$') < steps.index("Subtract 3") < steps.index("Take $3$ from both sides.")


def test_step_by_step_mode_reveals_working_lines_with_their_steps(app, logged_in):
    logged_in.post("/settings/preferences", data={"theme": "system"})
    logged_in.post("/solve", data={"mode": "type", "problem": "2x + 3 = 11"})
    page = logged_in.get("/solutions/1").get_data(as_text=True)
    assert 'data-step-line="-1"' in page and page.count("working-line  is-hidden") + page.count("is-last is-hidden") == 2


def test_older_solutions_without_working_still_show(app, logged_in):
    from mathhelper.extensions import db
    from mathhelper.models import Solution
    with app.app_context():
        db.session.add(Solution(user_id=1, source="type", prompt="1+1", topic="Arithmetic", problems=[
            {"problem": "Add $1 + 1$", "topic": "Arithmetic", "answer": "$2$", "steps": [{"title": "Count", "work": "One and one make two."}], "tip": ""}]))
        db.session.commit()
    page = logged_in.get("/solutions/1").get_data(as_text=True)
    assert "<h4>Count</h4>" in page and 'class="working"' not in page and "One and one make two." in page
