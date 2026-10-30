"""The admin dashboard: users, practice and translations, open to the admin account only."""
import re
import secrets
from datetime import timedelta

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import delete, func, or_, select

from .. import mascot
from ..accounts import delete_user
from ..ai import TOPICS
from ..extensions import db
from ..i18n import gettext as _
from ..i18n import language
from ..curriculum.catalog import CHAPTERS
from ..curriculum.translate import correct_translation, shown_translation
from ..models import LessonCompletion, PracticeAttempt, SavedPractice, Solution, TranslationCache, User, utcnow
from ..practice import SKILLS, build_round
from ..practice.catalog import all_skills, forget_practice, stored_practice
from ..translations.fr import FR
from .helpers import safe_next

bp = Blueprint("admin", __name__, url_prefix="/admin")
PER_PAGE = 20
STUDENT_PAGES = {"solve", "library", "practice", "curriculum"}
STUDENT_ENDPOINTS = {"main.home", "main.upload"}
MIN_QUESTIONS, MAX_QUESTIONS, CHOICES = 3, 30, 4
QUESTION_FIELD = re.compile(r"q-(\d{1,3})-")


@bp.before_app_request
def keep_admin_in_dashboard():
    """Send the admin to the dashboard instead of the student pages, which are not part of the admin account."""
    if not current_user.is_authenticated or not current_user.is_admin:
        return None
    if request.blueprint in STUDENT_PAGES or request.endpoint in STUDENT_ENDPOINTS:
        return redirect(url_for("admin.index"))
    return None


@bp.before_request
@login_required
def admins_only():
    """Stop anyone who is not the admin before any admin page or action runs."""
    if not current_user.is_admin:
        abort(403)


@bp.get("/")
def index():
    students = select(func.count()).select_from(User).where(User.is_admin.is_(False))
    week = utcnow() - timedelta(days=7)

    def this_week(model):
        return db.session.scalar(select(func.count()).select_from(model).where(model.created_at >= week))

    numbers = {
        "users": db.session.scalar(students),
        "new": db.session.scalar(students.where(User.created_at >= week)),
        "suspended": db.session.scalar(students.where(User.suspended_at.is_not(None))),
        "lessons": len(CHAPTERS),
        "practice": len(all_skills()),
        "solved": this_week(Solution),
        "rounds": this_week(PracticeAttempt),
        "finished": this_week(LessonCompletion),
    }
    newest = db.session.scalars(select(User).where(User.is_admin.is_(False)).order_by(User.created_at.desc()).limit(5)).all()
    return render_template("admin/index.html", tab="overview", numbers=numbers, newest=newest)


@bp.get("/beral")
def beral():
    return render_template("admin/beral.html", tab="overview", three=mascot.three_d(), model_file=mascot.MODEL_FILE)


# Users.

def activity(ids):
    """Count solutions, practice rounds and finished lessons for a list of users."""
    counts = {}
    for name, model in (("solutions", Solution), ("rounds", PracticeAttempt), ("lessons", LessonCompletion)):
        rows = db.session.execute(select(model.user_id, func.count()).where(model.user_id.in_(ids)).group_by(model.user_id))
        counts[name] = {user_id: total for user_id, total in rows}
    return counts


def student(user_id):
    """Load a user the admin may act on, which never includes the admin account."""
    user = db.session.get(User, user_id)
    if user is None:
        abort(404)
    if user.is_admin:
        abort(403)
    return user


def back_to_users():
    """Return to the user list, keeping the search and page the admin was on."""
    return redirect(safe_next(request.form.get("next"), url_for("admin.users")))


