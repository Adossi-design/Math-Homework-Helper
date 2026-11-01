"""Cinquième chapter 3 (fractions), recomputed independently."""
import random
import re
from fractions import Fraction as F

import pytest

from mathhelper.curriculum.chapters.sn_5e_fractions import CHAPTER as FRA, assessment

BY_ID = {e.id.split("/")[1]: e for e in FRA.exercises().values()}


def fractions_in(prompt):
    """Read every a/b written as \\dfrac{a}{b} in a prompt, as exact fractions."""
    return [F(int(a), int(b)) for a, b in re.findall(r"\\dfrac\{(\d+)\}\{(\d+)\}", prompt)]


def test_fixed_answers_match_an_independent_recalculation():
    plain = {"s1-g1": F(7, 8) - F(3, 8), "s1-g2": F(3, 4) - F(1, 6), "s1-g3": 2 - F(3, 7), "s1-g4": 1 - F(2, 5) - F(1, 4),
             "s2-g1": 4 * F(3, 5), "s2-g2": F(2, 3) * F(5, 7), "s2-g3": F(3, 8) * F(4, 9), "s2-g4": F(3, 4) * F(2, 5),
             "s3-g1": F(3, 4) ** 2, "s3-g2": F(1, 3) ** 3, "s3-g3": F(2, 5) ** 2 * 5, "s3-g4": F(1, 2) ** 5,
             "s4-g3": F(3, 8),
             "p1": F(9, 10) - F(4, 10), "p2": F(11, 12) - F(5, 12), "p3": F(3, 4) - F(1, 3), "p4": F(7, 10) - F(1, 5), "p5": 5 - F(3, 4), "p6": F(13, 6) - F(5, 4),
             "p7": F(7, 8) - F(1, 4), "p8": 1 - F(1, 3) - F(1, 5),
             "p9": 5 * F(2, 7), "p10": 6 * F(3, 4), "p11": F(3, 5) * F(2, 7), "p12": F(5, 6) * F(3, 10), "p13": F(7, 12) * F(4, 21), "p14": F(3, 5) * 200, "p15": F(2, 3) * F(3, 4),
             "p16": (48 - F(3, 8) * 48) * (1 - F(1, 3)),
             "p18": F(1, 4) ** 2, "p19": F(5, 2) ** 2, "p20": F(2, 3) ** 3, "p21": F(3, 2) ** 4, "p22": 1 - F(1, 3) ** 2, "p23": F(1, 2) ** 2 + F(1, 4) ** 2, "p24": F(1, 2) ** 3,
             "p29": F(7, 20), "p30": F(9, 8)}
    for key, value in plain.items():
        assert BY_ID[key].answer.value == F(value), (key, BY_ID[key].answer.value, value)
    lists = {"s4-g1": [F(16, 10), F(17, 10)], "s4-g2": [F(66, 100), F(67, 100)], "p26": [F(13, 10), F(14, 10)], "p27": [F(83, 100), F(84, 100)], "p28": [F(14, 10), F(15, 10)]}
    for key, value in lists.items():
        assert list(BY_ID[key].answer.value) == value, key
    assert F(16, 10) < F(5, 3) < F(17, 10) and F(66, 100) < F(2, 3) < F(67, 100) and F(13, 10) < F(4, 3) < F(14, 10)
    assert F(83, 100) < F(5, 6) < F(84, 100) and F(14, 10) < F(10, 7) < F(15, 10) and F(1, 1) < F(7, 6) < 2 and 4 < F(23, 5) < 5
    assert F(5, 7) < F(3, 4) and F(3, 7) < F(4, 9)
    choices = {"s1-g5": 1, "s2-g5": 1, "s3-g5": 0, "s4-g4": 1, "s4-g5": 0, "p17": 0, "p25": 0, "p31": 1, "p32": 0}
    for key, index in choices.items():
        assert BY_ID[key].answer.value == index, key
    assert set(plain) | set(lists) | set(choices) == set(BY_ID)


