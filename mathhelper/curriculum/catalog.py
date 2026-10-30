"""Countries, curricula, academic levels and the chapters that exist for them.

A level is only listed with chapters when real content has been written and checked for it. Everything else is shown as not yet available,
so no curriculum is presented as supported before it is.
"""
from dataclasses import dataclass

from .chapters.sn_6e_angles import CHAPTER as SN_6E_ANGLES
from .chapters.sn_6e_decimaux import CHAPTER as SN_6E_DECIMAUX
from .chapters.sn_6e_calcul import CHAPTER as SN_6E_CALCUL
from .chapters.sn_6e_division import CHAPTER as SN_6E_DIVISION
from .chapters.sn_6e_droites_cercles import CHAPTER as SN_6E_DROITES_CERCLES
from .chapters.sn_6e_entiers import CHAPTER as SN_6E_ENTIERS
from .chapters.sn_6e_fractions import CHAPTER as SN_6E_FRACTIONS
from .chapters.sn_6e_multiplication import CHAPTER as SN_6E_MULTIPLICATION
from .chapters.sn_6e_parallelogramme import CHAPTER as SN_6E_PARALLELOGRAMME
from .chapters.sn_6e_proportionnalite import CHAPTER as SN_6E_PROPORTIONNALITE
from .chapters.sn_6e_relatifs import CHAPTER as SN_6E_RELATIFS
from .chapters.sn_6e_solides import CHAPTER as SN_6E_SOLIDES
from .chapters.sn_6e_symetrie import CHAPTER as SN_6E_SYMETRIE
from .chapters.sn_6e_triangles import CHAPTER as SN_6E_TRIANGLES
from .chapters.sn_6e_statistique import CHAPTER as SN_6E_STATISTIQUE

FRANCOPHONE_LEVELS = [
    ("6e", "Sixième", "Sixième", 6), ("5e", "Cinquième", "Cinquième", 7), ("4e", "Quatrième", "Quatrième", 8),
    ("3e", "Troisième", "Troisième", 9), ("2nde", "Seconde", "Seconde", 10), ("1ere", "Première", "Première", 11),
    ("tle", "Terminale", "Terminale", 12),
]


@dataclass(frozen=True)
class Level:
    id: str
    en: str
    fr: str
    grade: int  # the rough Grade equivalent, used only to order levels and to pick general guidance for the AI


@dataclass(frozen=True)
class Country:
    id: str
    en: str
    fr: str
    language: str
    levels: tuple


def _levels(rows):
    return tuple(Level(*row) for row in rows)


COUNTRIES = {
    "sn": Country("sn", "Senegal", "Sénégal", "fr", _levels(FRANCOPHONE_LEVELS)),
    "ci": Country("ci", "Côte d'Ivoire", "Côte d'Ivoire", "fr", _levels(FRANCOPHONE_LEVELS)),
    "td": Country("td", "Chad", "Tchad", "fr", _levels(FRANCOPHONE_LEVELS)),
    "rw": Country("rw", "Rwanda", "Rwanda", "en", _levels(
        [("p6", "Primary 6", "Primaire 6", 6)] + [(f"s{n}", f"Senior {n}", f"Senior {n}", 6 + n) for n in range(1, 7)])),
    "za": Country("za", "South Africa", "Afrique du Sud", "en", _levels([(f"g{n}", f"Grade {n}", f"Grade {n}", n) for n in range(6, 13)])),
}

CHAPTERS = [SN_6E_DECIMAUX, SN_6E_MULTIPLICATION, SN_6E_DIVISION, SN_6E_CALCUL, SN_6E_PROPORTIONNALITE, SN_6E_FRACTIONS, SN_6E_RELATIFS, SN_6E_ENTIERS, SN_6E_STATISTIQUE, SN_6E_SOLIDES, SN_6E_DROITES_CERCLES, SN_6E_ANGLES, SN_6E_TRIANGLES, SN_6E_PARALLELOGRAMME, SN_6E_SYMETRIE]
CHAPTER_BY_ID = {chapter.id: chapter for chapter in CHAPTERS}


def country(country_id):
    """Return the country with this id, or None."""
    return COUNTRIES.get(country_id)


def level(country_id, level_id):
    """Return the level of a country, or None when the country has no such level."""
    found = COUNTRIES.get(country_id)
    return next((lv for lv in found.levels if lv.id == level_id), None) if found else None


def valid_choice(country_id, level_id):
    """Return True when the level exists in the country, or when neither is chosen."""
    if not country_id and not level_id:
        return True
    return level(country_id, level_id) is not None


def chapters_for(country_id, level_id):
    """Return the chapters written for this country and level, in teaching order."""
    found = [c for c in CHAPTERS if c.level == level_id and country_id in (c.country, *c.also_for)]
    return sorted(found, key=lambda c: c.number)


def find_chapter(chapter_id):
    """Return a chapter by id, or None."""
    return CHAPTER_BY_ID.get(chapter_id)


def label(item, lang):
    """Return the name of a country or level in the given language."""
    return item.fr if lang == "fr" else item.en


def available_levels():
    """Return the (country id, level id) pairs that have at least one chapter."""
    return sorted({(country_id, c.level) for c in CHAPTERS for country_id in (c.country, *c.also_for)})
