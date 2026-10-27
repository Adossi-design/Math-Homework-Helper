"""The shapes of curriculum content: sources, exercises, lesson sections and chapters."""
from dataclasses import dataclass, field
from typing import Callable

from .checker import Answer


@dataclass(frozen=True)
class Source:
    """A textbook or official document that informed the content, with what it may be used for."""

    id: str
    title: str
    publisher: str
    url: str
    licence: str
    use: str  # what this project took from it
    attribution: str = ""


@dataclass
class Exercise:
    """One question with a machine-checkable answer, progressive hints and a worked solution."""

    id: str
    concept: str
    prompt: str
    answer: Answer
    hints: list = field(default_factory=list)
    solution: list = field(default_factory=list)
    options: list = field(default_factory=list)
    level: int = 1
    wrong: dict = field(default_factory=dict)  # a typical wrong answer (as shown by checker.show or option index) -> what went wrong


@dataclass
class Section:
    """One part of a chapter, short enough to study in a sitting."""

    id: str
    title: str
    minutes: int
    concept: str
    goal: str
    blocks: list
    guided: list


@dataclass
class Chapter:
    """A complete chapter of one curriculum at one level."""

    id: str
    country: str
    level: str
    number: int
    title: str
    language: str  # the language the content was written in
    intro: str
    objectives: list
    prerequisites: list
    sections: list
    practice: list
    summary: list
    concepts: dict  # concept id -> (name shown to the student, id of the section that teaches it)
    assessment: Callable  # random.Random -> list[Exercise]
    sources: list
    status_note: str = ""
    also_for: tuple = ()  # other countries whose official programme lists the same contents, checked against its text
    assessment_version: int = 1  # raise it whenever the assessment generator changes, so old attempts are not shown with new questions

    def section(self, section_id):
        """Return the section with this id, or None."""
        return next((s for s in self.sections if s.id == section_id), None)

    def concept_section(self, concept):
        """Return the section that teaches a concept, used to point students to the right revision."""
        entry = self.concepts.get(concept)
        return self.section(entry[1]) if entry else None

    def exercises(self):
        """Return every fixed exercise of the chapter by id."""
        found = {e.id: e for e in self.practice}
        for section in self.sections:
            found.update({e.id: e for e in section.guided})
        return found
