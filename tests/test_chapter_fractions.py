"""Chapter 6 (fractions), recalculated independently, and the irreducible answer form."""
import math
import random
import re
from fractions import Fraction as F

import pytest

from mathhelper.curriculum import checker
from mathhelper.curriculum.chapters.sn_6e_fractions import CHAPTER as FRAC, assessment

INDEPENDENT = {
    "s1-g1": F(5, 12), "s1-g2": 2, "s1-g3": F(1375, 1000), "s1-g4": F(35, 100), "s1-g5": F(10, 6),
    "s2-g1": F(6, 8) / 2 * 2 / 2 * 2 / 2 if False else F(3, 4), "s2-g2": 2 * 3, "s2-g3": F(18 // 9, 45 // 9), "s2-g4": 0, "s2-g5": 3 * 2,
    "s3-g1": 0, "s3-g2": F(5 + 3, 11), "s3-g3": F(5, 6) - F(2, 6), "s3-g4": F(2, 4) + F(1, 4), "s3-g5": 1 - (F(2, 6) + F(1, 6)),
    "s4-g1": 80 // 4, "s4-g2": 150 // 5 * 3, "s4-g3": 45 // 3 * 2, "s4-g4": F(18 // 6, 24 // 6), "s4-g5": 400 // 8 * 3,
    "p1": F(8 - 3, 8), "p2": F(9, 4), "p3": F(7, 10), "p4": 1, "p5": F(8, 5), "p6": F(3, 8), "p7": 1, "p8": F(10 // 5, 15 // 5), "p9": F(24 // 12, 36 // 12),
    "p10": 4 * 5, "p11": F(35 // 5, 60 // 5), "p12": 6 * 4, "p13": 1, "p14": 5 * 5, "p15": F(84 // 42, 126 // 42),
    "p16": 2, "p18": F(6, 9), "p19": F(4, 10), "p20": F(4, 6) + F(1, 6), "p21": F(6, 8) - F(1, 8), "p22": F(4, 12) + F(3, 12), "p23": F(5, 6) - F(3, 6), "p24": 0,
    "p25": F(1, 4) + F(2, 4), "p26": 120 // 4 * 3, "p27": 350 // 5 * 2, "p28": 60 // 6 * 5, "p29": F(15 // 3, 36 // 3), "p30": 80 // 8 * 3,
    "p31": 600 - 600 // 5 * 2 - 600 // 3, "p32": 2000 - 2000 // 5 * 3 - (2000 - 2000 // 5 * 3) // 2,
}


def test_the_chapter_answers_match_an_independent_recalculation():
    by_id = {e.id.split("/")[1]: e for e in FRAC.exercises().values()}
    assert set(by_id) - {"p17"} == set(INDEPENDENT), set(by_id) ^ set(INDEPENDENT)
    for key, value in INDEPENDENT.items():
        assert by_id[key].answer.value == F(value), (key, by_id[key].answer.value, value)
    assert list(by_id["p17"].answer.value) == sorted([F(1, 2), F(3, 8), F(5, 8), F(1, 4)])


def test_the_irreducible_form_accepts_only_fully_simplified_answers():
    answer = checker.Answer("number", F(3, 4), form="irreducible")
    for typed, status in [("3/4", "correct"), (" 3 / 4 ", "correct"), ("\\frac{3}{4}", "correct"), ("6/8", "wrong_form"), ("0,75", "wrong_form"), ("0.75", "wrong_form"),
                          ("9/12", "wrong_form"), ("3/5", "wrong"), ("1,5/2", "wrong_form"), ("3/4/1", "unreadable")]:
        assert checker.check(answer, typed).status == status, typed
    whole = checker.Answer("number", F(2), form="irreducible")
    for typed, status in [("2", "correct"), ("4/2", "wrong_form"), ("2/1", "wrong_form"), ("2,0", "wrong_form"), ("3", "wrong")]:
        assert checker.check(whole, typed).status == status, typed


def test_a_simplification_exercise_cannot_be_passed_by_retyping_the_question():
    by_id = {e.id.split("/")[1]: e for e in FRAC.exercises().values()}
    for key, typed in [("s2-g1", "6/8"), ("s2-g3", "18/45"), ("p8", "10/15"), ("p11", "35/60"), ("p18", "6/9"), ("s3-g3", "3/6")]:
        assert checker.check(by_id[key].answer, typed).status == "wrong_form", key
    for q in assessment(random.Random("simplify")):
        if q.id.endswith("/a3"):
            assert q.answer.form == "irreducible"


def test_chapter_shape_and_alignment_claims():
    assert FRAC.number == 6 and len(FRAC.sections) == 4 and FRAC.also_for == ("ci",)
    assert "lesson 11 of the Côte d'Ivoire" in FRAC.status_note and "not been checked against the official Senegalese" in FRAC.status_note


def fractions_in(text):
    """Read every fraction written as \\dfrac{a}{b} in a prompt."""
    return [F(int(a), int(b)) for a, b in re.findall(r"dfrac\{(\d+)\}\{(\d+)\}", text)]


def test_assessment_keys_match_a_recalculation_from_each_prompt():
    for seed in range(400):
        q = {x.id.split("/")[1]: x for x in assessment(random.Random(f"fr{seed}"))}
        assert sorted(q, key=lambda k: int(k[1:])) == [f"a{i}" for i in range(1, 13)]
        total, part = [int(x) for x in re.search(r"coupé en (\d+) parts égales\. On en mange (\d+)", q["a1"].prompt).groups()]
        assert q["a1"].answer.value == F(part, total)
        assert q["a2"].answer.value == fractions_in(q["a2"].prompt)[0] and q["a2"].answer.form == "decimal"
        unreduced = re.search(r"dfrac\{(\d+)\}\{(\d+)\}", q["a3"].prompt)
        top, bottom = int(unreduced.group(1)), int(unreduced.group(2))
        assert q["a3"].answer.value == F(top, bottom) and math.gcd(top, bottom) > 1
        first, second = re.findall(r"dfrac\{(\d+)\}\{(\d+)\}", q["a4"].prompt)[0], re.search(r"\?\}\{(\d+)\}", q["a4"].prompt).group(1)
        a, b, new_b = int(first[0]), int(first[1]), int(second)
        assert new_b % b == 0 and q["a4"].answer.value * b == a * new_b
        left, right = fractions_in(q["a5"].prompt)[:2]
        assert left != right and q["a5"].answer.value == (0 if left < right else 1)
        for key in ("a6", "a7", "a8"):
            first_fraction, second_fraction = fractions_in(q[key].prompt)[:2]
            plus = " + " in q[key].prompt
            expected = first_fraction + second_fraction if plus else first_fraction - second_fraction
            assert q[key].answer.value == expected and expected > 0, (key, q[key].prompt)
            assert q[key].answer.form == "irreducible"
        fraction, quantity = fractions_in(q["a9"].prompt)[0], int(re.search(r"de (\d+)\.$", q["a9"].prompt).group(1))
        assert q["a9"].answer.value == fraction * quantity and (fraction * quantity).denominator == 1
        total, absent = [int(x) for x in re.search(r"classe de (\d+) élèves, (\d+) sont absents", q["a10"].prompt).groups()]
        assert q["a10"].answer.value == F(absent, total) and math.gcd(absent, total) > 1
        eaten_one, eaten_two = fractions_in(q["a11"].prompt)[:2]
        assert q["a11"].answer.value == 1 - eaten_one - eaten_two and 0 < q["a11"].answer.value < 1
        assert q["a12"].options[q["a12"].answer.value].startswith("Elle a additionné les numérateurs")


@pytest.fixture
def ci_student(app, make_user):
    make_user("kone@example.com", "secret123", "Kone")
    client = app.test_client()
    client.post("/login", data={"email": "kone@example.com", "password": "secret123"})
    client.post("/settings/curriculum", data={"curriculum": "ci:6e"})
    return client


def test_the_chapter_is_offered_in_both_countries_and_all_pages_render(ci_student):
    hub = ci_student.get("/curriculum/").get_data(as_text=True)
    assert hub.count("chapter-card") == 11
    for path in ["", "/practice", "/summary", "/assessment?seed=abcd1234", "/s/sens", "/s/egales", "/s/operations", "/s/quantite"]:
        for headers in ({}, {"Accept-Language": "fr-FR,fr;q=0.9"}):
            assert ci_student.get(f"/curriculum/{FRAC.id}{path}", headers=headers).status_code == 200, path
    reply = ci_student.post("/curriculum/check", json={"exercise": f"{FRAC.id}/s2-g1", "answer": "6/8"}).get_json()
    assert reply["status"] == "wrong_form" and "Simplify as far as possible" in reply["message"]
    assert ci_student.post("/curriculum/check", json={"exercise": f"{FRAC.id}/s2-g1", "answer": "3/4"}).get_json()["status"] == "correct"
