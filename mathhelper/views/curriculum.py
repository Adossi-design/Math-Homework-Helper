"""Curriculum chapters: lessons, guided exercises, practice, assessments and progress."""
import random
import re
import secrets
from datetime import timedelta
from fractions import Fraction

from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import delete, func, select
from sqlalchemy.exc import IntegrityError

from .. import ai, mascot
from ..curriculum import COUNTRIES, available_levels, chapters_for, country, find_chapter, label, level, valid_choice
from ..curriculum.checker import MAX_LENGTH, check, show
from ..curriculum.context import done_keys, lesson_text, profile, section_key
from ..curriculum.progress import PASS_MARK, chapter_progress, grade
from ..curriculum.translate import localize, walk
from ..extensions import db
from ..i18n import gettext as _
from ..i18n import language, polish
from ..models import ChapterAttempt, ExerciseResult, LessonCompletion, TutorQuestion, utcnow

bp = Blueprint("curriculum", __name__, url_prefix="/curriculum")

MAX_QUESTION_LENGTH = 1000
SEED = re.compile(r"[A-Za-z0-9]{4,16}")
MESSAGES = {
    "unreadable": "I could not read that answer. Write a number such as 3,5 or 7/2.",
    "unreadable_list": "I could not read that answer. Write the numbers separated by semicolons, such as 1,2 ; 1,5 ; 2.",
    "unreadable_choice": "Choose one of the answers first.",
    "fraction": "Write it as a fraction, such as 235/100.",
    "decimal_fraction": "Write it as a fraction whose denominator is 10, 100, 1000 and so on, such as 235/100.",
    "decimal": "Write it as a decimal number with a comma.",
    "wrong": "Not quite. Try again, or open a hint.",
    "right": "Correct!",
}


def math(value):
    """Write an exact number as math with a decimal comma, ready to be shown in either language."""
    return "$" + show(value).replace(",", "{,}") + "$"


def present(chapter, tree):
    """Return the content in the student's language, and whether any of it stayed in the original language."""
    lang = language()
    result = localize(tree, chapter.language, lang)
    content = walk(result.content, lambda text: polish(text, "fr")) if lang == "fr" else result.content
    return content, result.fallback


def exercise_view(exercise):
    """Describe an exercise for a page, without its answer and without its solution."""
    return {"id": exercise.id, "concept": exercise.concept, "kind": exercise.answer.kind, "prompt": exercise.prompt,
            "options": exercise.options, "hints": exercise.hints, "level": exercise.level, "form": exercise.answer.form}


def section_view(section):
    """Describe a lesson section for a page. The 'verify' expressions used by the tests stay on the server."""
    return {"id": section.id, "title": section.title, "goal": section.goal, "minutes": section.minutes,
            "blocks": [{k: v for k, v in block.items() if k != "verify"} for block in section.blocks],
            "guided": [exercise_view(e) for e in section.guided]}


def chapter_view(chapter):
    """Describe a chapter overview for a page."""
    return {"title": chapter.title, "intro": chapter.intro, "objectives": chapter.objectives, "status_note": chapter.status_note,
            "prerequisites": [{"text": p["text"], "course": p["course"], "lesson": p["lesson"]} for p in chapter.prerequisites],
            "sections": [{"id": s.id, "title": s.title, "goal": s.goal, "minutes": s.minutes} for s in chapter.sections],
            "concepts": {key: name for key, (name, _section) in chapter.concepts.items()}}


def load(chapter_id, section_id=None):
    """Return the chapter (and section) for a URL or stop with 404."""
    chapter = find_chapter(chapter_id)
    if chapter is None:
        abort(404)
    if section_id is None:
        return chapter, None
    section = chapter.section(section_id)
    if section is None:
        abort(404)
    return chapter, section


def exercise_by_id(exercise_id):
    """Find a fixed exercise from its id, or return None."""
    if not isinstance(exercise_id, str):
        return None, None
    chapter = find_chapter(exercise_id.split("/")[0])
    return (chapter, chapter.exercises().get(exercise_id)) if chapter else (None, None)


def chosen_level():
    """Return the country and level to show: the one in the address when valid, else the student's own."""
    asked_country, asked_level = request.args.get("country", ""), request.args.get("grade", "")
    if asked_country and asked_level and valid_choice(asked_country, asked_level):
        return asked_country, asked_level
    return current_user.country, current_user.grade


