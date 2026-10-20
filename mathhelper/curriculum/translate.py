"""Translation of lesson text with a stored cache: math is set aside before translating and put back afterwards unchanged."""
import hashlib
import logging
import re
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from .. import ai
from ..extensions import db
from ..models import TranslationCache

log = logging.getLogger(__name__)

MATH = re.compile(r"\$\$.+?\$\$|\$[^$]+?\$", re.S)
HOLE = re.compile(r"⟦(\d+)⟧")
WORDS = re.compile(r"[^\W\d_]{2,}")
SKIP_KEYS = {"type", "id", "concept", "verify", "kind", "value", "course", "lesson", "given", "status", "level", "form"}


@dataclass
class Localized:
    """Translated content, and whether any of it had to fall back to the original language."""

    content: object
    fallback: bool = False


def digest(text, source):
    """Return the cache key of a piece of text written in a given language."""
    return hashlib.sha256(f"{source}\n{text}".encode()).hexdigest()


def protect(text):
    """Replace every math span with a numbered marker, returning the masked text and the spans."""
    spans = []

    def hide(match):
        spans.append(match.group(0))
        return f"⟦{len(spans)}⟧"

    return MATH.sub(hide, text), spans


def convert_number(span, source, target):
    """Write the decimal marker of the target language inside a math span: a comma in French, a point in English."""
    if (source, target) == ("fr", "en"):
        return span.replace("{,}", ".")
    if (source, target) == ("en", "fr"):
        return re.sub(r"(?<=\d)\.(?=\d)", "{,}", span)
    return span


def convert_plain(text, source, target):
    """Write decimal numbers in running text with the decimal marker of the target language, whatever the model did."""
    if (source, target) == ("fr", "en"):
        return re.sub(r"(?<=\d),(?=\d)", ".", text)
    if (source, target) == ("en", "fr"):
        return re.sub(r"(?<=\d)\.(?=\d)", ",", text)
    return text


def restore(masked, spans, source, target):
    """Put the math spans back, or return None when the translation lost, repeated or invented one."""
    found = [int(n) for n in HOLE.findall(masked)]
    if sorted(found) != list(range(1, len(spans) + 1)):
        return None
    masked = convert_plain(masked, source, target)
    return HOLE.sub(lambda m: convert_number(spans[int(m.group(1)) - 1], source, target), masked)


def needs_translation(masked):
    """Return True when the text has words, so pure numbers and formulas are left alone."""
    return bool(WORDS.search(HOLE.sub("", masked)))


def translate_texts(texts, source, target):
    """Translate each text from source to target, using stored translations and asking the AI only for the missing ones."""
    if source == target:
        return list(texts), False
    result, missing, fallback = {}, {}, False
    for text in dict.fromkeys(texts):
        masked, spans = protect(text)
        if text.strip() == "," and (source, target) == ("fr", "en"):
            result[text] = "."
        elif not needs_translation(masked):
            result[text] = convert_number(text, source, target)
        else:
            missing[text] = (masked, spans)
    if missing:
        keys = {digest(text, source): text for text in missing}
        rows = db.session.scalars(select(TranslationCache).where(TranslationCache.digest.in_(list(keys)), TranslationCache.lang == target)).all()
        for row in rows:
            result[keys[row.digest]] = row.text
            missing.pop(keys[row.digest], None)
    if missing:
        fallback = fill(result, missing, source, target)
    return [result.get(text, text) for text in texts], fallback


def fill(result, missing, source, target):
    """Translate the texts that are not stored yet and store the good ones. Returns True if any text stayed in the original language."""
    pending = list(missing.items())
    try:
        translated = ai.translate_batch([masked for _, (masked, _) in pending], source, target)
    except ai.AIError as exc:
        log.warning("Translation to %s failed: %s", target, exc)
        return True
    fallback = False
    for (text, (masked, spans)), new in zip(pending, translated):
        final = restore(new, spans, source, target)
        if final is None:
            log.warning("Translation to %s changed the math in %r, so the original was kept.", target, text[:60])
            fallback = True
            continue
        result[text] = final
        db.session.add(TranslationCache(digest=digest(text, source), lang=target, source=text, text=final))
    try:
        db.session.commit()
    except IntegrityError:
        # Another request stored the same text at the same moment.
        db.session.rollback()
    return fallback


def walk(node, action, key=None):
    """Rebuild a structure of dicts and lists, passing every translatable string through action."""
    if isinstance(node, str):
        return node if key in SKIP_KEYS else action(node)
    if isinstance(node, list):
        return [walk(item, action, key) for item in node]
    if isinstance(node, dict):
        return {k: walk(v, action, k) for k, v in node.items()}
    return node


def localize(tree, source, target):
    """Return the structure translated into the target language, plus whether any text fell back to the original."""
    if source == target:
        return Localized(tree)
    texts = []
    walk(tree, lambda s: texts.append(s) or s)
    translated, fallback = translate_texts(texts, source, target)
    table = dict(zip(texts, translated))
    return Localized(walk(tree, lambda s: table[s]), fallback)
