"""Cinquième chapter 11 (right prism), recomputed independently."""
import random
import re
from fractions import Fraction as F

import pytest

from mathhelper.curriculum.chapters.sn_5e_prisme import CHAPTER as PRI, assessment

BY_ID = {e.id.split("/")[1]: e for e in PRI.exercises().values()}


def ints_in(prompt):
    """Read the whole numbers of a prompt."""
    return [int(x) for x in re.findall(r"\d+", prompt.replace(" ", "").replace(" 000", "000"))]


def test_fixed_answers_match_an_independent_recalculation():
    plain = {"s1-g1": 5 + 2, "s1-g2": 3 * 5, "s1-g3": 2 * 5, "s1-g4": 21 // 3,
             "s2-g1": 2 * (8 + 5) * 7, "s2-g2": 15 * 6, "s2-g3": 240 // 12, "s2-g4": 4,
             "s3-g1": 200 + 2 * 30, "s3-g2": 2 * (6 * 5 + 6 * 2 + 5 * 2), "s3-g3": 6 * 5 * 5, "s3-g4": (150 - 110) // 2,
             "s4-g1": 10 * 6 * 4, "s4-g2": 35 * 6, "s4-g3": 500 // 10, "s4-g4": 8000 // 1000,
             "p1": 8 + 2, "p2": 3 * 8, "p3": 2 * 8, "p4": 30 // 3, "p5": 12 // 2 + 2,
             "p8": 4 * 5 * 9, "p9": 2 * (12 + 7) * 5, "p10": (5 + 12 + 13) * 4, "p11": 360 // 36, "p12": 9,
             "p13": 96 + 2 * 18, "p14": 2 * (4 * 3 + 4 * 2 + 3 * 2), "p15": 6 * 10 * 10, "p16": 6 * 4 * 4, "p17": 200 - 2 * 25,
             "p18": (3 + 4 + 5) * 10 + 2 * (3 * 4 // 2),
             "p19": 7 * 5 * 2, "p20": 6**3, "p21": 28 * 15, "p22": 720 // 60, "p23": 10 * 6 // 2 * 8, "p24": 12000 // 1000,
             "p25": F(2) * 1 * F(1, 2), "p26": 1000, "p27": 96 // (8 * 4), "p28": 20 * 10 * 5, "p29": 300 // 2,
             "p30": 20 * 10 - 12 * 10, "p31": (2 + 2 + 2) * 3, "p32": (4**3) // (2**3)}
    for key, value in plain.items():
        assert BY_ID[key].answer.value == F(value), (key, BY_ID[key].answer.value, value)
    choices = {"s1-g5": 0, "p6": 0, "p7": 0}
    for key, index in choices.items():
        assert BY_ID[key].answer.value == index, key
    assert set(plain) | set(choices) == set(BY_ID)


def test_chapter_shape():
    assert PRI.number == 11 and PRI.level == "5e" and len(PRI.sections) == 4 and PRI.also_for == ("ci",)


def test_assessment_keys_match_a_recalculation_from_each_prompt():
    for seed in range(300):
        q = {x.id.split("/")[1]: x for x in assessment(random.Random(f"pri{seed}"))}
        assert sorted(q, key=lambda k: int(k[1:])) == [f"a{i}" for i in range(1, 13)]
        sides = {"triangle": 3, "quadrilatère": 4, "pentagone": 5, "hexagone": 6, "heptagone": 7, "octogone": 8}
        for key, formula in (("a1", lambda n: n + 2), ("a2", lambda n: 3 * n), ("a3", lambda n: 2 * n)):
            n = next(v for k, v in sides.items() if k in q[key].prompt)
            assert q[key].answer.value == formula(n)
        length, width, h = ints_in(q["a4"].prompt)[:3]
        assert q["a4"].answer.value == length * width * h
        length, width, h = ints_in(q["a5"].prompt)[:3]
        assert q["a5"].answer.value == 2 * (length + width) * h
        length, width, h = ints_in(q["a6"].prompt)[:3]
        assert q["a6"].answer.value == 2 * (length * width + length * h + width * h)
        base, h = ints_in(q["a7"].prompt)[:2]
        assert q["a7"].answer.value == base * h
        volume, base = ints_in(q["a8"].prompt)[:2]
        assert q["a8"].answer.value * base == volume
        p, q_, h = ints_in(q["a9"].prompt)[:3]
        assert q["a9"].answer.value == F(p * q_ * h, 2)
        perimeter, h = ints_in(q["a10"].prompt)[:2]
        assert q["a10"].answer.value == perimeter * h
        assert q["a11"].answer.value * 1000 == ints_in(q["a11"].prompt)[0]
        a = ints_in(q["a12"].prompt)[0]
        assert q["a12"].answer.value == 6 * a * a


@pytest.fixture
def student(app, make_user):
    make_user("ba@example.com", "secret123", "Ba")
    client = app.test_client()
    client.post("/login", data={"email": "ba@example.com", "password": "secret123"})
    client.post("/settings/curriculum", data={"curriculum": "sn:5e"})
    return client


def test_pages_render(student):
    for path in ["", "/practice", "/summary", "/assessment?seed=abcd1234", "/s/elements", "/s/patron", "/s/aire", "/s/volume"]:
        for headers in ({}, {"Accept-Language": "fr-FR,fr;q=0.9"}):
            assert student.get(f"/curriculum/{PRI.id}{path}", headers=headers).status_code == 200, path
    assert student.post("/curriculum/check", json={"exercise": f"{PRI.id}/s4-g1", "answer": "240 cm³"}).get_json()["status"] == "correct"