@bp.get("/users")
def users():
    query = request.args.get("q", "").strip()[:100]
    status = request.args.get("status", "all")
    stmt = select(User).where(User.is_admin.is_(False))
    if query:
        needle = query.lower()
        stmt = stmt.where(or_(func.lower(User.name).contains(needle, autoescape=True),
                              func.lower(User.email).contains(needle, autoescape=True)))
    if status == "suspended":
        stmt = stmt.where(User.suspended_at.is_not(None))
    elif status == "active":
        stmt = stmt.where(User.suspended_at.is_(None))
    else:
        status = "all"
    page = db.paginate(stmt.order_by(User.created_at.desc(), User.id.desc()), page=request.args.get("page", 1, type=int),
                       per_page=PER_PAGE, error_out=False)
    return render_template("admin/users.html", tab="users", page=page, query=query, status=status,
                           activity=activity([user.id for user in page.items]))


@bp.post("/users/<int:user_id>/suspend")
def suspend(user_id):
    user = student(user_id)
    user.suspended_at = user.suspended_at or utcnow()
    db.session.commit()
    flash(_("{name} is suspended and can no longer sign in.", name=user.name), "info")
    return back_to_users()


@bp.post("/users/<int:user_id>/reactivate")
def reactivate(user_id):
    user = student(user_id)
    user.suspended_at = None
    db.session.commit()
    flash(_("{name} can sign in again.", name=user.name), "success")
    return back_to_users()


@bp.post("/users/<int:user_id>/delete")
def remove_user(user_id):
    user = student(user_id)
    name = user.name
    delete_user(user)
    db.session.commit()
    flash(_("{name} and all of their data were deleted.", name=name), "info")
    return back_to_users()


# Practice.

def slugify(title, taken, prefix=""):
    """Turn a title into a short web address that is not already taken."""
    base = prefix + (re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:50] or "item")
    slug, number = base, 2
    while slug in taken:
        slug, number = f"{base}-{number}", number + 1
    return slug


def practice_row(skill_id):
    """Return the admin's row for a practice set, or None."""
    return db.session.scalar(select(SavedPractice).where(SavedPractice.skill_id == skill_id))


def blank_question():
    """Return an empty question block for the form."""
    return {"prompt": "", "choices": [""] * CHOICES, "answer": 0, "explanation": "",
            "fr": {"prompt": "", "choices": [""] * CHOICES, "explanation": ""}}


def question_blocks(stored):
    """Turn stored questions into form blocks with four choice slots each."""
    blocks = []
    for item in stored:
        english, french = item["en"], item.get("fr", {})
        pad = lambda choices: (list(choices) + [""] * CHOICES)[:CHOICES]
        blocks.append({"prompt": english["prompt"], "choices": pad(english["choices"]), "answer": item["answer"],
                       "explanation": english.get("explanation", ""),
                       "fr": {"prompt": french.get("prompt", ""), "choices": pad(french.get("choices") or []),
                              "explanation": french.get("explanation", "")}})
    return blocks


def read_questions():
    """Read the question blocks, returning what was typed, the clean questions and an error message, if any."""
    def field(index, name, limit=500):
        return request.form.get(f"q-{index}-{name}", "").strip()[:limit]

    indexes = sorted({int(match.group(1)) for key in request.form if (match := QUESTION_FIELD.match(key))})
    blocks, questions, error = [], [], None
    for index in indexes:
        block = {"prompt": field(index, "prompt", 1000), "choices": [field(index, f"choice-{j}") for j in range(CHOICES)],
                 "answer": request.form.get(f"q-{index}-answer", -1, type=int), "explanation": field(index, "explanation", 1000),
                 "fr": {"prompt": field(index, "fr-prompt", 1000), "choices": [field(index, f"fr-choice-{j}") for j in range(CHOICES)],
                        "explanation": field(index, "fr-explanation", 1000)}}
        if not block["prompt"] and not any(block["choices"]) and not block["explanation"]:
            continue
        blocks.append(block)
        filled = [j for j, choice in enumerate(block["choices"]) if choice]
        if not block["prompt"] or len(filled) < 2 or block["answer"] not in filled:
            error = error or _("Question {n} needs its text, at least two choices and the right answer marked.", n=len(blocks))
            continue
        french_choices = [block["fr"]["choices"][j] for j in filled]
        questions.append({
            "answer": filled.index(block["answer"]),
            "en": {"prompt": block["prompt"], "choices": [block["choices"][j] for j in filled], "explanation": block["explanation"]},
            "fr": {"prompt": block["fr"]["prompt"], "choices": french_choices if all(french_choices) else [],
                   "explanation": block["fr"]["explanation"]},
        })
    if not error and len(questions) < MIN_QUESTIONS:
        error = _("Write at least {n} questions.", n=MIN_QUESTIONS)
    elif not error and len(questions) > MAX_QUESTIONS:
        error = _("A practice set can have up to {n} questions.", n=MAX_QUESTIONS)
    return blocks, questions, error