def solved_ids(user):
    """Return the ids of the curriculum exercises this student has solved."""
    return set(db.session.scalars(select(ExerciseResult.exercise_id).where(ExerciseResult.user_id == user.id, ExerciseResult.solved.is_(True))))


def question_text(exercise, verdict):
    """Return the message for a checked answer."""
    kind = exercise.answer.kind
    if verdict.status == "unreadable":
        return _(MESSAGES["unreadable_choice" if kind == "choice" else "unreadable_list" if kind == "numbers" else "unreadable"])
    if verdict.status == "wrong_form":
        return _(MESSAGES[exercise.answer.form])
    return _(MESSAGES["right" if verdict.status == "correct" else "wrong"])


def note_for(exercise, given):
    """Return the explanation for a typical wrong answer to an exercise, or an empty string."""
    if exercise.answer.kind == "choice":
        verdict = check(exercise.answer, given)
        return exercise.wrong.get(verdict.value, "") if verdict.status == "wrong" else ""
    value = check(exercise.answer, given).value
    return exercise.wrong.get(show(value), "") if isinstance(value, Fraction) else ""


def answer_text(exercise, options):
    """Write the correct answer of an exercise so it can be shown after an assessment."""
    answer = exercise.answer
    if answer.kind == "choice":
        return options[answer.value]
    if answer.kind == "numbers":
        return " < ".join(math(v) for v in answer.value)
    if answer.kind == "between":
        return "Tout nombre strictement compris entre " + math(answer.value) + " et " + math(answer.high) + "."
    return math(answer.value)


@bp.get("/")
@login_required
def index():
    place_id, level_id = chosen_level()
    stage = level(place_id, level_id) if place_id else None
    chapters = chapters_for(place_id, level_id) if stage else []
    cards = []
    for chapter in chapters:
        view, _fallback = present(chapter, {"title": chapter.title, "intro": chapter.intro})
        cards.append({"chapter": chapter, "view": view, "progress": chapter_progress(current_user, chapter)})
    lang = language()
    offered = [(country(c), level(c, l)) for c, l in available_levels()]
    return render_template("curriculum/index.html", active_nav="learn", place=country(place_id), stage=stage, cards=cards, countries=COUNTRIES,
                           offered=offered, label=label, lang=lang, own=(place_id == current_user.country and level_id == current_user.grade))


@bp.get("/<chapter_id>")
@login_required
def chapter(chapter_id):
    chapter, _section = load(chapter_id)
    view, fallback = present(chapter, chapter_view(chapter))
    progress = chapter_progress(current_user, chapter)
    resume = next((s for s in chapter.sections if s.id not in progress["sections_done"]), None)
    foreign = bool(current_user.country and current_user.grade) and (current_user.country, current_user.grade) != (chapter.country, chapter.level)
    return render_template("curriculum/chapter.html", active_nav="learn", chapter=chapter, view=view, fallback=fallback, progress=progress,
                           resume=resume, foreign=foreign, place=country(chapter.country), stage=level(chapter.country, chapter.level),
                           sources=chapter.sources, label=label, lang=language(), passmark=PASS_MARK)


@bp.get("/<chapter_id>/s/<section_id>")
@login_required
def section(chapter_id, section_id):
    chapter, section = load(chapter_id, section_id)
    view, fallback = present(chapter, section_view(section))
    titles, _fb = present(chapter, {"chapter": chapter.title})
    index = chapter.sections.index(section)
    done = done_keys(current_user)
    history = list(db.session.scalars(
        select(TutorQuestion).where(TutorQuestion.user_id == current_user.id, TutorQuestion.section_key == section_key(chapter.id, section.id)).order_by(TutorQuestion.id)))
    return render_template("curriculum/section.html", active_nav="learn", chapter=chapter, section=section, view=view, fallback=fallback,
                           chapter_title=titles["chapter"], index=index, total=len(chapter.sections),
                           previous=chapter.sections[index - 1] if index else None,
                           upcoming=chapter.sections[index + 1] if index + 1 < len(chapter.sections) else None,
                           is_done=section_key(chapter.id, section.id) in done, solved=solved_ids(current_user), history=history,
                           prompts=[_("Explain this again"), _("Explain it in a simpler way"), _("Why does this work?"), _("Give me another example"), _("Give me another exercise like this one")])


