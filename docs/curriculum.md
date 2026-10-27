# Curriculum chapters

This describes how the curriculum part of the app works, how to add a chapter and what must be true before one is offered to students.

## How a chapter is built

A chapter is one Python file in `mathhelper/curriculum/chapters/`, written in the language of its source (French for the Francophone chapters). It is a `Chapter` (see `curriculum/model.py`) with:

- **sections** with blocks (paragraphs, definitions, rules, worked examples, warnings, tables) and guided exercises;
- **practice**: independent exercises from easy to hard;
- **summary**;
- **assessment**: a function that builds 12 fresh questions from a seeded random generator, so every retake has new numbers and the corrections can be rebuilt from the seed;
- **concepts**: each concept points to the section that teaches it, which is how revision advice finds the right lesson.

Every fixed exercise has an `Answer` that is checked exactly with fractions (`curriculum/checker.py`). Forms can be required: `decimal`, `fraction`, `decimal_fraction` and `irreducible`. Units are accepted after a number. Every worked example has a `verify` expression that the tests evaluate, so a printed result cannot drift from the arithmetic.

## Adding a chapter

1. Write the chapter file, using `chapters/kit.py` for the builders (`make_kit(chapter_id, default_form=...)`).
2. Register it in `curriculum/catalog.py`. Use `also_for=("ci",)` only for a country whose official programme text was read and lists the same contents.
3. Add the French text of its `status_note` to `translations/fr_curriculum.py` (a test fails if it is missing).
4. Add tests: an independent recalculation of every fixed answer and of the assessment answers parsed back from the prompts (see `tests/test_chapters.py` and the other `tests/test_chapter_*.py`).
5. Have the chapter reviewed by someone who did not write it (math, wording, answer keys, required forms, repeated numbers) before it goes live, and keep the findings fixed and re-tested.

## Sources and licences

- ADEM-Dakar Sixième booklet (Senegal): a free exercise booklet, "interdit à la vente", no open licence. Used only to decide which topics belong in each chapter. No text, exercise or figure is copied.
- Côte d'Ivoire Sixième mathematics programme: an official programme with no licence statement. Used only to read the list of contents for lessons 9 to 13; nothing is copied.
- Rwanda Basic Education Board books: "All rights reserved", credit required when quoting. Not used.
- Siyavula Everything Maths: the branded books are CC BY-ND (no adaptation). Only the unbranded CC BY editions may be adapted, with credit to Siyavula. Not used yet.

Each chapter page lists its sources with their licences.

## What is not done

- No chapter has been checked against the official Senegalese programme, because it was not found.
- Only the number and data part of Sixième is written. The geometry lessons, and every other level and country, are not.
- English text is machine translated and should be read by a person (Admin → Translations).
