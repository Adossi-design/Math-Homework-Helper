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
HIDDEN = re.compile(r"\$\$.+?\$\$|\$[^$]+?\$|[0-9]+(?:[.,][0-9]+)*|(?<![^\W\d_])[A-Z](?: [A-Z]){3,}(?![^\W\d_])|(?<=pour )[A-Z](?![^\W\d_])", re.S)
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
    """Replace every formula and every number with a numbered marker, returning the masked text and the spans."""
    spans = []

    def hide(match):
        spans.append(match.group(0))
        return f"⟦{len(spans)}⟧"

    return HIDDEN.sub(hide, text), spans


def convert_number(span, source, target):
    """Write the decimal marker of the target language in a formula or a plain number: a comma in French, a point in English."""
    if (source, target) == ("fr", "en"):
        return re.sub(r"(?<=\d),(?=\d)", ".", span.replace("{,}", "."))
    if (source, target) == ("en", "fr"):
        return re.sub(r"(?<=\d)\.(?=\d)", "{,}" if span.startswith("$") else ",", span)
    return span


def convert_plain(text, source, target):
    """Write decimal numbers in running text with the decimal marker of the target language, whatever the model did."""
    if (source, target) == ("fr", "en"):
        # English has no space before a colon, semicolon, question mark or exclamation mark.
        return re.sub(r"[   ]+([:;?!])", r"\1", re.sub(r"(?<=\d),(?=\d)", ".", text))
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


def same_math(source, edited, source_lang, target_lang):
    """Return True when a corrected translation keeps exactly the formulas and numbers of the source text."""
    wanted = sorted(convert_number(span, source_lang, target_lang) for span in protect(source)[1])
    return wanted == sorted(protect(edited)[1])


def needs_translation(masked):
    """Return True when the text has words, so pure numbers and formulas are left alone."""
    return bool(WORDS.search(HOLE.sub("", masked)))


def translate_texts(texts, source, target):
    """Translate each text, reusing stored translations. Sentences that differ only in their formulas share one stored translation."""
    if source == target:
        return list(texts), False
    result, wanted, fallback = {}, {}, False
    for text in dict.fromkeys(texts):
        masked, spans = protect(text)
        if text.strip() == "," and (source, target) == ("fr", "en"):
            result[text] = "."
        elif not needs_translation(masked):
            result[text] = convert_number(text, source, target)
        else:
            wanted.setdefault(masked, []).append((text, spans))
    missing = dict(wanted)
    if wanted:
        keys = {digest(masked, source): masked for masked in wanted}
        rows = db.session.scalars(select(TranslationCache).where(TranslationCache.digest.in_(list(keys)), TranslationCache.lang == target)).all()
        for row in rows:
            masked = keys[row.digest]
            missing.pop(masked, None)
            for text, spans in wanted[masked]:
                final = restore(row.text, spans, source, target)
                if final is None:
                    log.warning("The stored translation of %r does not keep its formulas, so the original is shown.", text[:60])
                    fallback = True
                else:
                    result[text] = final
    if missing:
        fallback = fill(result, missing, source, target) or fallback
    return [result.get(text, text) for text in texts], fallback


def fill(result, missing, source, target):
    """Translate the sentences that are not stored yet and store the good ones. Returns True if any text stayed in the original language."""
    pending = list(missing.items())
    try:
        translated = ai.translate_batch([masked for masked, _ in pending], source, target)
    except ai.AIError as exc:
        log.warning("Translation to %s failed: %s", target, exc)
        return True
    fallback = False
    for (masked, entries), new in zip(pending, translated):
        finals = [(text, restore(new, spans, source, target)) for text, spans in entries]
        if any(final is None for _, final in finals):
            log.warning("Translation to %s changed the math in %r, so the original was kept.", target, entries[0][0][:60])
            fallback = True
            continue
        result.update(finals)
        db.session.add(TranslationCache(digest=digest(masked, source), lang=target, source=entries[0][0], text=new))
    try:
        db.session.commit()
    except IntegrityError:
        # Another request stored the same sentence at the same moment.
        db.session.rollback()
    return fallback


def shown_translation(row):
    """Return a stored translation written with the formulas of the text it was first made from, so an admin can read it."""
    source_lang = "fr" if row.lang == "en" else "en"
    spans = protect(row.source)[1]
    return restore(row.text, spans, source_lang, row.lang) or row.text


def correct_translation(row, edited):
    """Store a corrected translation if it keeps exactly the formulas of the source. Returns False when it does not."""
    source_lang = "fr" if row.lang == "en" else "en"
    if not same_math(row.source, edited, source_lang, row.lang):
        return False
    masked, spans = protect(edited)
    wanted = [convert_number(span, source_lang, row.lang) for span in protect(row.source)[1]]
    place, taken = {}, set()
    for position, span in enumerate(wanted, 1):
        index = next(i for i, found in enumerate(spans, 1) if found == span and i not in taken)
        taken.add(index)
        place[index] = position
    row.text = HOLE.sub(lambda m: f"⟦{place[int(m.group(1))]}⟧", masked)
    row.reviewed = True
    return True


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
