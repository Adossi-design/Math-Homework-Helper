"""Exact answer checking for curriculum exercises, so a correct answer is never marked wrong for how it is written."""
import math
import re
from dataclasses import dataclass
from fractions import Fraction

MAX_LENGTH = 200
MAX_DIGITS = 60
_FRAC = re.compile(r"\\d?frac\s*\{([^{}]{0,60})\}\s*\{([^{}]{0,60})\}")
_GROUPED = re.compile(r"^\d{1,3}( \d{3})+(,\d+)?$", re.ASCII)
_DECIMAL = re.compile(r"^(\d+([.,]\d+)?|[.,]\d+)$", re.ASCII)
_INDEX = re.compile(r"^[0-9]{1,3}$")
_SIGN = re.compile(r"^[+-]")
_SEPARATORS = re.compile(r"[;<>]|\s+(?:puis|then|et|and)\s+")


@dataclass(frozen=True)
class Answer:
    """What a correct answer looks like. kind is number, numbers, choice or between."""

    kind: str
    value: object = None
    units: tuple = ()
    form: str = ""  # "fraction", "decimal_fraction", "decimal" or "irreducible" when the exercise asks for that way of writing the number
    high: object = None


@dataclass(frozen=True)
class Verdict:
    """The outcome of checking one answer."""

    status: str  # correct, wrong, unreadable or wrong_form
    value: object = None


def clean(text):
    """Normalise spaces, minus signs and LaTeX so the text can be read as a number."""
    text = (text or "").replace("\u00a0", " ").replace("\u202f", " ").replace("\u2212", "-")
    text = text.replace("$", "").replace("\\,", "").replace("\\ ", " ").replace("{,}", ",")
    for _round in range(3):
        text = _FRAC.sub(lambda m: f"({m.group(1)})/({m.group(2)})", text)
    return text.strip()


def strip_units(text, units):
    """Remove a unit written after the number, such as 'm' or 'F', but only a unit the exercise allows."""
    for unit in sorted(units, key=len, reverse=True):
        if text.lower().endswith(unit.lower()) and text[: len(text) - len(unit)].strip():
            return text[: len(text) - len(unit)].strip()
    return text


def parse_plain(text):
    """Read a decimal such as 3,5 or 3.5 or 1 500,25 or 1.353.287 as an exact fraction, or return None."""
    text = text.strip()
    if text.startswith("(") and text.endswith(")"):
        text = text[1:-1].strip()
    if _GROUPED.match(text):
        text = text.replace(" ", "")
    if text.count(".") > 1 and "," not in text:
        # Several points only mean thousands (1.353.287); anything else such as 1.5. or 2.5.0 is a typing slip.
        if not re.fullmatch(r"-?\d{1,3}(\.\d{3})+", text):
            return None
        text = text.replace(".", "")
    elif text.count(".") >= 1 and text.count(",") == 1 and text.rfind(",") > text.rfind("."):
        text = text.replace(".", "")
    sign = -1 if text.startswith("-") else 1
    body = _SIGN.sub("", text).strip()
    if len(body) > MAX_DIGITS or not _DECIMAL.match(body):
        return None
    whole, _, decimals = body.replace(",", ".").partition(".")
    return sign * Fraction(int(whole + decimals), 10 ** len(decimals))


def parse_number(text, units=()):
    """Read a number, decimal or fraction typed by a student, or return None when it cannot be understood."""
    text = strip_units(clean(text), units)
    if "/" in text:
        parts = [p.strip().strip("()").strip() for p in text.split("/")]
        if len(parts) != 2:
            return None
        top, bottom = parse_plain(parts[0]), parse_plain(parts[1])
        return top / bottom if top is not None and bottom else None
    return parse_plain(text)


def parse_list(text, units=()):
    """Read several numbers separated by semicolons or by the signs < and >, or return None."""
    text = clean(text)
    pieces = [p for p in _SEPARATORS.split(text) if p.strip()]
    if len(pieces) == 1 and " " in pieces[0].strip() and not _GROUPED.match(pieces[0].strip()):
        pieces = pieces[0].split()
    values = [parse_number(piece, units) for piece in pieces]
    return None if not values or None in values else values


def decimal_fraction(text):
    """Return True when the text is a fraction whose denominator is 10, 100, 1000 and so on."""
    parts = text.split("/")
    if len(parts) != 2:
        return False
    bottom = parts[1].strip().strip("()").strip().replace(" ", "")
    top = parts[0].strip().strip("()").strip().replace(" ", "")
    return bool(re.fullmatch(r"10+", bottom)) and bool(re.fullmatch(r"[0-9]{1,30}", top))


def irreducible(text, value):
    """Return True when the text is a whole number or a fraction that cannot be simplified any further."""
    if "/" not in text:
        return value.denominator == 1 and bool(re.fullmatch(r"[0-9]{1,30}", text.strip()))
    top, _, bottom = text.partition("/")
    top, bottom = top.strip().strip("()").strip(), bottom.strip().strip("()").strip()
    if not (re.fullmatch(r"[0-9]{1,30}", top) and re.fullmatch(r"[0-9]{1,30}", bottom)):
        return False
    return int(bottom) > 1 and math.gcd(int(top), int(bottom)) == 1


def check(answer, given):
    """Compare what the student wrote with the correct answer, and say whether it is right."""
    if isinstance(given, int) and not isinstance(given, bool):
        given = str(given)
    if not isinstance(given, str) or len(given) > MAX_LENGTH:
        return Verdict("unreadable")
    if answer.kind == "choice":
        if not _INDEX.match(given.strip()):
            return Verdict("unreadable")
        return Verdict("correct" if int(given) == answer.value else "wrong", int(given))
    if answer.kind == "numbers":
        values = parse_list(given, answer.units)
        if values is None:
            return Verdict("unreadable")
        return Verdict("correct" if values == list(answer.value) else "wrong", values)
    value = parse_number(given, answer.units)
    if value is None:
        return Verdict("unreadable")
    text = clean(given)
    if answer.form == "fraction" and "/" not in text:
        return Verdict("wrong_form", value)
    if answer.form == "decimal_fraction" and not decimal_fraction(text):
        return Verdict("wrong_form", value)
    if answer.form == "irreducible" and not irreducible(text, value):
        return Verdict("wrong_form", value)
    if answer.form == "decimal" and "/" in text:
        return Verdict("wrong_form", value)
    if answer.kind == "between":
        return Verdict("correct" if answer.value < value < answer.high else "wrong", value)
    return Verdict("correct" if value == answer.value else "wrong", value)


def show(value):
    """Write an exact fraction the French way: a decimal comma when it is a finite decimal, else a fraction."""
    value = Fraction(value)
    denominator = value.denominator
    for prime in (2, 5):
        while denominator % prime == 0:
            denominator //= prime
    if denominator != 1:
        return f"{value.numerator}/{value.denominator}"
    places = 0
    while (value * 10**places).denominator != 1:
        places += 1
    whole = value * 10**places
    digits = str(abs(whole.numerator)).rjust(places + 1, "0")
    text = digits[:-places] + "," + digits[-places:] if places else digits
    return ("-" if value < 0 else "") + text
