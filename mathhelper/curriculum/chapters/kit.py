"""Helpers shared by the chapter files: number formatting, exact reading of numbers, worked example blocks and exercise builders."""
import re
from fractions import Fraction

from ..checker import Answer, parse_number, show
from ..model import Exercise

D = r"$\mathbb{D}$"
NAT = r"$\mathbb{N}$"


def N(text):
    """Write numbers as math: a decimal comma that LaTeX does not space out, and a/b drawn as a stacked fraction."""
    text = re.sub(r"(\d+)/(\d+)", lambda m: "\\dfrac{" + m.group(1) + "}{" + m.group(2) + "}", text)
    return "$" + text.replace(",", "{,}") + "$"


def d(text):
    """Read a number or fraction written with a decimal comma as an exact fraction."""
    return parse_number(text)


def join_equal(line):
    """Merge '$a$ = $b$' into one formula '$a = b$', so a calculation reads as one connected line."""
    return re.sub(r"\$ (=|<|>) \$", r" \1 ", line)


def example(title, problem, method, steps, answer, verify, formula=""):
    """Build a worked example: a method, then each line of working with the reason for it."""
    return {"type": "example", "title": title, "problem": problem, "formula": formula, "method": method,
            "steps": [{"math": join_equal(math), "why": why} for math, why in steps], "answer": answer, "verify": verify}


def para(text):
    """A paragraph of explanation."""
    return {"type": "p", "text": text}


def definition(title, text):
    """A definition box."""
    return {"type": "definition", "title": title, "text": text}


def rule(title, text):
    """A property or rule box."""
    return {"type": "property", "title": title, "text": text}


def warning(text):
    """A box about a typical mistake."""
    return {"type": "warning", "text": text}


def column(sign, top, bottom, result=""):
    """Draw an addition or a subtraction in columns, with the commas under each other."""
    bar = " \\\\ \\hline " + result if result else " \\\\ \\hline"
    gap = "\\ " if sign == "+" else "\\ \\ "
    return ("$$\\begin{array}{r} " + top.replace(",", "{,}") + " \\\\ " + sign + gap + bottom.replace(",", "{,}") + bar.replace(",", "{,}") + " \\end{array}$$")


def rand_decimal(rng, low, high, places):
    """Return a random number with exactly this many decimals whose last decimal is not 0."""
    last = rng.randint(1, 9)
    middle = rng.randint(0, 10 ** (places - 1) - 1) if places > 1 else 0
    return Fraction(rng.randint(low, high) * 10**places + middle * 10 + last, 10**places)


def spaced(value, places):
    """Write a value with exactly this many decimals, padding with zeros."""
    return show(value) if places == 0 else f"{int(value)},{str(int((value - int(value)) * 10**places)).rjust(places, '0')}"


UNIT_SYNONYMS = {"F": ("FCFA", "francs", "franc"), "L": ("litres", "litre"), "m": ("mètres", "mètre"), "kg": ("kilogrammes",), "km": ("kilomètres",)}


def make_kit(chapter_id, default_form=""):
    """Return the exercise builders of one chapter, which prefix every exercise id with the chapter id. A default form can be required for every number answer."""

    def number(exercise_id, concept, prompt, value, level=1, hints=(), solution=(), units=(), form="", wrong=None):
        """Build an exercise whose answer is one number, given as an exact fraction."""
        units = tuple(units) + tuple(word for unit in units for word in UNIT_SYNONYMS.get(unit, ()))
        return Exercise(f"{chapter_id}/{exercise_id}", concept, prompt, Answer("number", value, units, form or default_form),
                        list(hints), list(solution), level=level, wrong=wrong or {})


    def choice(exercise_id, concept, prompt, options, right, level=1, hints=(), solution=(), wrong=None):
        """Build a multiple choice exercise, the right answer is the index of the option."""
        return Exercise(f"{chapter_id}/{exercise_id}", concept, prompt, Answer("choice", right), list(hints), list(solution),
                        options=list(options), level=level, wrong=wrong or {})


    def ordered(exercise_id, concept, prompt, values, level=1, hints=(), solution=()):
        """Build an exercise whose answer is a list of numbers in a given order."""
        return Exercise(f"{chapter_id}/{exercise_id}", concept, prompt, Answer("numbers", tuple(values)), list(hints), list(solution), level=level)


    def between(exercise_id, concept, prompt, low, high, level=1, hints=(), solution=()):
        """Build an exercise where any number strictly between two values is a correct answer."""
        return Exercise(f"{chapter_id}/{exercise_id}", concept, prompt, Answer("between", low, high=high, form="decimal"), list(hints), list(solution), level=level)

    return number, choice, ordered, between
