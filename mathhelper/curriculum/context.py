"""What the AI is told about a student's curriculum, level and progress, and about the lesson being read."""
from sqlalchemy import select

from ..extensions import db
from ..models import LessonCompletion
from .catalog import CHAPTERS, country, level

GENERAL_GUIDANCE = [
    (7, "Prefer arithmetic reasoning, number lines, tables and drawings. Use letters only to state a general property, and no calculus."),
    (9, "Elementary algebra may be used when the problem needs it, with every step explained. Do not use calculus."),
    (13, "Functions and trigonometry may be used. Use calculus only if the student's own question needs it, and explain the technique first."),
]


def section_key(chapter_id, section_id):
    """Return the key under which a finished section is stored."""
    return f"cur:{chapter_id}:{section_id}"


def done_keys(user):
    """Return every lesson or section key the user finished."""
    return set(db.session.scalars(select(LessonCompletion.lesson_key).where(LessonCompletion.user_id == user.id)))


def finished_sections(user):
    """Return the (chapter, section) pairs the user has marked as done, in chapter order."""
    done = done_keys(user)
    return [(c, s) for c in CHAPTERS for s in c.sections if section_key(c.id, s.id) in done]


def profile(user):
    """Describe the student's curriculum and level for the AI, or return nothing when they have not chosen one."""
    if not user.is_authenticated or not user.country or not user.grade:
        return ""
    place, stage = country(user.country), level(user.country, user.grade)
    if place is None or stage is None:
        return ""
    guidance = next((text for limit, text in GENERAL_GUIDANCE if stage.grade < limit), "")
    studied = [f"{c.title}: {s.title}" for c, s in finished_sections(user)]
    lines = [
        "",
        "About this student:",
        f"- They follow the {place.en} curriculum, at the level {stage.en} (roughly the equivalent of Grade {stage.grade}).",
        f"- {guidance} These are general expectations for the year, not the official syllabus, so never claim what the official programme requires.",
        "- Solve with the methods a student at this level has been taught, and explain every transformation instead of jumping to the answer.",
        "- If the problem needs knowledge beyond this level, say so kindly and explain the needed idea in simple words. Never give up mathematical correctness to make a solution look easier.",
    ]
    if studied:
        lines.append("- Lessons finished in this app: " + "; ".join(studied[:12]) + ".")
    return "\n".join(lines) + "\n"


def lesson_text(view):
    """Flatten a lesson section into plain text for the tutor to read."""
    out = [f"Section: {view['title']}", f"Goal: {view['goal']}"]
    for block in view["blocks"]:
        kind = block["type"]
        if kind == "example":
            out.append(f"Worked example. {block['problem']} Method: {block['method']}")
            out += [f"  {step['math']}   ({step['why']})" for step in block["steps"]]
            out.append(f"  Answer: {block['answer']}")
        elif kind == "figure":
            out.append(f"Figure: {block['alt']} ({block['caption']})")
        elif kind == "table":
            out.append("Table: " + " | ".join(block["head"]) + " / " + " | ".join(block["rows"][0]))
        else:
            title = block.get("title")
            out.append((f"{title}: " if title else "") + block["text"])
    return "\n".join(out)
