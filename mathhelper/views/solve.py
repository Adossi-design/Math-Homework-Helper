"""Solving problems, viewing solutions and chatting with the tutor."""
from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from .. import ai, mascot
from ..curriculum.context import profile
from ..extensions import db
from ..images import ImageError, delete_image, prepare_image, save_image
from ..models import Message, Solution
from .helpers import owned_solution, questions_last_hour, solves_last_hour, wants_json

from ..i18n import gettext as _

bp = Blueprint("solve", __name__)

MAX_PROBLEM_LENGTH = 2000
MAX_QUESTION_LENGTH = 1000
EXAMPLES = [
    "Solve 3x - 7 = 11",
    "What is 2/3 + 5/6?",
    "Find the derivative of x^3 sin(x)",
    "A circle has radius 4 cm. Find its area.",
]


def solve_form(mode="photo", text="", error=None, status=200):
    """Render the solve page, keeping whatever the student typed."""
    return render_template("solve/new.html", mode=mode, text=text, error=error, examples=[_(e) for e in EXAMPLES]), status


@bp.get("/solve")
@login_required
def new():
    mode = "type" if request.args.get("mode") == "type" else "photo"
    return solve_form(mode, request.args.get("q", "")[:MAX_PROBLEM_LENGTH])


@bp.post("/solve")
@login_required
def create():
    mode = "type" if request.form.get("mode") == "type" else "photo"
    text = request.form.get("problem", "").strip()[:MAX_PROBLEM_LENGTH]
    if solves_last_hour(current_user) >= current_app.config["SOLVES_PER_HOUR"]:
        return solve_form(mode, text, _("You have solved a lot this hour. Take a short break and try again soon."), 429)

    # Read the input and ask the AI.
    image_bytes = None
    try:
        if mode == "photo":
            upload = request.files.get("photo")
            if not upload or not upload.filename:
                return solve_form(mode, text, _("Choose or take a photo of your problem first."), 400)
            image_bytes = prepare_image(upload.stream)
            result = ai.solve_image(image_bytes, profile(current_user))
        else:
            if len(text) < 2:
                return solve_form(mode, text, _("Type the problem you want solved."), 400)
            result = ai.solve_text(text, profile(current_user))
    except ImageError as exc:
        return solve_form(mode, text, str(exc), 400)
    except ai.AIError as exc:
        return solve_form(mode, text, str(exc), 503)

    if not result.problems:
        message = result.note or _("No math problem was found. Try a clearer photo or type the problem.")
        return solve_form(mode, text, message, 422)

    # Save the solution so it shows up in the library.
    problems = [p.model_dump() for p in result.problems]
    solution = Solution(
        user_id=current_user.id,
        source=mode,
        prompt=text if mode == "type" else None,
        image_name=save_image(image_bytes) if image_bytes else None,
        problems=problems,
        topic=problems[0]["topic"],
        note=result.note or None,
    )
    db.session.add(solution)
    db.session.commit()
    mascot.queue("completed")
    return redirect(url_for("solve.show", solution_id=solution.id))


@bp.get("/solutions/<int:solution_id>")
@login_required
def show(solution_id):
    solution = owned_solution(solution_id)
    prompts = [_("Explain this more simply"), _("Why does the first step work?"), _("Give me a similar problem to try")]
    return render_template("solve/show.html", solution=solution, prompts=prompts)


@bp.post("/solutions/<int:solution_id>/star")
@login_required
def star(solution_id):
    solution = owned_solution(solution_id)
    solution.starred = not solution.starred
    db.session.commit()
    if wants_json():
        return {"starred": solution.starred}
    flash(_("Saved to your library.") if solution.starred else _("Removed from saved."), "success")
    return redirect(url_for("solve.show", solution_id=solution.id))


@bp.post("/solutions/<int:solution_id>/delete")
@login_required
def delete(solution_id):
    solution = owned_solution(solution_id)
    delete_image(solution.image_name)
    db.session.delete(solution)
    db.session.commit()
    flash(_("Solution deleted."), "info")
    return redirect(url_for("library.index"))


@bp.post("/solutions/<int:solution_id>/ask")
@login_required
def ask(solution_id):
    solution = owned_solution(solution_id)
    payload = request.get_json(silent=True)
    payload = payload if isinstance(payload, dict) else request.form
    question = payload.get("question")
    question = question.strip() if isinstance(question, str) else ""
    if not question:
        return {"error": _("Type a question for the tutor first.")}, 400
    if len(question) > MAX_QUESTION_LENGTH:
        return {"error": _("Please keep your question under 1000 characters.")}, 400
    if questions_last_hour(current_user) >= current_app.config["QUESTIONS_PER_HOUR"]:
        return {"error": _("You have asked a lot of questions this hour. Please try again a little later.")}, 429

    history = [(m.role, m.content) for m in solution.messages]
    try:
        reply = ai.ask_tutor(solution.problems, history, question, profile(current_user))
    except ai.AIError as exc:
        return {"error": str(exc)}, 503

    asked, answered = Message(role="user", content=question), Message(role="assistant", content=reply)
    solution.messages.extend([asked, answered])
    db.session.commit()
    return {"html": render_template("solve/_messages.html", messages=[asked, answered])}
