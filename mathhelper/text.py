"""Safe rendering of Markdown that contains LaTeX math."""
import re

from markdown_it import MarkdownIt
from markupsafe import Markup, escape

_markdown = MarkdownIt("js-default", {"html": False, "breaks": True, "typographer": False})
_MATH = re.compile(r"\$\$.+?\$\$|\\\[.+?\\\]|\\\(.+?\\\)|\$[^\s$](?:[^$\n]*?[^\s$])?\$", re.S)
_COMMAND = re.compile(r"\\[a-zA-Z]+")
_NAMED = re.compile(r"\\(?:text|mathrm|operatorname|mathbf|begin|end)\{[^{}]*\}")
_TRIGGER = re.compile(r"\\[a-zA-Z]|\^")
_DOUBLED = re.compile(r"\\\\(?=[a-zA-Z]{2,})")
_ALLOWED = re.compile(r"[\\A-Za-z0-9=+\-*/^_().,;:!?{}\[\]|<>%'&]+")
_WORDS = {"a", "i", "an", "as", "at", "be", "by", "do", "if", "in", "is", "it", "no", "of", "on", "or", "so", "to", "we",
          "au", "de", "du", "en", "et", "il", "la", "le", "ou", "un"}


def _formula_piece(token):
    """Return True for a word that reads as part of a formula rather than prose."""
    core = token.rstrip(".,;:!?")
    if not core or not _ALLOWED.fullmatch(core) or core.lower() in _WORDS:
        return False
    return not re.search(r"[A-Za-z]{3,}", _COMMAND.sub("", _NAMED.sub("", core)))


def _wrap_plain(piece):
    """Put dollar signs around formulas written without them in a stretch of plain text."""
    parts, out, run = re.split(r"(\s+|\*\*)", piece), [], []

    def flush():
        text = "".join(run)
        core = text.rstrip()
        tail = re.search(r"[.,;:!?]*$", core).group(0)
        formula = core[: len(core) - len(tail)]
        out.append(f"${formula}${tail}{text[len(core):]}" if formula and _TRIGGER.search(formula) else text)
        run.clear()

    for index, part in enumerate(parts):
        if index % 2 and part.isspace() and run:
            run.append(part)
        elif not index % 2 and part and _formula_piece(part):
            run.append(part)
        else:
            flush()
            out.append(part)
    flush()
    return "".join(out)


def mark_math(text):
    """Turn LaTeX written without dollar signs, such as \\frac{13}{6}, into math that renders as a real fraction."""
    text = text or ""
    if "\\" not in text and "^" not in text:
        return text
    pieces, last = [], 0
    for match in _MATH.finditer(text):
        pieces.append(_wrap_plain(text[last:match.start()]))
        pieces.append(_DOUBLED.sub(lambda _found: "\\", match.group(0)))
        last = match.end()
    pieces.append(_wrap_plain(text[last:]))
    return "".join(pieces)


def tall_fractions(text):
    """Draw fractions at full size, the way they are written by hand, for answers and lines of working."""
    return re.sub(r"\\frac(?=\s*\{)", lambda _found: "\\dfrac", mark_math(text))


def _protect(text):
    """Swap math out for placeholders so Markdown does not touch it."""
    saved = []

    def stash(match):
        saved.append(match.group(0))
        return f"MATHSLOT{len(saved) - 1}END"

    return _MATH.sub(stash, mark_math(text)), saved


def _restore(html, saved):
    """Put the escaped math back in place of the placeholders."""
    return re.sub(r"MATHSLOT(\d+)END", lambda m: str(escape(saved[int(m.group(1))])), html)


def rich(text):
    """Render block Markdown with math left intact for KaTeX."""
    body, saved = _protect(text)
    return Markup(_restore(_markdown.render(body), saved))


def rich_inline(text):
    """Render a single line of Markdown with math left intact for KaTeX."""
    body, saved = _protect(text)
    return Markup(_restore(_markdown.renderInline(body), saved))


def plain(text, limit=120):
    """Strip math markers and Markdown for short previews."""
    cleaned = re.sub(r"\$+|\\[()\[\]]|[*_`#>]", "", text or "")
    cleaned = re.sub(r"\\(frac|dfrac)\{([^}]*)\}\{([^}]*)\}", r"\2/\3", cleaned)
    cleaned = re.sub(r"\\(cdot|times)", "×", cleaned)
    cleaned = re.sub(r"\\([a-zA-Z]+)", r"\1", cleaned)
    cleaned = re.sub(r"[{}]", "", cleaned)
    cleaned = " ".join(cleaned.split())
    return cleaned if len(cleaned) <= limit else cleaned[: limit - 3].rstrip() + "..."
