"""Gemini service that solves math problems and answers follow up questions."""
import json
import logging
import re

import httpx
from flask import current_app
from google import genai
from google.genai import errors, types
from pydantic import BaseModel

from .grades import ai_guidance
from .i18n import gettext as _
from .i18n import language

log = logging.getLogger(__name__)

TOPICS = [
    "Arithmetic", "Fractions", "Decimals", "Percentages", "Ratios", "Algebra", "Equations",
    "Inequalities", "Functions", "Exponents", "Geometry", "Trigonometry", "Statistics",
    "Probability", "Calculus", "Linear Algebra", "Word Problem", "Other",
]
RETRYABLE = {408, 429, 500, 502, 503, 504}


class AIError(Exception):
    """An error whose message is safe to show to the student."""


class Step(BaseModel):
    title: str
    result: str = ""
    work: str


class Problem(BaseModel):
    problem: str
    topic: str
    start: str = ""
    answer: str
    steps: list[Step]
    tip: str = ""


class SolveResult(BaseModel):
    problems: list[Problem]
    note: str = ""


SOLVE_INSTRUCTIONS = r"""You are a patient, encouraging math tutor. {audience}

Find every math problem in the message, solve each one correctly, and show exactly how you got there.

Rules:
- Check your arithmetic twice before you answer.
- Show the full working as a chain of math lines, the way a teacher writes it on the board. "start" is the problem written as one line of math, such as $3x - 2 = -x + 6$. For a word problem, "start" is the equation or expression you set up from it.
- Then split the work into small steps. Each step changes the line before it in one simple way. "result" is the new line of math after that step, such as $3x + x = 6 + 2$, written only in math with no words. "title" names the move in a few words. "work" explains in one or two plain sentences what was done and why.
- Read from top to bottom, "start" followed by every "result" must be the complete working, ending with the line that gives the answer, such as $x = 2$.
- Explain in plain, friendly words. Skip filler.
- Write all math in LaTeX between single dollar signs, like $\frac{3}{4}$ or $x^2 + 1$. Use $$...$$ only for a long equation on its own line.
- In the JSON output escape every backslash, so \frac is written as \\frac.
- Write money in words, like 5 dollars, so dollar signs only ever wrap math.
- "problem" restates the problem clearly. "answer" is only the final answer, kept short. "tip" is one sentence worth remembering next time.
- "topic" is one of: {topics}.
- If there is no math problem, return an empty "problems" list and use "note" to explain kindly what went wrong, such as a blurry photo or a question that is not about math.
"""

TUTOR_INSTRUCTIONS = r"""You are a friendly math tutor chatting about work you already solved together. {audience}

The solved work:
{context}

Reply to the student's latest message. Keep it under 150 words unless they ask for more detail. Use Markdown for structure and LaTeX between single dollar signs for math. If they ask for a similar problem, give one without the answer and offer to check their work. If they share their own attempt, check it and point to the exact step that went wrong. When you show working, put each line of math on its own line so every calculation is easy to follow. Stay focused on math and learning.
"""

LANGUAGE_RULES = {
    "fr": "\nWrite every title, explanation, answer, tip and note in French, using the informal \"tu\". Use a decimal comma, written as 3{,}5 inside math. Keep the \"topic\" value exactly as listed above, in English.\n",
}
TUTOR_LANGUAGE_RULES = {"fr": "\nReply in French, using the informal \"tu\".\n"}
ANYONE = "Learners of every age and teachers use this app, so explain clearly enough for anyone to follow."
IN_CLASS = "Explain at the level of the student's class, described below."

_ESCAPE = re.compile(r"\\(u[0-9a-fA-F]{4}|.)", re.S)
_LATEX_AFTER_N = re.compile(r"(?:eq|abla|eg|ot|otin|mid|leq|geq|ewline|subseteq|parallel)(?![a-zA-Z])")
_clients = {}


def repair_json(raw):
    """Double lone backslashes that belong to LaTeX so the JSON parses as the model meant."""

    def fix(match):
        seq = match.group(1)
        if len(seq) == 5 or seq in '"\\/':
            return match.group(0)
        after = raw[match.end():match.end() + 12]
        if seq in "bfrt" and not after[:1].isalpha():
            return match.group(0)
        if seq == "n" and not _LATEX_AFTER_N.match(after):
            return match.group(0)
        return "\\\\" + seq

    return _ESCAPE.sub(fix, raw)


def _client():
    """Return a cached Gemini client for the configured key."""
    key = current_app.config["GEMINI_API_KEY"]
    if not key:
        raise AIError(_("The AI tutor is not set up yet. Add GEMINI_API_KEY to the .env file."))
    if key not in _clients:
        options = types.HttpOptions(timeout=30_000, retry_options=types.HttpRetryOptions(attempts=1))
        _clients[key] = genai.Client(api_key=key, http_options=options)
    return _clients[key]


def _models():
    """Return the main model followed by the backup model."""
    names = [current_app.config["GEMINI_MODEL"], current_app.config["GEMINI_FALLBACK_MODEL"]]
    return [name for i, name in enumerate(names) if name and name not in names[:i]]


