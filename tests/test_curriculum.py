"""Curriculum chapter: exact answer checking, content correctness, translation, and the full student journey."""
import random
import re
from fractions import Fraction

import pytest

from mathhelper import ai
from mathhelper.curriculum import checker, translate
from mathhelper.curriculum.catalog import CHAPTERS
from mathhelper.curriculum.chapters.sn_6e_decimaux import CHAPTER, assessment, d
from mathhelper.extensions import db
from mathhelper.models import ChapterAttempt, ExerciseResult, TranslationCache, TutorQuestion, User

CID = CHAPTER.id
FRENCH = {"Accept-Language": "fr-FR,fr;q=0.9,en;q=0.5"}


# ----- Exact answer checking -----

@pytest.mark.parametrize("typed", ["3,5", "3.5", " 3,50 ", "7/2", "\\frac{7}{2}", "$3{,}5$", "3,5 m", "14/4", "35/10", "03,5"])
def test_equivalent_ways_of_writing_a_number_are_all_correct(typed):
    assert checker.check(checker.Answer("number", Fraction(7, 2), ("m",)), typed).status == "correct"


@pytest.mark.parametrize("typed,status", [("3,05", "wrong"), ("35", "wrong"), ("0,35", "wrong"), ("", "unreadable"), ("abc", "unreadable"),
                                          ("1/0", "unreadable"), ("3,5,5", "unreadable"), ("3,5 kg", "unreadable"), ("3 / 2 / 1", "unreadable"), ("--3", "unreadable")])
def test_wrong_and_unreadable_answers_are_told_apart(typed, status):
    assert checker.check(checker.Answer("number", Fraction(7, 2), ("m",)), typed).status == status


def test_thousand_separators_and_negative_numbers():
    answer = checker.Answer("number", Fraction(1353287))
    for typed in ["1 353 287", "1.353.287", "1353287", "1 353 287"]:
        assert checker.check(answer, typed).status == "correct", typed
    assert checker.check(checker.Answer("number", Fraction(-5, 2)), "-2,5").status == "correct"
    assert checker.check(checker.Answer("number", Fraction(-5, 2)), "−2,5").status == "correct"


def test_required_form_is_enforced_but_value_still_matters():
    fraction = checker.Answer("number", Fraction(3125, 1000), form="decimal_fraction")
    assert checker.check(fraction, "3125/1000").status == "correct"
    assert checker.check(fraction, "\\frac{3125}{1000}").status == "correct"
    assert checker.check(fraction, "3,125").status == "wrong_form"
    assert checker.check(fraction, "25/8").status == "wrong_form"
    assert checker.check(fraction, "3,125/1").status == "wrong_form"
    assert checker.check(fraction, "3124/1000").status == "wrong"


def test_ordered_lists_between_and_choice_answers():
    ordered = checker.Answer("numbers", (Fraction(598, 100), Fraction(602, 100), Fraction(62, 10)))
    for typed in ["5,98 ; 6,02 ; 6,2", "5,98<6,02<6,20", "5.98;6.02;6.2", "5,98 6,02 6,2"]:
        assert checker.check(ordered, typed).status == "correct", typed
    assert checker.check(ordered, "6,2 ; 6,02 ; 5,98").status == "wrong"
    assert checker.check(ordered, "5,98 ; 6,02").status == "wrong"
    between = checker.Answer("between", Fraction(13, 10), high=Fraction(14, 10))
    assert checker.check(between, "1,35").status == "correct"
    assert checker.check(between, "1,3").status == "wrong" and checker.check(between, "1,4").status == "wrong"
    choice = checker.Answer("choice", 1)
    assert checker.check(choice, "1").status == "correct" and checker.check(choice, "0").status == "wrong"
    assert checker.check(choice, "x").status == "unreadable"


def test_show_writes_exact_numbers_the_french_way():
    assert [checker.show(Fraction(*p)) for p in [(7, 2), (5, 1), (1, 1000), (-5, 4), (1, 3)]] == ["3,5", "5", "0,001", "-1,25", "1/3"]


# ----- Content correctness, checked independently of the code that built it -----

def test_every_worked_example_verifies_with_exact_arithmetic():
    count = 0
    for section in CHAPTER.sections:
        for block in section.blocks:
            if block["type"] == "example":
                assert eval(block["verify"], {"d": d}), (section.id, block["title"])
                count += 1
    assert count >= 22


def test_fixed_exercises_have_unique_ids_hints_and_solutions_and_accept_their_own_answer():
    exercises = list(CHAPTER.practice) + [e for s in CHAPTER.sections for e in s.guided]
    assert len({e.id for e in exercises}) == len(exercises)
    for e in exercises:
        assert e.hints and e.solution and e.concept in CHAPTER.concepts, e.id
        if e.answer.kind == "choice":
            typed = str(e.answer.value)
        elif e.answer.kind == "numbers":
            typed = " ; ".join(checker.show(v) for v in e.answer.value)
        elif e.answer.kind == "between":
            typed = checker.show((e.answer.value + e.answer.high) / 2)
        elif e.answer.form == "decimal_fraction":
            typed = f"{int(e.answer.value * 1000)}/1000"
        else:
            typed = checker.show(e.answer.value)
        assert checker.check(e.answer, typed).status == "correct", e.id
        if e.answer.kind == "choice":
            assert 0 <= e.answer.value < len(e.options)


# The answers below are typed again here, directly from the question, and not taken from the chapter file.
INDEPENDENT = {
    "s1-g1": Fraction(47, 100), "s1-g2": Fraction(3125, 1000), "s1-g3": 2, "s1-g4": 2,
    "s2-g1": 7, "s2-g2": Fraction(6, 100), "s2-g3": Fraction(7, 1000), "s2-g4": 1, "s2-g5": Fraction(708, 1000),
    "s3-g1": 1, "s3-g4": 8,
    "s4-g1": Fraction(1760 + 485, 100), "s4-g2": 14, "s4-g3": 100, "s4-g4": 2,
    "s5-g1": Fraction(2540 - 867, 100), "s5-g2": Fraction(600 - 245, 100), "s5-g3": Fraction(900 - 375 - 250, 100), "s5-g4": Fraction(800 - 360, 100),
    "p1": Fraction(358, 100), "p2": Fraction(9, 1000), "p3": Fraction(13, 1000), "p4": Fraction(35, 100), "p5": 5, "p6": 2,
    "p7": 804, "p8": 9, "p9": Fraction(4, 100), "p10": Fraction(305, 1000), "p11": 608, "p12": 39, "p13": Fraction(78, 10), "p14": Fraction(94, 10),
    "p15": 1, "p18": Fraction(151, 10), "p19": 100, "p20": 1,
    "p21": Fraction(640 + 235, 100), "p22": Fraction(90 + 1200 + 75 + 710, 100), "p23": 1, "p24": 100, "p25": 0, "p26": 1, "p27": Fraction(1250 + 875 + 625, 100),
    "p28": Fraction(98 - 35, 10), "p29": Fraction(1500 - 726, 100), "p30": Fraction(1000 - 435, 100), "p31": Fraction(10000 - 1, 100), "p32": Fraction(100000 - 9999, 100),
    "p33": 0, "p34": Fraction(5000 - 1875 - 1350, 100),
}


