"""Building blocks shared by every practice skill."""
import random
from dataclasses import dataclass
from fractions import Fraction
from typing import Callable

from ..i18n import language
from ..i18n import pick as L  # noqa: F401  shared by every skill module

LEVEL_ORDER = ["Elementary", "Middle School", "High School", "College"]
QUESTIONS_PER_ROUND = 10


@dataclass
class Question:
    prompt: str
    choices: list[str]
    answer: int
    explanation: str


@dataclass(frozen=True)
class Skill:
    id: str
    title: str
    level: str
    topic: str
    blurb: str
    make: Callable[[random.Random], Question] | None
    questions: tuple = ()


SKILLS: dict[str, Skill] = {}


def skill(skill_id, title, level, topic, blurb):
    """Register a question generator as a practice skill."""

    def register(make):
        SKILLS[skill_id] = Skill(skill_id, title, level, topic, blurb, make)
        return make

    return register


def written_round(questions, rng, count):
    """Shuffle questions the admin wrote, and their choices, the same way every time for a seed."""
    picked = list(questions)
    rng.shuffle(picked)
    result = []
    for question in picked[:count]:
        order = list(range(len(question.choices)))
        rng.shuffle(order)
        result.append(Question(question.prompt, [question.choices[i] for i in order], order.index(question.answer), question.explanation))
    return result


def build_round(skill_id, seed, count=QUESTIONS_PER_ROUND, skill=None):
    """Create the same list of questions every time for a given skill and seed."""
    skill = skill or SKILLS[skill_id]
    rng = random.Random(f"{skill_id}:{seed}")
    if skill.questions:
        return written_round(skill.questions, rng, count)
    make = skill.make
    questions, seen = [], set()
    for _ in range(count * 25):
        question = make(rng)
        if question.prompt not in seen:
            seen.add(question.prompt)
            questions.append(question)
        if len(questions) == count:
            break
    while len(questions) < count:
        questions.append(make(rng))
    return questions


def pick(rng, correct, wrong, fmt=str):
    """Shuffle the right answer with three distinct likely mistakes."""
    options = [fmt(correct)]
    for candidate in wrong:
        text = fmt(candidate)
        if text not in options:
            options.append(text)
        if len(options) == 4:
            break
    step = 1
    while len(options) < 4:
        for candidate in (correct + step, correct - step):
            text = fmt(candidate)
            if text not in options and len(options) < 4:
                options.append(text)
        step += 1
    order = list(range(4))
    rng.shuffle(order)
    return [options[i] for i in order], order.index(0)


def m(expr):
    """Wrap an expression in inline math delimiters."""
    return f"${expr}$"


def frac(value):
    """Write a whole number or fraction in LaTeX."""
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    sign = "-" if value < 0 else ""
    return f"{sign}\\frac{{{abs(value.numerator)}}}{{{value.denominator}}}"


def mf(value):
    """Wrap a fraction in inline math."""
    return m(frac(value))


def paren(n):
    """Put negative numbers in brackets so expressions stay readable."""
    return f"({n})" if n < 0 else str(n)


def linear(terms):
    """Write a sum like [(3, 'x'), (-2, 'y'), (5, '')] as 3x - 2y + 5."""
    parts = []
    for coef, var in terms:
        coef = Fraction(coef)
        if coef == 0:
            continue
        size = abs(coef)
        body = frac(size) if not var or size != 1 else ""
        parts.append(("-" if coef < 0 else "+", body + var))
    if not parts:
        return "0"
    text = ("-" if parts[0][0] == "-" else "") + parts[0][1]
    for sign, body in parts[1:]:
        text += f" {sign} {body}"
    return text


def power(var, exp):
    """Write a variable raised to a power, keeping x^1 as just x."""
    if exp == 0:
        return ""
    return var if exp == 1 else f"{var}^{{{exp}}}"


def poly(coeffs, var="x"):
    """Write a polynomial from a {power: coefficient} map in LaTeX."""
    return linear([(coeffs[p], power(var, p)) for p in sorted(coeffs, reverse=True)])


def local_number(text):
    """Write decimal numbers with a comma when the language is French."""
    return text.replace(".", "{,}") if language() == "fr" else text
