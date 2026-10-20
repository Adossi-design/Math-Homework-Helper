"""Language choice, translation lookups and localized dates."""
import re

from flask import g, has_request_context, request

from .translations.fr import FR

LANGUAGES = {"en": "English", "fr": "Français"}
COOKIE = "lang"
CATALOGS = {"fr": FR}
NBSP = chr(160)
_PUNCTUATION = re.compile(r" ([?!:;»])")

DAYS = {
    "en": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    "fr": ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"],
}
MONTHS = {
    "en": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
    "fr": ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"],
}
SHORT_MONTHS = {
    "en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    "fr": ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."],
}
JS_KEYS = [
    "Please choose an image file.", "That photo is over 12 MB. Please use a smaller one.",
    "That photo is too large to upload. Please crop it and try again.", "Pasted image",
    "Choose or take a photo first.", "Type the problem you want solved.", "Reading your problem",
    "Working through each step", "Double checking the math", "Writing up the explanation",
    "Show the first step", "Show the next step ({left} left)", "Saved", "Save", "Saved to your library.",
    "Removed from saved.", "Thinking", "Something went wrong. Please try again.", "Correct!", "Not quite",
    "See results", "Next", "Leave this round? Your answers so far will not be saved.", "Hide password",
    "Show password", "Dismiss", "Write or choose an answer first.", "Hint {n}",
]


def pick_language():
    """Choose the language from the saved cookie, then the browser, then English."""
    saved = request.cookies.get(COOKIE)
    if saved in LANGUAGES:
        return saved
    return request.accept_languages.best_match(list(LANGUAGES)) or "en"


def language():
    """Return the language of the current request, or English outside of one."""
    return getattr(g, "lang", "en") if has_request_context() else "en"


def polish(text, lang):
    """Keep French punctuation attached to the word before it."""
    return _PUNCTUATION.sub(NBSP + r"\1", text) if lang == "fr" else text


def gettext(text, ctx=None, **values):
    """Translate a source string, with an optional context and named values."""
    lang = language()
    catalog = CATALOGS.get(lang, {})
    translated = catalog.get(f"{text}|{ctx}") if ctx else None
    translated = polish(translated or catalog.get(text, text), lang)
    return translated.format(**values) if values else translated


def ngettext(singular, plural, n, **values):
    """Translate the singular or plural form that fits the number."""
    one = n < 2 if language() == "fr" else n == 1
    return gettext(singular if one else plural, n=n, **values)


def pick(english, french):
    """Return the text written for the current language."""
    lang = language()
    return polish(french, lang) if lang == "fr" else english


def format_date(moment, style="date"):
    """Write a date in the current language as a long day, a month and year, or a short date."""
    lang = language()
    day, month = DAYS[lang][moment.weekday()], MONTHS[lang][moment.month - 1]
    if style == "day":
        return f"{day} {moment.day} {month}" if lang == "fr" else f"{day}, {month} {moment.day}"
    if style == "month":
        return f"{month} {moment.year}"
    short = SHORT_MONTHS[lang][moment.month - 1]
    return f"{moment.day} {short} {moment.year}" if lang == "fr" else f"{short} {moment.day}, {moment.year}"


def day_label(moment):
    """Return a two letter weekday label for the activity strip."""
    return DAYS[language()][moment.weekday()][:2].capitalize()


def js_strings():
    """Return the translated strings used by the browser code, or nothing for English."""
    if language() == "en":
        return {}
    return {key: gettext(key) for key in JS_KEYS}