def read_practice_form(written):
    """Read the practice form and return its values, the typed question blocks and an error message, if any."""
    def text(name, limit):
        return request.form.get(name, "").strip()[:limit]

    content = {"en": {"title": text("title", 80), "blurb": text("blurb", 200)},
               "fr": {"title": text("fr_title", 80), "blurb": text("fr_blurb", 200)}}
    topic = request.form.get("topic", "")
    values = {"content": content, "topic": topic, "published": request.form.get("published") == "on"}
    blocks, questions, error = read_questions() if written else ([], [], None)
    values["questions"] = questions
    if not content["en"]["title"] or not content["en"]["blurb"]:
        error = _("Give the practice set an English title and description.")
    elif topic not in TOPICS:
        error = _("Choose a topic.")
    return values, blocks, error


def practice_form(values, blocks, error, editing, written):
    """Show the practice form."""
    return render_template("admin/practice_form.html", tab="practice", form=values, blocks=blocks, error=error, editing=editing,
                           written=written, topics=TOPICS, choices=CHOICES, blank=blank_question())


@bp.get("/practice")
def practice():
    rows = {row.skill_id: row for row in stored_practice()}
    shown = all_skills(hidden=True)
    items = []
    for skill_id, skill in shown.items():
        row = rows.get(skill_id)
        if skill_id in SKILLS:
            state = "builtin" if row is None else "deleted" if row.deleted else "edited" if row.content else "builtin"
        else:
            state = "custom"
        items.append({"skill": skill, "state": state, "draft": bool(row) and not row.published and not row.deleted,
                      "count": len(skill.questions)})
    return render_template("admin/practice.html", tab="practice", items=items)


@bp.get("/practice/<skill_id>/preview")
def preview_practice(skill_id):
    skill = all_skills(hidden=True).get(skill_id) or abort(404)
    questions = build_round(skill.id, secrets.token_hex(8), skill=skill)
    return render_template("admin/practice_preview.html", tab="practice", skill=skill, questions=questions)


@bp.route("/practice/new", methods=["GET", "POST"])
def new_practice():
    values = {"content": {"en": {"title": "", "blurb": ""}, "fr": {"title": "", "blurb": ""}}, "topic": "", "published": True}
    blocks, error = [blank_question() for _n in range(MIN_QUESTIONS)], None
    if request.method == "POST":
        values, blocks, error = read_practice_form(written=True)
        if not error:
            taken = set(SKILLS) | {row.skill_id for row in stored_practice()}
            db.session.add(SavedPractice(skill_id=slugify(values["content"]["en"]["title"], taken, prefix="set-"), level="", **values))
            db.session.commit()
            forget_practice()
            flash(_("Practice set published.") if values["published"] else _("Practice set saved as a draft."), "success")
            return redirect(url_for("admin.practice"))
    return practice_form(values, blocks or [blank_question()], error, None, True)


@bp.route("/practice/<skill_id>/edit", methods=["GET", "POST"])
def edit_practice(skill_id):
    row, original = practice_row(skill_id), SKILLS.get(skill_id)
    if row is None and original is None:
        abort(404)
    written = original is None
    error = None
    if request.method == "POST":
        values, blocks, error = read_practice_form(written)
        if not error:
            if row is None:
                row = SavedPractice(skill_id=skill_id)
                db.session.add(row)
            row.content, row.topic, row.level = values["content"], values["topic"], original.level if original else ""
            row.published, row.deleted = values["published"], False
            if written:
                row.questions = values["questions"]
            db.session.commit()
            forget_practice()
            flash(_("Practice set updated."), "success")
            return redirect(url_for("admin.practice"))
    elif row is not None and row.content:
        values = {"content": row.content, "topic": row.topic, "published": row.published}
        blocks = question_blocks(row.questions or [])
    else:
        values = {"content": {"en": {"title": original.title, "blurb": original.blurb},
                              "fr": {"title": FR.get(original.title, ""), "blurb": FR.get(original.blurb, "")}},
                  "topic": original.topic, "published": True}
        blocks = []
    return practice_form(values, blocks, error, skill_id, written)