@bp.post("/<chapter_id>/s/<section_id>/complete")
@login_required
def complete(chapter_id, section_id):
    chapter, section = load(chapter_id, section_id)
    key = section_key(chapter.id, section.id)
    existing = db.session.scalar(select(LessonCompletion).where(LessonCompletion.user_id == current_user.id, LessonCompletion.lesson_key == key))
    if existing:
        db.session.execute(delete(LessonCompletion).where(LessonCompletion.id == existing.id))
        db.session.commit()
        flash(_("Marked as not done."), "info")
        return redirect(url_for("curriculum.section", chapter_id=chapter.id, section_id=section.id))
    db.session.add(LessonCompletion(user_id=current_user.id, lesson_key=key))
    db.session.commit()
    mascot.queue("completed")
    index = chapter.sections.index(section)
    if index + 1 < len(chapter.sections):
        return redirect(url_for("curriculum.section", chapter_id=chapter.id, section_id=chapter.sections[index + 1].id))
    return redirect(url_for("curriculum.chapter", chapter_id=chapter.id))


@bp.get("/<chapter_id>/practice")
@login_required
def practice(chapter_id):
    chapter, _section = load(chapter_id)
    tree = {"title": chapter.title, "exercises": [exercise_view(e) for e in chapter.practice]}
    view, fallback = present(chapter, tree)
    return render_template("curriculum/practice.html", active_nav="learn", chapter=chapter, view=view, fallback=fallback, solved=solved_ids(current_user))


@bp.get("/<chapter_id>/summary")
@login_required
def summary(chapter_id):
    chapter, _section = load(chapter_id)
    view, fallback = present(chapter, {"title": chapter.title, "blocks": chapter.summary})
    return render_template("curriculum/summary.html", active_nav="learn", chapter=chapter, view=view, fallback=fallback)


@bp.post("/check")
@login_required
def check_answer():
    payload = request.get_json(silent=True)
    payload = payload if isinstance(payload, dict) else {}
    chapter, exercise = exercise_by_id(payload.get("exercise"))
    if exercise is None:
        return {"error": _("That exercise does not exist.")}, 404
    reveal = payload.get("reveal") is True
    given = payload.get("answer", "")
    given = given if isinstance(given, str) else ""
    verdict = None if reveal else check(exercise.answer, given[:MAX_LENGTH + 1])
    row = db.session.scalar(select(ExerciseResult).where(ExerciseResult.user_id == current_user.id, ExerciseResult.exercise_id == exercise.id))
    if row is None:
        row = ExerciseResult(user_id=current_user.id, exercise_id=exercise.id, attempts=0, solved=False)
        db.session.add(row)
    reply = {"status": "revealed" if reveal else verdict.status}
    if not reveal and verdict.status in ("correct", "wrong"):
        row.attempts += 1
        row.solved = row.solved or verdict.status == "correct"
        row.updated_at = utcnow()
    try:
        db.session.commit()
    except IntegrityError:
        # Two first answers to the same exercise arrived together, so the other request already created the row.
        db.session.rollback()
        row = db.session.scalar(select(ExerciseResult).where(ExerciseResult.user_id == current_user.id, ExerciseResult.exercise_id == exercise.id))
    if reveal or verdict.status == "correct":
        reply["solution"] = present(chapter, {"solution": exercise.solution})[0]["solution"]
    if not reveal:
        reply["message"] = question_text(exercise, verdict)
        note = note_for(exercise, given) if verdict.status == "wrong" else ""
        if note:
            reply["message"] = present(chapter, {"note": note})[0]["note"]
    reply["solved"] = row.solved
    return reply


@bp.get("/<chapter_id>/assessment")
@login_required
def assessment(chapter_id):
    chapter, _section = load(chapter_id)
    seed = request.args.get("seed", "")
    if not SEED.fullmatch(seed):
        return redirect(url_for("curriculum.assessment", chapter_id=chapter.id, seed=secrets.token_hex(4)))
    questions = chapter.assessment(random.Random(seed))
    view, fallback = present(chapter, {"title": chapter.title, "questions": [exercise_view(q) for q in questions]})
    return render_template("curriculum/assessment.html", active_nav="learn", chapter=chapter, view=view, fallback=fallback, seed=seed)


