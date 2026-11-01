"""Cinquième chapter 8 (special triangles and the bisector), recomputed independently."""
import random
import re
from fractions import Fraction as F

import pytest

from mathhelper.curriculum.chapters.sn_5e_triangles import CHAPTER as TRI, assessment

BY_ID = {e.id.split("/")[1]: e for e in TRI.exercises().values()}


def ints_in(prompt):
    """Read the whole numbers of a prompt."""
    return [int(x) for x in re.findall(r"\d+", prompt)]


def test_fixed_answers_match_an_independent_recalculation():
    plain = {"s1-g1": 3, "s1-g2": 1, "s1-g3": 0, "s1-g4": 14 // 2, "s1-g5": 64 // 2,
             "s2-g1": 180 - 140, "s2-g2": 180 - 144, "s2-g3": (180 - 100) // 2, "s2-g4": (40 - 14) // 2,
             "s3-g3": 45 // 3, "s3-g4": 10 * 10 // 2, "s3-g5": 90 // 2,
             "s4-g1": 84 // 2, "s4-g2": (180 - 100) // 2, "s4-g3": 180 - 25 - 65, "s4-g4": (180 - 140) // 2,
             "p1": 1, "p2": 0, "p3": F(9, 2), "p4": 25, "p8": 3, "p9": 180 - 110, "p10": (180 - 36) // 2, "p11": 180 - 140, "p12": 12 + 12 + 8, "p13": 50 - 36,
             "p14": 180 - 160, "p15": (180 - 80) // 2, "p17": 60, "p18": 36 // 3, "p19": 180 - 60, "p21": 12 * 12 // 2, "p22": 90 - 34, "p23": 2, "p24": 3,
             "p25": 45, "p26": (180 - 80) // 2, "p27": 180 - 20 - 70, "p28": (180 - 150) // 2, "p29": 56, "p30": 180 - 40 - 60}
    for key, value in plain.items():
        assert BY_ID[key].answer.value == F(value), (key, BY_ID[key].answer.value, value)
    choices = {"s2-g5": 0, "s3-g1": 0, "s3-g2": 0, "s4-g5": 0, "p5": 0, "p6": 0, "p7": 0, "p16": 0, "p20": 0, "p31": 0, "p32": 0}
    for key, index in choices.items():
        assert BY_ID[key].answer.value == index, key
    assert 40 + 50 == 90 and 30 + 60 == 90 and 60 // 2 == 30
    assert set(plain) | set(choices) == set(BY_ID)


def test_chapter_shape_and_figures():
    assert TRI.number == 8 and TRI.level == "5e" and len(TRI.sections) == 4 and TRI.also_for == ("ci",)
    assert len([b for s in TRI.sections for b in s.blocks if b["type"] == "figure"]) >= 4


def test_assessment_keys_match_a_recalculation_from_each_prompt():
    for seed in range(300):
        q = {x.id.split("/")[1]: x for x in assessment(random.Random(f"t5{seed}"))}
        assert sorted(q, key=lambda k: int(k[1:])) == [f"a{i}" for i in range(1, 13)]
        prompt = q["a1"].prompt
        expected = 0 if "différents" in prompt else 1 if "isocèle" in prompt else 3
        assert q["a1"].answer.value == expected
        assert q["a2"].answer.value * 2 == ints_in(q["a2"].prompt)[0] or q["a2"].answer.value * 2 == ints_in(q["a2"].prompt)[-1]
        top = ints_in(q["a3"].prompt)[0]
        assert q["a3"].answer.value * 2 == top
        b = ints_in(q["a4"].prompt)[0]
        assert q["a4"].answer.value == 180 - 2 * b > 0
        top = ints_in(q["a5"].prompt)[0]
        assert q["a5"].answer.value == F(180 - top, 2)
        perimeter, base = ints_in(q["a6"].prompt)[:2]
        assert q["a6"].answer.value == F(perimeter - base, 2) and base < 2 * q["a6"].answer.value
        assert q["a7"].answer.value * 3 == ints_in(q["a7"].prompt)[0]
        x, y = ints_in(q["a8"].prompt)[:2]
        expected = 0 if x + y == 90 else 1
        assert q["a8"].answer.value == expected and (x != y or x not in (45, 60)) and not (x == y and x + y == 90)
        side = ints_in(q["a9"].prompt)[0]
        assert q["a9"].answer.value == F(side * side, 2)
        assert q["a10"].answer.value * 2 == ints_in(q["a10"].prompt)[0] or q["a10"].answer.value * 2 == ints_in(q["a10"].prompt)[-1]
        b, c = ints_in(q["a11"].prompt)[:2]
        assert q["a11"].answer.value == F(180 - b - c, 2)
        bad, b = ints_in(q["a12"].prompt)[:2]
        assert q["a12"].answer.value == 180 - bad - b


@pytest.fixture
def student(app, make_user):
    make_user("lo@example.com", "secret123", "Lo")
    client = app.test_client()
    client.post("/login", data={"email": "lo@example.com", "password": "secret123"})
    client.post("/settings/curriculum", data={"curriculum": "sn:5e"})
    return client


def test_pages_render(student):
    for path in ["", "/practice", "/summary", "/assessment?seed=abcd1234", "/s/axes", "/s/isocele", "/s/equilateral", "/s/bissectrice"]:
        for headers in ({}, {"Accept-Language": "fr-FR,fr;q=0.9"}):
            assert student.get(f"/curriculum/{TRI.id}{path}", headers=headers).status_code == 200, path
    assert student.post("/curriculum/check", json={"exercise": f"{TRI.id}/s1-g5", "answer": "32°"}).get_json()["status"] == "correct"