def test_fixed_exercise_answers_match_an_independent_recalculation():
    by_id = {e.id.split("/")[1]: e for e in CHAPTER.exercises().values()}
    for key, value in INDEPENDENT.items():
        answer = by_id[key].answer
        assert answer.value == Fraction(value), (key, answer.value, value)


def test_ordering_exercises_are_sorted_correctly():
    by_id = {e.id.split("/")[1]: e for e in CHAPTER.exercises().values()}
    assert list(by_id["s3-g2"].answer.value) == sorted(map(d, ["6,2", "6,02", "6,25", "5,98"]))
    assert list(by_id["p16"].answer.value) == sorted(map(d, ["0,8", "0,78", "0,087", "0,807"]), reverse=True)


def test_every_fixed_exercise_is_covered_by_the_independent_recalculation_or_is_an_ordering_or_between_question():
    covered = set(INDEPENDENT) | {"s3-g2", "s3-g3", "p16", "p17"}
    assert covered == {e.id.split("/")[1] for e in CHAPTER.exercises().values()}


def test_required_forms_stop_students_from_typing_the_question_back():
    by_id = {e.id.split("/")[1]: e for e in CHAPTER.exercises().values()}
    for key, typed in [("s1-g1", "47/100"), ("p1", "358/100"), ("p3", "13/1000"), ("p4", "7/20")]:
        assert checker.check(by_id[key].answer, typed).status == "wrong_form", key
    assert checker.check(by_id["s3-g3"].answer, "27/20").status == "wrong_form"
    assert checker.check(by_id["s3-g3"].answer, "1,35").status == "correct"


def test_hints_never_give_the_final_answer_away():
    for e in CHAPTER.exercises().values():
        if e.answer.kind in ("number",) and len(checker.show(e.answer.value)) >= 2:
            shown = checker.show(e.answer.value)
            if shown in re.sub(r"[^0-9,]", " ", e.prompt).split():
                continue
            for hint in e.hints:
                assert shown not in re.sub(r"[^0-9,]", " ", hint).split(), (e.id, hint)


NUMBER = r"\$([0-9{,}]+)\$"


def decimal(text):
    """Read a number such as 12{,}5 from a prompt."""
    return d(text.replace("{,}", ","))


def test_assessment_answer_keys_match_a_recalculation_from_each_prompt_for_many_seeds():
    for seed in range(300):
        questions = assessment(random.Random(f"seed{seed}"))
        assert [q.id.split("/")[1] for q in questions] == [f"a{i}" for i in range(1, 13)]
        q = {q.id.split("/")[1]: q for q in questions}
        assert q["a4"].answer.value != 0
        bounded = decimal(re.search(r"\$([0-9{,}]+)\$", q["a11"].prompt).group(1))
        assert q["a11"].answer.value == int(bounded) + 1 and bounded != int(bounded)
        long_text, short_text = re.search(r"« \$([0-9{,}]+)\$ est plus grand que \$([0-9{,}]+)\$", q["a12"].prompt).groups()
        assert decimal(long_text) < decimal(short_text)
        right_text = q["a12"].options[q["a12"].answer.value]
        assert right_text.startswith("Il a tort :") and "plus grand que" in right_text
        assert sum(o.startswith("Il a tort :") and "plus grand que" in o for o in q["a12"].options) == 1
        top, bottom = re.search(r"dfrac\{(\d+)\}\{(\d+)\}", q["a1"].prompt).groups()
        assert q["a1"].answer.value == Fraction(int(top), int(bottom))
        shown = decimal(re.search(r"\$([0-9{,}]+)\$", q["a2"].prompt).group(1))
        assert q["a2"].answer.value == shown and q["a2"].answer.form == "decimal_fraction"
        text = re.search(r"dans \$([0-9{,}]+)\$", q["a3"].prompt).group(1).replace("{,}", ",")
        whole, decimals = text.split(",")
        place = {"dixièmes": 0, "centièmes": 1, "millièmes": 2}[re.search(r"des (\w+) dans", q["a3"].prompt).group(1)]
        assert q["a3"].answer.value == int(decimals[place])
        digit = int(re.search(r"chiffre (\d) dans", q["a4"].prompt).group(1))
        spot = (whole + decimals).index(str(digit))
        assert (whole + decimals).count(str(digit)) == 1
        assert q["a4"].answer.value == digit * Fraction(1, 10) ** (spot - len(whole) + 1)
        options = [decimal(re.search(NUMBER, o).group(1)) for o in q["a5"].options]
        assert len(set(options)) == 3 and options.index(max(options)) == q["a5"].answer.value
        listed = [decimal(x) for x in re.findall(NUMBER, q["a6"].prompt)]
        assert len(set(listed)) == 4 and list(q["a6"].answer.value) == sorted(listed)
        left, right = re.search(r"\$([0-9{,}]+) \+ ([0-9{,}]+)\$", q["a7"].prompt).groups()
        assert q["a7"].answer.value == decimal(left) + decimal(right)
        left, right = re.search(r"\$([0-9{,}]+) - ([0-9{,}]+)\$", q["a8"].prompt).groups()
        assert decimal(left) > decimal(right) and q["a8"].answer.value == decimal(left) - decimal(right)
        numbers = [decimal(x.replace(".", ",")) for x in re.findall(r"(\d+(?:,\d+)?) m", q["a9"].prompt)]
        assert q["a9"].answer.value == numbers[0] - numbers[1] - numbers[2] > 0
        low, high = [decimal(x) for x in re.findall(NUMBER, q["a10"].prompt)]
        assert q["a10"].answer.value == low and q["a10"].answer.high == high and high - low == Fraction(1, 100)
        middle = low + Fraction(1, 1000)
        assert checker.check(q["a10"].answer, checker.show(middle)).status == "correct"
        assert checker.check(q["a10"].answer, checker.show(low)).status == "wrong"