def _friendly(exc):
    """Turn a low level failure into a message a student can act on."""
    if isinstance(exc, errors.APIError):
        message = (exc.message or "").lower()
        if exc.code == 429:
            return _("The AI has hit its usage limit for now. Please try again in a minute.")
        if exc.code in (400, 401, 403) and "key" in message:
            return _("The AI service rejected the API key. Check GEMINI_API_KEY in the .env file.")
        if exc.code == 404:
            return _("The AI model is not available. Check GEMINI_MODEL in the .env file.")
        if exc.code >= 500:
            return _("The AI service is very busy right now. Please try again in a moment.")
    if isinstance(exc, httpx.HTTPError):
        return _("Could not reach the AI service. Check your internet connection and try again.")
    return _("The AI could not work this one out. Try a clearer photo or type the problem instead.")


def _run(contents, config, parse):
    """Call Gemini, moving on to the backup model when the first one fails."""
    last_error = None
    for model in _models():
        try:
            response = _client().models.generate_content(model=model, contents=contents, config=config)
            return parse(response)
        except errors.APIError as exc:
            log.warning("Gemini model %s failed with %s: %s", model, exc.code, exc.message)
            last_error = exc
            if exc.code not in RETRYABLE:
                break
        except (httpx.HTTPError, ValueError) as exc:
            log.warning("Gemini model %s gave an unusable reply: %s", model, exc)
            last_error = exc
    raise AIError(_friendly(last_error))


def _normalize_topic(topic):
    """Map the topic onto the known list so filters stay tidy."""
    for known in TOPICS:
        if known.lower() == topic.strip().lower():
            return known
    return topic.strip().title()[:40] or "Other"


def math_line(line):
    """Make sure a line of working is marked as math, since models sometimes leave out the dollar signs."""
    line = line.strip()
    return f"${line}$" if line and "$" not in line else line


def _parse_solution(response):
    """Read the structured solution out of a Gemini reply."""
    text = (response.text or "").strip()
    if not text:
        raise ValueError("empty reply")
    result = SolveResult.model_validate(json.loads(repair_json(text)))
    for problem in result.problems:
        problem.topic = _normalize_topic(problem.topic)
        problem.start = math_line(problem.start)
        for step in problem.steps:
            step.result = math_line(step.result)
    return result


def _audience(template, grade, beyond):
    """Fill in who the tutor is talking to and add the methods of the student's class."""
    guidance = ai_guidance(grade, beyond)
    return template.replace("{audience}", IN_CLASS if guidance else ANYONE) + guidance


def _solve(contents, grade=None):
    """Ask Gemini for a structured solution to the given contents, at the student's class."""
    instructions = _audience(SOLVE_INSTRUCTIONS, grade, 'say so kindly in "note".')
    instructions = instructions.replace("{topics}", ", ".join(TOPICS))
    instructions += LANGUAGE_RULES.get(language(), "")
    config = types.GenerateContentConfig(
        system_instruction=instructions,
        response_mime_type="application/json",
        response_schema=SolveResult,
        temperature=0.2,
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
    )
    return _run(contents, config, _parse_solution)


def solve_image(image_bytes, grade=None):
    """Solve every problem found in a JPEG photo."""
    photo = types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")
    return _solve([photo, "Solve every math problem in this photo."], grade)


def solve_text(problem, grade=None):
    """Solve a problem the student typed."""
    return _solve([f"Solve this:\n{problem}"], grade)


def _describe(problems):
    """Write the solved problems as plain text for the tutor prompt."""
    lines = []
    for number, problem in enumerate(problems, 1):
        lines.append(f"Problem {number}: {problem['problem']}")
        if problem.get("start"):
            lines.append(f"  Start: {problem['start']}")
        for index, step in enumerate(problem["steps"], 1):
            result = f" {step['result']}" if step.get("result") else ""
            lines.append(f"  Step {index}. {step['title']}:{result} {step['work']}")
        lines.append(f"  Answer: {problem['answer']}")
    return "\n".join(lines) or "No problem was found."


def _parse_text(response):
    """Read plain text out of a Gemini reply."""
    text = (response.text or "").strip()
    if not text:
        raise ValueError("empty reply")
    return text


def ask_tutor(problems, history, question, grade=None):
    """Answer a follow up question about an existing solution, at the student's class."""
    instructions = _audience(TUTOR_INSTRUCTIONS, grade, "say that this idea comes in a later class.")
    instructions = instructions.replace("{context}", _describe(problems))
    instructions += TUTOR_LANGUAGE_RULES.get(language(), "")
    turns = [(role, text) for role, text in history[-12:]] + [("user", question)]
    contents = [
        types.Content(role="user" if role == "user" else "model", parts=[types.Part.from_text(text=text)])
        for role, text in turns
    ]
    config = types.GenerateContentConfig(
        system_instruction=instructions,
        temperature=0.4,
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
    )
    return _run(contents, config, _parse_text)