@bp.post("/practice/<skill_id>/delete")
def delete_practice(skill_id):
    row, original = practice_row(skill_id), SKILLS.get(skill_id)
    if row is None and original is None:
        abort(404)
    if original is not None:
        # A built in practice set stays hidden through a marker row, so it can be restored later.
        if row is None:
            row = SavedPractice(skill_id=skill_id, level=original.level, topic=original.topic, content={})
            db.session.add(row)
        row.deleted = True
    else:
        db.session.delete(row)
        db.session.execute(delete(PracticeAttempt).where(PracticeAttempt.skill_id == skill_id))
    db.session.commit()
    forget_practice()
    flash(_("Practice set deleted."), "info")
    return redirect(url_for("admin.practice"))


@bp.post("/practice/<skill_id>/restore")
def restore_practice(skill_id):
    row = practice_row(skill_id)
    if row is None or skill_id not in SKILLS:
        abort(404)
    db.session.delete(row)
    db.session.commit()
    forget_practice()
    flash(_("The original practice set is back."), "success")
    return redirect(url_for("admin.practice"))


# ----- Translations of curriculum lessons: review, correct and clear -----

def translation_row(row_id):
    """Load a stored translation or stop with 404."""
    row = db.session.get(TranslationCache, row_id)
    if row is None:
        abort(404)
    return row


@bp.get("/translations")
def translations():
    query = request.args.get("q", "").strip()[:100]
    status = request.args.get("status", "unreviewed")
    stmt = select(TranslationCache)
    if query:
        needle = query.lower()
        stmt = stmt.where(or_(func.lower(TranslationCache.source).contains(needle, autoescape=True),
                              func.lower(TranslationCache.text).contains(needle, autoescape=True)))
    if status == "reviewed":
        stmt = stmt.where(TranslationCache.reviewed.is_(True))
    elif status == "all":
        pass
    else:
        status = "unreviewed"
        stmt = stmt.where(TranslationCache.reviewed.is_(False))
    page = db.paginate(stmt.order_by(TranslationCache.id.desc()), page=request.args.get("page", 1, type=int), per_page=PER_PAGE, error_out=False)
    shown = {row.id: shown_translation(row) for row in page.items}
    return render_template("admin/translations.html", tab="translations", page=page, query=query, status=status, shown=shown)


@bp.post("/translations/<int:row_id>/save")
def save_translation(row_id):
    row = translation_row(row_id)
    text = request.form.get("text", "").strip()
    if not text or len(text) > 4000:
        flash(_("Write the corrected translation first."), "error")
    elif not correct_translation(row, text):
        flash(_("A correction must keep every formula exactly as it is. Only the words can change."), "error")
    else:
        db.session.commit()
        flash(_("Translation saved and marked as checked."), "success")
    return redirect(safe_next(request.form.get("next"), url_for("admin.translations")))


@bp.post("/translations/<int:row_id>/review")
def review_translation(row_id):
    translation_row(row_id).reviewed = True
    db.session.commit()
    flash(_("Translation marked as checked."), "success")
    return redirect(safe_next(request.form.get("next"), url_for("admin.translations")))


@bp.post("/translations/<int:row_id>/delete")
def delete_translation(row_id):
    db.session.delete(translation_row(row_id))
    db.session.commit()
    flash(_("Translation deleted. It will be translated again the next time a student needs it."), "info")
    return redirect(safe_next(request.form.get("next"), url_for("admin.translations")))