def test_assessment_changes_with_the_seed_and_repeats_with_the_same_seed():
    first, again, other = (assessment(random.Random(s)) for s in ("abcd1234", "abcd1234", "zzzz9999"))
    assert [q.prompt for q in first] == [q.prompt for q in again]
    assert [q.prompt for q in first] != [q.prompt for q in other]


def test_only_the_reference_chapter_exists_and_it_claims_no_unchecked_alignment():
    assert [c.id for c in CHAPTERS][0] == CID and len({c.id for c in CHAPTERS}) == len(CHAPTERS)
    assert all("not been checked against the official Senegalese" in c.status_note for c in CHAPTERS)
    assert "not been checked against the official" in CHAPTER.status_note
    assert {s.id for s in CHAPTER.sources} == {"adem-sn-6e", "ci-programme-6e"}
    assert len(CHAPTER.sections) == 5 and len(CHAPTER.practice) == 34 and sum(len(s.guided) for s in CHAPTER.sections) == 21


def test_some_assessments_include_values_below_one_tenth_so_leading_zeros_are_tested():
    below = sum(any(q.id.endswith("/a1") and q.answer.value < Fraction(1, 10) for q in assessment(random.Random(f"z{seed}"))) for seed in range(100))
    assert below >= 10


def test_the_chapter_text_does_not_reuse_the_booklet_specific_items_that_were_found_to_overlap():
    text = repr([(s.blocks, [e.prompt for e in s.guided]) for s in CHAPTER.sections]) + repr([e.prompt for e in CHAPTER.practice])
    for phrase in ["701", "14,0", "7,75 m", "bazin", "ordre de grandeur de chaque terme", "une seule fois chacun de ces chiffres"]:
        assert phrase not in text, phrase


# ----- Translation keeps the math -----

def test_math_is_set_aside_and_restored_exactly():
    masked, spans = translate.protect("Calcule $12{,}5 + 7$ puis $$x$$.")
    assert masked == "Calcule ⟦1⟧ puis ⟦2⟧." and spans == ["$12{,}5 + 7$", "$$x$$"]
    assert translate.restore("Compute ⟦1⟧ then ⟦2⟧.", spans, "fr", "en") == "Compute $12.5 + 7$ then $$x$$."
    assert translate.restore("Compute ⟦1⟧.", spans, "fr", "en") is None
    assert translate.restore("Compute ⟦1⟧ ⟦1⟧ ⟦2⟧.", spans, "fr", "en") is None
    assert translate.restore("Compute ⟦1⟧ ⟦2⟧ ⟦3⟧.", spans, "fr", "en") is None


def test_translations_are_stored_reused_and_numbers_only_text_is_not_sent(app):
    sent = []

    def fake(texts, source, target):
        sent.append(list(texts))
        return [f"EN {t}" for t in texts]

    original = ai.translate_batch
    ai.translate_batch = fake
    try:
        with app.app_context():
            out, fallback = translate.translate_texts(["Calcule $2{,}5 + 1$.", "$2{,}35$", ",", "Calcule $2{,}5 + 1$."], "fr", "en")
            assert out == ["EN Calcule $2.5 + 1$.", "$2.35$", ".", "EN Calcule $2.5 + 1$."] and not fallback
            assert sent == [["Calcule ⟦1⟧."]]
            out, _ = translate.translate_texts(["Calcule $2{,}5 + 1$."], "fr", "en")
            assert out == ["EN Calcule $2.5 + 1$."] and len(sent) == 1
            assert db.session.query(TranslationCache).count() == 1
    finally:
        ai.translate_batch = original


def test_a_reviewed_correction_wins_and_is_not_overwritten(app):
    with app.app_context():
        text = "Écris le nombre."
        db.session.add(TranslationCache(digest=translate.digest(text, "fr"), lang="en", source=text, text="Write the number (checked).", reviewed=True))
        db.session.commit()
        assert translate.translate_texts([text], "fr", "en")[0] == ["Write the number (checked)."]


def test_a_translation_that_loses_a_formula_is_rejected_and_not_stored(app):
    original = ai.translate_batch
    ai.translate_batch = lambda texts, source, target: ["No formula here" for _ in texts]
    try:
        with app.app_context():
            out, fallback = translate.translate_texts(["Calcule $2 + 2$."], "fr", "en")
            assert out == ["Calcule $2 + 2$."] and fallback
            assert db.session.query(TranslationCache).count() == 0
    finally:
        ai.translate_batch = original


def test_when_translation_is_unavailable_the_original_text_is_kept(app):
    with app.app_context():
        out, fallback = translate.translate_texts(["Calcule $2 + 2$."], "fr", "en")
        assert out == ["Calcule $2 + 2$."] and fallback and db.session.query(TranslationCache).count() == 0


# ----- The student journey -----

@pytest.fixture
def translated(monkeypatch):
    calls = []

    def fake(texts, source, target):
        calls.append(list(texts))
        return [f"EN {t}" for t in texts]

    monkeypatch.setattr(ai, "translate_batch", fake)
    return calls


@pytest.fixture
def student(logged_in):
    logged_in.post("/settings/curriculum", data={"curriculum": "sn:6e"})
    return logged_in


def test_choosing_a_curriculum_is_saved_and_validated(app, logged_in):
    page = logged_in.post("/settings/curriculum", data={"curriculum": "sn:6e"}, follow_redirects=True).get_data(as_text=True)
    assert "Your curriculum was saved" in page
    with app.app_context():
        user = db.session.query(User).filter_by(email="ama@example.com").one()
        assert (user.country, user.grade) == ("sn", "6e")
    bad = logged_in.post("/settings/curriculum", data={"curriculum": "sn:g7"}, follow_redirects=True).get_data(as_text=True)
    assert "Choose a country and a level from the list." in bad
    with app.app_context():
        assert db.session.query(User).filter_by(email="ama@example.com").one().grade == "6e"
    logged_in.post("/settings/curriculum", data={"curriculum": ""})
    with app.app_context():
        assert db.session.query(User).filter_by(email="ama@example.com").one().country is None