@bp.post("/<chapter_id>/assessment")
@login_required
def submit(chapter_id):
    chapter, _section = load(chapter_id)
    seed = request.form.get("seed", "")
    if not SEED.fullmatch(seed):
        abort(400)
    questions = chapter.assessment(random.Random(seed))
    answers = [request.form.get(f"q{i}", "").strip()[:200] for i in range(len(questions))]
    verdicts, by_concept = grade(questions, answers)
    attempt = ChapterAttempt(user_id=current_user.id, chapter_id=chapter.id, seed=seed, answers=answers, version=chapter.assessment_version,
                             correct=sum(v == "correct" for v in verdicts), total=len(questions), by_concept=by_concept)
    db.session.add(attempt)
    db.session.commit()
    if attempt.percent >= PASS_MARK:
        mascot.queue("completed")
    return redirect(url_for("curriculum.result", chapter_id=chapter.id, attempt_id=attempt.id))


@bp.get("/<chapter_id>/assessment/<int:attempt_id>")
@login_required
def result(chapter_id, attempt_id):
    chapter, _section = load(chapter_id)
    attempt = db.session.get(ChapterAttempt, attempt_id)
    if not attempt or attempt.user_id != current_user.id or attempt.chapter_id != chapter.id:
        abort(404)
    # Corrections are rebuilt from the seed, which only works while the question generator is the one that made the attempt.
    outdated = attempt.version != chapter.assessment_version
    questions = [] if outdated else chapter.assessment(random.Random(attempt.seed))
    verdicts = [] if outdated else grade(questions, attempt.answers)[0]
    by_concept = attempt.by_concept
    items, givens = [], []
    for exercise, given, status in zip(questions, attempt.answers, verdicts):
        picked = check(exercise.answer, given).value if exercise.answer.kind == "choice" and status in ("correct", "wrong") else None
        label_given = exercise.options[picked] if isinstance(picked, int) and picked < len(exercise.options) else ""
        # What the student typed stays out of the translated content, so it is never sent to the translator or stored.
        givens.append(given)
        items.append({**exercise_view(exercise), "given_label": label_given, "correct_text": answer_text(exercise, exercise.options),
                      "solution": exercise.solution, "wrong_note": note_for(exercise, given) if status == "wrong" else ""})
    concepts = {key: name for key, (name, _s) in chapter.concepts.items()}
    tree = {"title": chapter.title, "items": items, "concepts": concepts, "sections": {s.id: s.title for s in chapter.sections}}
    view, fallback = present(chapter, tree)
    progress = chapter_progress(current_user, chapter)
    revise = [r for r in progress["revise"] if r["concept"] in by_concept and by_concept[r["concept"]][1] and 100 * by_concept[r["concept"]][0] / by_concept[r["concept"]][1] < 60]
    return render_template("curriculum/result.html", active_nav="learn", chapter=chapter, view=view, fallback=fallback, attempt=attempt, verdicts=verdicts,
                           givens=givens, outdated=outdated, by_concept=by_concept, revise=revise, passmark=PASS_MARK, order=list(chapter.concepts))


@bp.post("/<chapter_id>/s/<section_id>/ask")
@login_required
def ask(chapter_id, section_id):
    chapter, section = load(chapter_id, section_id)
    payload = request.get_json(silent=True)
    payload = payload if isinstance(payload, dict) else request.form
    question = payload.get("question")
    question = question.strip() if isinstance(question, str) else ""
    if not question:
        return {"error": _("Type a question for the tutor first.")}, 400
    if len(question) > MAX_QUESTION_LENGTH:
        return {"error": _("Please keep your question under 1000 characters.")}, 400
    since = utcnow() - timedelta(hours=1)
    asked = db.session.scalar(select(func.count()).select_from(TutorQuestion).where(TutorQuestion.user_id == current_user.id, TutorQuestion.created_at >= since))
    if asked >= current_app.config["QUESTIONS_PER_HOUR"]:
        return {"error": _("You have asked a lot of questions this hour. Please try again a little later.")}, 429
    key = section_key(chapter.id, section.id)
    history = []
    for row in db.session.scalars(select(TutorQuestion).where(TutorQuestion.user_id == current_user.id, TutorQuestion.section_key == key).order_by(TutorQuestion.id.desc()).limit(4)):
        history = [("user", row.question), ("assistant", row.answer)] + history
    view, _fallback = present(chapter, section_view(section))
    try:
        reply = ai.ask_lesson_tutor(lesson_text(view), profile(current_user), history, question)
    except ai.AIError as exc:
        return {"error": str(exc)}, 503
    html = render_template("curriculum/_tutor_messages.html", rows=[("user", question), ("assistant", reply)])
    db.session.add(TutorQuestion(user_id=current_user.id, section_key=key, question=question, answer=reply))
    db.session.commit()
    return {"html": html}