def test_chapter_shape_and_alignment():
    assert FRA.number == 3 and FRA.level == "5e" and len(FRA.sections) == 4 and FRA.also_for == ("ci",)
    assert "lesson 3 of the C" in FRA.status_note and "not been checked against the official Senegalese" in FRA.status_note
    assert all(e.answer.form in ("irreducible", "decimal") for e in FRA.exercises().values() if e.answer.kind == "number")


def test_assessment_keys_match_a_recalculation_from_each_prompt():
    for seed in range(300):
        q = {x.id.split("/")[1]: x for x in assessment(random.Random(f"f5{seed}"))}
        assert sorted(q, key=lambda k: int(k[1:])) == [f"a{i}" for i in range(1, 13)]
        a, b = fractions_in(q["a1"].prompt)[:2]
        assert q["a1"].answer.value == a - b > 0
        a, b = fractions_in(q["a2"].prompt)[:2]
        assert q["a2"].answer.value == a - b > 0
        n = int(re.search(r"\$(\d+) -", q["a3"].prompt).group(1))
        assert q["a3"].answer.value == n - fractions_in(q["a3"].prompt)[0] and 0 < fractions_in(q["a3"].prompt)[0] < 1
        a, b = fractions_in(q["a4"].prompt)[:2]
        assert q["a4"].answer.value == 1 - a - b > 0
        n = int(re.search(r"\$(\d+) \\times", q["a5"].prompt).group(1))
        assert q["a5"].answer.value == n * fractions_in(q["a5"].prompt)[0]
        a, b = fractions_in(q["a6"].prompt)[:2]
        assert q["a6"].answer.value == a * b
        f = fractions_in(q["a7"].prompt)[0]
        quantity = int(re.search(r"de (\d+) kg", q["a7"].prompt).group(1))
        assert q["a7"].answer.value == f * quantity and (f * quantity).denominator == 1
        num, den, k = [int(x) for x in re.search(r"\\dfrac\{(\d+)\}\{(\d+)\}\\right\)\^(\d)", q["a8"].prompt).groups()]
        assert q["a8"].answer.value == F(num, den) ** k
        n = int(re.search(r"\$(\d+) \+", q["a9"].prompt).group(1))
        assert q["a9"].answer.value == n + fractions_in(q["a9"].prompt)[0] ** 2
        num, den = [int(x) for x in re.search(r"\\dfrac\{(\d+)\}\{(\d+)\}", q["a10"].prompt).groups()]
        low, high = q["a10"].answer.value
        assert high - low == F(1, 10) and low < F(num, den) < high and (low * 10).denominator == 1
        num, den = [int(x) for x in re.search(r"\\dfrac\{(\d+)\}\{(\d+)\}", q["a11"].prompt).groups()]
        low, high = q["a11"].answer.value
        assert high - low == F(1, 100) and low < F(num, den) < high and (low * 100).denominator == 1
        f, g = fractions_in(q["a12"].prompt)[:2]
        assert q["a12"].answer.value == (0 if f > g else 1) and f != g


@pytest.fixture
def student(app, make_user):
    make_user("faye@example.com", "secret123", "Faye")
    client = app.test_client()
    client.post("/login", data={"email": "faye@example.com", "password": "secret123"})
    client.post("/settings/curriculum", data={"curriculum": "sn:5e"})
    return client


def test_pages_render_and_irreducible_form_is_required(student):
    for path in ["", "/practice", "/summary", "/assessment?seed=abcd1234", "/s/difference", "/s/produit", "/s/puissance", "/s/encadrement"]:
        for headers in ({}, {"Accept-Language": "fr-FR,fr;q=0.9"}):
            assert student.get(f"/curriculum/{FRA.id}{path}", headers=headers).status_code == 200, path
    post = lambda typed: student.post("/curriculum/check", json={"exercise": f"{FRA.id}/s1-g1", "answer": typed}).get_json()["status"]
    assert post("1/2") == "correct"
    assert post("4/8") == "wrong_form"
    assert post("0,5") != "correct"