def test_a_level_without_chapters_is_not_presented_as_supported(student):
    student.post("/settings/curriculum", data={"curriculum": "rw:s1"})
    page = student.get("/curriculum/").get_data(as_text=True)
    assert "No chapters here yet" in page and "Les nombres décimaux" not in page


def test_chapter_hub_and_overview_for_a_senegal_sixieme_student(student, translated):
    page = student.get("/curriculum/").get_data(as_text=True)
    assert "Senegal, Sixième" in page and "Not started" in page
    chapter = student.get(f"/curriculum/{CID}").get_data(as_text=True)
    assert "0 of 5 sections done" in chapter and "Sources and licences" in chapter and "interdit" in chapter
    assert "has not been checked against the official" in chapter or "EN Reference chapter" in chapter
    assert "Start chapter" in chapter


def test_language_does_not_change_curriculum_and_french_needs_no_translation(app, student, translated):
    english = student.get(f"/curriculum/{CID}/s/ecritures").get_data(as_text=True)
    assert "EN " in english and "{,}" not in english.split("<main")[1].split("</main>")[0]
    calls_after_english = len(translated)
    french = student.get(f"/curriculum/{CID}/s/ecritures", headers=FRENCH).get_data(as_text=True)
    assert "Des nombres entiers aux nombres décimaux" in french and "Exercices guidés" in french and "{,}" in french
    assert len(translated) == calls_after_english
    again = student.get(f"/curriculum/{CID}/s/ecritures").get_data(as_text=True)
    assert len(translated) == calls_after_english and "EN " in again
    switched = student.get(f"/language/fr?next=/curriculum/{CID}/s/ecritures")
    assert switched.location.endswith(f"/curriculum/{CID}/s/ecritures")
    with app.app_context():
        user = db.session.query(User).filter_by(email="ama@example.com").one()
        assert (user.country, user.grade) == ("sn", "6e")


def test_the_lesson_page_does_not_leak_answers_or_solutions(student):
    page = student.get(f"/curriculum/{CID}/s/soustraction", headers=FRENCH).get_data(as_text=True)
    assert "Calcule" in page and "16{,}73" not in page and "1673 centièmes" not in page and "2,75 m" not in page
    assert page.count("data-exercise=") >= 3


def test_every_section_summary_practice_and_assessment_page_renders_in_both_languages(student, translated):
    paths = [f"/curriculum/{CID}", f"/curriculum/{CID}/practice", f"/curriculum/{CID}/summary", f"/curriculum/{CID}/assessment?seed=abcd1234"]
    paths += [f"/curriculum/{CID}/s/{s.id}" for s in CHAPTER.sections]
    for path in paths:
        for headers in ({}, FRENCH):
            response = student.get(path, headers=headers)
            assert response.status_code == 200, (path, headers)
    assert student.get(f"/curriculum/nope").status_code == 404
    assert student.get(f"/curriculum/{CID}/s/nope").status_code == 404


def check(client, exercise, answer=None, reveal=False):
    body = {"exercise": f"{CID}/{exercise}"}
    body.update({"reveal": True} if reveal else {"answer": answer})
    return client.post("/curriculum/check", json=body)


def test_exercise_checking_accepts_equivalent_answers_and_records_progress(app, student):
    wrong = check(student, "s1-g1", "0,047").get_json()
    assert wrong["status"] == "wrong" and not wrong["solved"] and "solution" not in wrong
    with app.app_context():
        assert not db.session.query(ExerciseResult).filter_by(exercise_id=f"{CID}/s1-g1").one().solved
    for typed in ["0,47", "0.47", " 0,470 ", "$0{,}47$", "0,4700"]:
        reply = check(student, "s1-g1", typed).get_json()
        assert reply["status"] == "correct" and reply["solved"] and reply["solution"], typed
    typed_back = check(student, "s1-g1", "47/100").get_json()
    assert typed_back["status"] == "wrong_form" and "decimal" in typed_back["message"].lower()
    reply = check(student, "s1-g1", "0,047").get_json()
    assert reply["status"] == "wrong" and reply["solved"]
    with app.app_context():
        row = db.session.query(ExerciseResult).filter_by(exercise_id=f"{CID}/s1-g1").one()
        assert row.solved and row.attempts == 7


def test_wrong_answers_get_specific_help_and_form_errors_are_not_counted_as_attempts(app, student):
    reply = check(student, "s5-g2", "4,45").get_json()
    assert reply["status"] == "wrong" and "6 − 2 = 4" in reply["message"] and "solution" not in reply
    assert check(student, "s5-g2", "abc").get_json()["status"] == "unreadable"
    wrong_form = check(student, "s1-g2", "3,125").get_json()
    assert wrong_form["status"] == "wrong_form" and "fraction" in wrong_form["message"]
    assert check(student, "s1-g2", "25/8").get_json()["status"] == "wrong_form"
    choice = check(student, "s1-g3", "1").get_json()
    assert choice["status"] == "wrong" and "0,8 est plus petit que 1" in choice["message"]
    assert check(student, "s1-g3", "2").get_json()["status"] == "correct"
    with app.app_context():
        assert db.session.query(ExerciseResult).filter_by(exercise_id=f"{CID}/s5-g2").one().attempts == 1
        assert db.session.query(ExerciseResult).filter_by(exercise_id=f"{CID}/s1-g2").count() == 1


def test_revealing_the_solution_does_not_count_as_solving(app, student):
    reply = check(student, "s4-g1", reveal=True).get_json()
    assert reply["status"] == "revealed" and len(reply["solution"]) >= 3 and reply["solved"] is False
    with app.app_context():
        row = db.session.query(ExerciseResult).filter_by(exercise_id=f"{CID}/s4-g1").one()
        assert not row.solved and row.attempts == 0


def test_check_endpoint_rejects_unknown_exercises_and_assessment_questions(app, student):
    assert check(student, "nope", "1").status_code == 404
    assert student.post("/curriculum/check", json={"exercise": f"{CID}/a1", "answer": "1"}).status_code == 404
    assert student.post("/curriculum/check", json={}).status_code == 404
    assert app.test_client().post("/curriculum/check", json={"exercise": f"{CID}/p1", "answer": "3,58"}).status_code in (302, 401)


def test_finishing_sections_updates_progress_and_can_be_undone(student):
    response = student.post(f"/curriculum/{CID}/s/ecritures/complete")
    assert response.location.endswith(f"/curriculum/{CID}/s/rang")
    assert "1 of 5 sections done" in student.get(f"/curriculum/{CID}").get_data(as_text=True)
    page = student.get(f"/curriculum/{CID}").get_data(as_text=True)
    assert "Continue" in page
    undone = student.post(f"/curriculum/{CID}/s/ecritures/complete")
    assert undone.location.endswith(f"/curriculum/{CID}/s/ecritures")
    assert "0 of 5 sections done" in student.get(f"/curriculum/{CID}").get_data(as_text=True)
    for section in CHAPTER.sections:
        student.post(f"/curriculum/{CID}/s/{section.id}/complete")
    final = student.get(f"/curriculum/{CID}").get_data(as_text=True)
    assert "5 of 5 sections done" in final and "Review chapter" in final


def answers_for(seed, transform=checker.show):
    """Build the right answers for an assessment seed, in the order of the questions."""
    out = []
    for question in assessment(random.Random(seed)):
        answer = question.answer
        if answer.kind == "choice":
            out.append(str(answer.value))
        elif answer.kind == "numbers":
            out.append(" ; ".join(transform(v) for v in answer.value))
        elif answer.kind == "between":
            out.append(transform((answer.value + answer.high) / 2))
        elif answer.form == "decimal_fraction":
            out.append(f"{int(answer.value * 1000)}/1000")
        else:
            out.append(transform(answer.value))
    return out


def dotted(value):
    """Write a number with a decimal point and an extra trailing zero, to test other ways of writing the same value."""
    text = checker.show(value).replace(",", ".")
    return text + "0" if "." in text else text


def submit(client, seed, answers):
    data = {"seed": seed, **{f"q{i}": value for i, value in enumerate(answers)}}
    return client.post(f"/curriculum/{CID}/assessment", data=data)


def test_assessment_start_redirects_to_a_seeded_set_that_hides_the_answers(student):
    response = student.get(f"/curriculum/{CID}/assessment")
    assert response.status_code == 302 and "seed=" in response.location
    page = student.get(response.location).get_data(as_text=True)
    assert page.count('class="exercise"') == 12 and "Chapter assessment" in page
    assert "Correct answer" not in page and "How to solve it" not in page


def test_a_perfect_assessment_scores_full_marks_even_with_different_notations(app, student):
    seed = "perfect01"
    result = submit(student, seed, answers_for(seed))
    assert result.status_code == 302
    page = student.get(result.location).get_data(as_text=True)
    assert "12<span>/12</span>" in page and "Well done" in page
    with app.app_context():
        attempt = db.session.query(ChapterAttempt).one()
        assert (attempt.correct, attempt.total, attempt.percent) == (12, 12, 100)
        assert all(right == total for right, total in attempt.by_concept.values())
    seed = "perfect02"
    alternative = answers_for(seed, transform=dotted)
    page = student.get(submit(student, seed, alternative).location).get_data(as_text=True)
    assert "12<span>/12</span>" in page


def test_a_weak_assessment_gets_corrections_and_revision_advice(app, student):
    seed = "weak0001"
    right = answers_for(seed)
    wrong = ["" if i % 2 == 0 else "999" for i in range(12)]
    wrong[6] = right[6]
    page = student.get(submit(student, seed, wrong).location).get_data(as_text=True)
    assert "Review these first" in page and "Correct answer" in page and "How to solve it" in page
    assert "You did not answer this question." in page and f"/curriculum/{CID}/s/" in page
    chapter = student.get(f"/curriculum/{CID}").get_data(as_text=True)
    assert "Worth revising" in chapter and "Best score: 8%" in chapter and "1 try" in chapter
    with app.app_context():
        attempt = db.session.query(ChapterAttempt).one()
        assert attempt.correct == 1 and attempt.percent == 8


def test_retaking_gives_new_questions_and_keeps_every_attempt(app, student):
    first = student.get(student.get(f"/curriculum/{CID}/assessment").location).get_data(as_text=True)
    second = student.get(student.get(f"/curriculum/{CID}/assessment").location).get_data(as_text=True)
    assert first != second
    submit(student, "retake001", ["1"] * 12)
    submit(student, "retake002", ["2"] * 12)
    with app.app_context():
        assert db.session.query(ChapterAttempt).count() == 2


def test_invalid_assessment_data_is_rejected_safely(student):
    assert student.post(f"/curriculum/{CID}/assessment", data={"seed": "../etc"}).status_code == 400
    assert student.post(f"/curriculum/{CID}/assessment", data={}).status_code == 400
    page = student.get(submit(student, "short001", []).location).get_data(as_text=True)
    assert "0<span>/12</span>" in page
    page = student.get(submit(student, "junk0001", ["<script>x</script>"] * 10).location).get_data(as_text=True)
    assert "<script>x</script>" not in page


def test_nobody_can_open_someone_elses_assessment_result(app, student, make_user):
    attempt_url = submit(student, "private01", ["1"] * 12).location
    make_user("kofi@example.com", "secret123", "Kofi")
    other = app.test_client()
    other.post("/login", data={"email": "kofi@example.com", "password": "secret123"})
    assert other.get(attempt_url).status_code == 404
    assert student.get(attempt_url).status_code == 200


def test_the_lesson_tutor_gets_the_lesson_and_the_students_level(app, student, monkeypatch):
    seen = []

    def tutor(lesson, profile, history, question):
        seen.append((lesson, profile, list(history), question))
        return "Look at the **dixièmes** first."

    monkeypatch.setattr(ai, "ask_lesson_tutor", tutor)
    reply = student.post(f"/curriculum/{CID}/s/rang/ask", json={"question": "Why is the 7 worth 0,7?"})
    assert reply.status_code == 200 and "dixièmes" in reply.get_json()["html"]
    lesson, profile, history, question = seen[0]
    assert "Partie entière, partie décimale et rang des chiffres" in lesson and "Senegal" in profile and "Sixième" in profile and "official syllabus" in profile
    assert history == [] and question == "Why is the 7 worth 0,7?"
    student.post(f"/curriculum/{CID}/s/rang/ask", json={"question": "And the 6?"})
    assert seen[1][2] == [("user", "Why is the 7 worth 0,7?"), ("assistant", "Look at the **dixièmes** first.")]
    page = student.get(f"/curriculum/{CID}/s/rang").get_data(as_text=True)
    assert "Why is the 7 worth 0,7?" in page and "And the 6?" in page
    with app.app_context():
        assert db.session.query(TutorQuestion).count() == 2


def test_the_lesson_tutor_validates_questions_limits_use_and_survives_ai_failure(app, student, monkeypatch):
    url = f"/curriculum/{CID}/s/rang/ask"
    assert student.post(url, json={"question": "   "}).status_code == 400
    assert student.post(url, json={"question": "x" * 1001}).status_code == 400

    def broken(*args, **kwargs):
        raise ai.AIError("The AI service is very busy right now. Please try again in a moment.")

    monkeypatch.setattr(ai, "ask_lesson_tutor", broken)
    failed = student.post(url, json={"question": "Help"})
    assert failed.status_code == 503 and "busy" in failed.get_json()["error"]
    with app.app_context():
        assert db.session.query(TutorQuestion).count() == 0
    monkeypatch.setattr(ai, "ask_lesson_tutor", lambda *a, **k: "ok")
    app.config["QUESTIONS_PER_HOUR"] = 1
    assert student.post(url, json={"question": "One"}).status_code == 200
    assert student.post(url, json={"question": "Two"}).status_code == 429


def test_the_problem_solver_uses_the_students_curriculum_but_only_when_chosen(app, logged_in, monkeypatch):
    seen = []

    def solve(text, profile=""):
        seen.append(profile)
        from tests.conftest import fake_result
        return fake_result()

    monkeypatch.setattr(ai, "solve_text", solve)
    logged_in.post("/solve", data={"mode": "type", "problem": "Solve 2x + 3 = 11"})
    assert seen[-1] == ""
    logged_in.post("/settings/curriculum", data={"curriculum": "sn:6e"})
    logged_in.post("/solve", data={"mode": "type", "problem": "Solve 2x + 3 = 11"})
    assert "Senegal curriculum" in seen[-1] and "Sixième" in seen[-1] and "beyond this level" in seen[-1]
    logged_in.post("/settings/curriculum", data={"curriculum": "sn:tle"})
    logged_in.post("/solve", data={"mode": "type", "problem": "Solve 2x + 3 = 11"})
    assert "calculus" in seen[-1] and "Terminale" in seen[-1]


def test_the_profile_lists_finished_lessons(app, student, monkeypatch):
    student.post(f"/curriculum/{CID}/s/ecritures/complete")
    from mathhelper.curriculum.context import profile
    with app.test_request_context():
        from flask_login import login_user
        user = db.session.query(User).filter_by(email="ama@example.com").one()
        assert "Des nombres entiers aux nombres décimaux" in profile(user)


def test_admin_cannot_use_student_curriculum_pages_or_settings(admin):
    assert admin.get("/curriculum/").status_code == 302
    admin.post("/settings/curriculum", data={"curriculum": "sn:6e"})
    assert 'id="curriculum"' not in admin.get("/settings/").get_data(as_text=True)


def test_deleting_an_account_removes_curriculum_records(app, student):
    check(student, "p1", "3,58")
    submit(student, "delete001", ["1"] * 12)
    student.post(f"/curriculum/{CID}/s/rang/ask", json={"question": "Hi"})
    with app.app_context():
        assert db.session.query(ExerciseResult).count() == db.session.query(ChapterAttempt).count() == db.session.query(TutorQuestion).count() == 1
    student.post("/settings/delete-account", data={"password": "secret123"})
    with app.app_context():
        assert db.session.query(ExerciseResult).count() == db.session.query(ChapterAttempt).count() == db.session.query(TutorQuestion).count() == 0


# ----- Problems found by the independent reviews -----

import time


def test_hostile_answers_get_clean_replies_and_never_a_server_error_or_a_slow_request(student):
    nasty = ["9" * 5000, "0," + "1" * 5000, "1." * 5000, "٠" * 5000, "\\frac{" * 8000 + "1" + "}{1}" * 8000, "1/" + "0" * 400, "1e5", "nan", "inf",
             "１２", "\n\n", "3,5\x00", "x" * 100000, "²", "-", "/", "()", "((((((((((1))))))))))"]
    started = time.monotonic()
    for text in nasty:
        for exercise in ("s1-g1", "s1-g3", "s3-g2", "s3-g3"):
            reply = student.post("/curriculum/check", json={"exercise": f"{CID}/{exercise}", "answer": text})
            assert reply.status_code == 200, (exercise, text[:30])
    assert time.monotonic() - started < 10


def test_wrongly_typed_json_is_refused_cleanly(student):
    for body in [5, "text", [1], None, {"exercise": 5}, {"exercise": [1]}, {"exercise": None}, {"exercise": True},
                 {"exercise": f"{CID}/p1", "answer": 123}, {"exercise": f"{CID}/p1", "answer": [1]}, {"exercise": f"{CID}/p1", "answer": {"a": 1}},
                 {"exercise": f"{CID}/p1", "answer": True}, {"exercise": f"{CID}/p1", "answer": 0.47}, {"exercise": f"{CID}/p1", "reveal": "yes"}]:
        assert student.post("/curriculum/check", json=body).status_code in (200, 404), body
    for body in [5, "text", [1], {"question": 5}, {"question": [1]}, {"question": None}]:
        assert student.post(f"/curriculum/{CID}/s/rang/ask", json=body).status_code in (400, 200), body
    assert student.post(f"/curriculum/{CID}/s/rang/ask", json={"question": 5}).status_code == 400


def test_a_digit_like_symbol_in_a_choice_answer_cannot_break_the_result_page(student):
    answers = ["1"] * 12
    answers[4] = "²"
    answers[11] = "٣"
    seed = "unicode01"
    location = submit(student, seed, answers).location
    page = student.get(location)
    assert page.status_code == 200
    assert student.get(location).status_code == 200


def test_a_tutor_reply_that_imitates_the_internal_math_placeholder_does_not_break_the_page(app, student, monkeypatch):
    monkeypatch.setattr(ai, "ask_lesson_tutor", lambda *a, **k: "See MATHSLOT9END and MATHSLOT0END and $x$.")
    assert student.post(f"/curriculum/{CID}/s/rang/ask", json={"question": "Echo MATHSLOT99END"}).status_code == 200
    assert student.get(f"/curriculum/{CID}/s/rang").status_code == 200


def test_what_the_student_typed_is_never_sent_to_the_translator_or_stored(app, student, translated):
    secret = "ma reponse secrete personnelle"
    answers = [secret] * 12
    location = submit(student, "private02", answers).location
    page = student.get(location).get_data(as_text=True)
    assert secret in page
    assert not any(secret in text for call in translated for text in call)
    with app.app_context():
        assert db.session.query(TranslationCache).filter(TranslationCache.source.contains(secret)).count() == 0


def test_an_attempt_from_an_older_question_generator_keeps_its_score_but_hides_mismatched_corrections(app, student):
    location = submit(student, "oldgen001", ["1"] * 12).location
    with app.app_context():
        attempt = db.session.query(ChapterAttempt).one()
        attempt.version = 0
        db.session.commit()
    page = student.get(location)
    assert page.status_code == 200
    text = page.get_data(as_text=True)
    assert "no longer available" in text and "How to solve it" not in text


def test_the_old_database_without_the_version_column_is_upgraded(app):
    from sqlalchemy import inspect, text
    from mathhelper import schema
    with app.app_context():
        with db.engine.begin() as connection:
            connection.execute(text("DROP TABLE chapter_attempt"))
            connection.execute(text("CREATE TABLE chapter_attempt (id INTEGER PRIMARY KEY, user_id INTEGER, chapter_id VARCHAR(60), seed VARCHAR(32), answers JSON, correct INTEGER, total INTEGER, by_concept JSON, created_at DATETIME)"))
        schema.upgrade()
        assert "version" in {column["name"] for column in inspect(db.engine).get_columns("chapter_attempt")}


def test_the_solution_page_tutor_also_gets_the_students_level(app, student, monkeypatch):
    seen = []
    monkeypatch.setattr(ai, "ask_tutor", lambda problems, history, question, profile="": seen.append(profile) or "ok")
    student.post("/solve", data={"mode": "type", "problem": "Solve 2x + 3 = 11"})
    student.post("/solutions/1/ask", json={"question": "why?"})
    assert seen and "Senegal" in seen[0] and "Sixième" in seen[0]


def test_only_a_good_enough_score_counts_as_passing(student):
    perfect = student.get(submit(student, "pass00001", answers_for("pass00001")).location).get_data(as_text=True)
    assert "Well done" in perfect
    failed = student.get(submit(student, "pass00002", [""] * 12).location).get_data(as_text=True)
    assert "Well done" not in failed and "Good effort" in failed


# ----- Round 2 findings -----

def test_a_required_decimal_fraction_needs_a_whole_number_on_top():
    answer = checker.Answer("number", Fraction(3125, 1000), form="decimal_fraction")
    for typed in ["312,5/100", "3125,0/1000", "31,25/10", "3125/1000", "(3125)/(1000)", "3125 / 1000"]:
        expected = "correct" if "," not in typed else "wrong_form"
        assert checker.check(answer, typed).status == expected, typed


@pytest.mark.parametrize("typed", ["1.5.", "1..5", "2.5.0", "1.53.287", ".5.", "1.2.3"])
def test_misplaced_points_are_not_read_as_thousands_separators(typed):
    assert checker.parse_number(typed) is None


def test_points_as_thousands_separators_still_work():
    assert checker.parse_number("1.353.287") == 1353287 and checker.parse_number("-12.000") == -12000 or checker.parse_number("-12.000") == Fraction(-12)


def test_the_show_solution_button_does_not_collide_with_the_password_eye(student):
    page = student.get(f"/curriculum/{CID}/s/rang").get_data(as_text=True)
    assert "data-show-solution" in page and "data-reveal" not in page


def test_the_older_solution_tutor_also_refuses_wrongly_typed_json(logged_in):
    logged_in.post("/solve", data={"mode": "type", "problem": "Solve 2x + 3 = 11"})
    for body in [5, "text", [1], {"question": 5}, {"question": [1]}, {"question": None}, {"question": True}]:
        assert logged_in.post("/solutions/1/ask", json=body).status_code in (200, 400), body


def test_assessment_seeds_must_be_plain_ascii(student):
    for seed in ["²²²²²", "éééééé", "ab", "a" * 17, "ab cd", ""]:
        assert student.post(f"/curriculum/{CID}/assessment", data={"seed": seed}).status_code == 400, seed
        assert student.get(f"/curriculum/{CID}/assessment?seed={seed}").status_code == 302


def test_students_never_see_each_others_progress_exercises_or_tutor_history(app, student, make_user):
    check(student, "p1", "3,58")
    student.post(f"/curriculum/{CID}/s/rang/complete")
    student.post(f"/curriculum/{CID}/s/rang/ask", json={"question": "my private question"})
    make_user("kofi@example.com", "secret123", "Kofi")
    other = app.test_client()
    other.post("/login", data={"email": "kofi@example.com", "password": "secret123"})
    practice = other.get(f"/curriculum/{CID}/practice").get_data(as_text=True)
    assert "is-solved" not in practice
    section = other.get(f"/curriculum/{CID}/s/rang").get_data(as_text=True)
    assert "my private question" not in section and "Completed" not in section
    chapter = other.get(f"/curriculum/{CID}").get_data(as_text=True)
    assert "0 of 5 sections done" in chapter and "0 of 34 exercises solved" in chapter
    assert other.post("/curriculum/check", json={"exercise": f"{CID}/p1", "answer": "3,58"}).get_json()["solved"] is True
    with app.app_context():
        assert db.session.query(ExerciseResult).filter_by(exercise_id=f"{CID}/p1").count() == 2


def test_the_fifth_assessment_question_does_not_always_reward_the_longest_number():
    longest_wins = 0
    for seed in range(200):
        q = {q.id.split("/")[1]: q for q in assessment(random.Random(f"m{seed}"))}["a5"]
        shown = [decimal(re.search(NUMBER, o).group(1)) for o in q.options]
        digits = [len(str(o).split("{,}")[1].rstrip("$")) for o in q.options]
        longest_wins += digits.index(max(digits)) == q.answer.value
    assert longest_wins == 0


# ----- Translation review screen, shared sentences and the warm-up command -----

def fake_translator(sent):
    def fake(texts, source, target):
        sent.append(list(texts))
        return [f"EN {t}" for t in texts]
    return fake


def test_the_same_sentence_with_other_numbers_reuses_one_stored_translation(app, monkeypatch):
    sent = []
    monkeypatch.setattr(ai, "translate_batch", fake_translator(sent))
    with app.app_context():
        out, _ = translate.translate_texts(["Calcule $2{,}5 + 1$.", "Calcule $7{,}25 + 9$."], "fr", "en")
        assert out == ["EN Calcule $2.5 + 1$.", "EN Calcule $7.25 + 9$."]
        assert sent == [["Calcule ⟦1⟧."]] and db.session.query(TranslationCache).count() == 1
        out, _ = translate.translate_texts(["Calcule $100 - 0{,}01$."], "fr", "en")
        assert out == ["EN Calcule $100 - 0.01$."] and len(sent) == 1


@pytest.fixture
def stored_translation(app, monkeypatch):
    monkeypatch.setattr(ai, "translate_batch", lambda texts, s, t: [f"First, {x}, then" for x in texts])
    with app.app_context():
        translate.translate_texts(["Compare $2{,}5$ et $2{,}35$."], "fr", "en")
        return db.session.query(TranslationCache).one().id


def test_admin_sees_stored_translations_and_can_correct_them(app, admin, stored_translation):
    page = admin.get("/admin/translations").get_data(as_text=True)
    assert "Compare" in page and "To check" in page and "2.5" in page
    saved = admin.post(f"/admin/translations/{stored_translation}/save", data={"text": "Compare $2.35$ with $2.5$, please."}, follow_redirects=True)
    assert "Translation saved" in saved.get_data(as_text=True)
    with app.app_context():
        row = db.session.get(TranslationCache, stored_translation)
        assert row.reviewed and row.text == "Compare ⟦2⟧ with ⟦1⟧, please."
        assert translate.translate_texts(["Compare $2{,}5$ et $2{,}35$."], "fr", "en")[0] == ["Compare $2.35$ with $2.5$, please."]
        assert translate.translate_texts(["Compare $9{,}5$ et $9{,}35$."], "fr", "en")[0] == ["Compare $9.35$ with $9.5$, please."]


def test_a_correction_that_changes_a_formula_is_refused(app, admin, stored_translation):
    for bad in ["Compare $2.5$ with $2.36$.", "Compare $2.5$ only.", "Compare 2.5 with 2.35", "Compare $2.5$ with $2.35$ and $1$."]:
        reply = admin.post(f"/admin/translations/{stored_translation}/save", data={"text": bad}, follow_redirects=True).get_data(as_text=True)
        assert "must keep every formula" in reply, bad
    assert admin.post(f"/admin/translations/{stored_translation}/save", data={"text": "  "}, follow_redirects=True).get_data(as_text=True).count("Write the corrected") == 1
    with app.app_context():
        assert not db.session.get(TranslationCache, stored_translation).reviewed


def test_admin_can_mark_a_translation_as_checked_or_delete_it(app, admin, stored_translation):
    admin.post(f"/admin/translations/{stored_translation}/review")
    with app.app_context():
        assert db.session.get(TranslationCache, stored_translation).reviewed
    assert "Compare" not in admin.get("/admin/translations").get_data(as_text=True)
    assert "Compare" in admin.get("/admin/translations?status=reviewed").get_data(as_text=True)
    admin.post(f"/admin/translations/{stored_translation}/delete")
    with app.app_context():
        assert db.session.query(TranslationCache).count() == 0
    assert admin.post("/admin/translations/9999/save", data={"text": "x"}).status_code == 404


def test_only_the_admin_can_use_the_translation_screen(app, student, stored_translation):
    assert student.get("/admin/translations").status_code == 403
    assert student.post(f"/admin/translations/{stored_translation}/save", data={"text": "hacked"}).status_code == 403
    assert student.post(f"/admin/translations/{stored_translation}/delete").status_code == 403
    with app.app_context():
        assert db.session.query(TranslationCache).count() == 1


def test_the_admin_screen_escapes_html_in_stored_translations(app, admin):
    with app.app_context():
        db.session.add(TranslationCache(digest="x" * 64, lang="en", source="Texte", text="<script>alert(1)</script> <img src=x onerror=alert(2)>"))
        db.session.commit()
    page = admin.get("/admin/translations").get_data(as_text=True)
    assert "<script>alert(1)" not in page and "<img src=x" not in page


def test_the_warm_up_command_translates_the_whole_chapter_once(app, monkeypatch):
    sent = []
    monkeypatch.setattr(ai, "translate_batch", fake_translator(sent))
    runner = app.test_cli_runner()
    first = runner.invoke(args=["warm-translations"])
    assert first.exit_code == 0 and "All text is translated" in first.output
    with app.app_context():
        stored = db.session.query(TranslationCache).count()
    assert stored > 100 and sent
    calls = len(sent)
    again = runner.invoke(args=["warm-translations"])
    assert again.exit_code == 0 and len(sent) - calls <= 2


def test_the_warm_up_command_reports_failures(app):
    result = app.test_cli_runner().invoke(args=["warm-translations"])
    assert result.exit_code == 1 and "run the command again" in result.output


def test_plain_numbers_in_a_sentence_are_set_aside_like_formulas(app):
    masked, spans = translate.protect("Il a tort : 8,5 = 8,50 et 50 est plus grand que 49, voir $2{,}5$.")
    assert masked == "Il a tort : ⟦1⟧ = ⟦2⟧ et ⟦3⟧ est plus grand que ⟦4⟧, voir ⟦5⟧." and spans[0] == "8,5"
    assert translate.restore("He is wrong: ⟦1⟧ = ⟦2⟧ and ⟦3⟧ is bigger than ⟦4⟧, see ⟦5⟧.", spans, "fr", "en") == \
        "He is wrong: 8.5 = 8.50 and 50 is bigger than 49, see $2.5$."
    assert translate.restore("Elle: ⟦1⟧ ⟦2⟧ ⟦3⟧ ⟦4⟧ ⟦5⟧", ["2.5", "$2.5$", "3", "4", "1.000"], "en", "fr") == "Elle: 2,5 $2{,}5$ 3 4 1,000"


def test_french_spacing_before_punctuation_is_dropped_in_english():
    assert translate.convert_plain("Decimal parts : 48 et ? Yes !", "fr", "en") == "Decimal parts: 48 et? Yes!"
    assert translate.convert_plain("Parties : 3.5", "en", "fr") == "Parties : 3,5"
