"""Cinquième chapter 6 (angles), recomputed independently."""
import random
import re
from fractions import Fraction as F

import pytest

from mathhelper.curriculum.chapters.sn_5e_angles import CHAPTER as ANG, assessment

BY_ID = {e.id.split("/")[1]: e for e in ANG.exercises().values()}


def ints_in(prompt):
    """Read the whole numbers of a prompt."""
    return [int(x) for x in re.findall(r"\d+", prompt)]


def test_fixed_answers_match_an_independent_recalculation():
    plain = {"s1-g1": 90 - 62, "s1-g2": 180 - 62, "s1-g3": 180 - 125, "s1-g4": F(90, 4),
             "s2-g1": 55, "s2-g2": 180 - 55, "s2-g3": 2 * (180 - 72), "s2-g4": 15,
             "s3-g1": 180 - 115, "s3-g2": 90 - 28, "s3-g3": (180 - 100) // 2, "s3-g4": 180 - 110,
             "s4-g1": F(180 - 70, 4), "s4-g2": (180 + 40) // 2, "s4-g3": 30, "s4-g4": 36,
             "p1": 73, "p2": 163, "p3": 45, "p4": 90, "p5": 36, "p6": 35, "p7": 73, "p10": 112, "p11": 68, "p12": 150, "p13": 20, "p14": 4,
             "p16": 180 - 100, "p17": 180 - 135, "p18": 90 - 49, "p19": (180 - 50) // 2, "p20": 180 - 144, "p21": 60, "p22": 90, "p23": 60,
             "p26": (180 - 84) // 3, "p27": 75, "p28": 45, "p29": 180 - 160, "p30": 72, "p32": 180 - (180 - 35 - 85)}
    for key, value in plain.items():
        assert BY_ID[key].answer.value == F(value), (key, BY_ID[key].answer.value, value)
    assert 2 * 20 + 10 == 4 * 20 - 30 and 70 + 4 * F(55, 2) == 180 and 36 * 5 == 180 and 18 * 5 == 90 and 4 * 18 == 72
    choices = {"s1-g5": 0, "s2-g5": 0, "s3-g5": 0, "s4-g5": 0, "p8": 0, "p9": 0, "p15": 0, "p24": 0, "p25": 0, "p31": 0}
    for key, index in choices.items():
        assert BY_ID[key].answer.value == index, key
    assert set(plain) | set(choices) == set(BY_ID)


def test_chapter_shape_and_figures():
    assert ANG.number == 6 and ANG.level == "5e" and len(ANG.sections) == 4 and ANG.also_for == ("ci",)
    assert len([b for s in ANG.sections for b in s.blocks if b["type"] == "figure"]) >= 4


def test_assessment_keys_match_a_recalculation_from_each_prompt():
    for seed in range(300):
        q = {x.id.split("/")[1]: x for x in assessment(random.Random(f"a5{seed}"))}
        assert sorted(q, key=lambda k: int(k[1:])) == [f"a{i}" for i in range(1, 13)]
        assert q["a1"].answer.value == 90 - ints_in(q["a1"].prompt)[0]
        assert q["a2"].answer.value == 180 - ints_in(q["a2"].prompt)[0]
        a, b = ints_in(q["a3"].prompt)[:2]
        total = a + b
        assert q["a3"].answer.value == (0 if total == 90 else 1 if total == 180 else 2)
        assert q["a4"].answer.value == 180 - ints_in(q["a4"].prompt)[-1]
        assert q["a5"].answer.value == ints_in(q["a5"].prompt)[-1]
        values = ints_in(q["a6"].prompt)
        assert q["a6"].answer.value == 180 - values[0] and values[0] != 90
        a, b = ints_in(q["a7"].prompt)[:2]
        assert q["a7"].answer.value == 180 - a - b > 0
        assert q["a8"].answer.value == 90 - ints_in(q["a8"].prompt)[0]
        top = ints_in(q["a9"].prompt)[0]
        assert q["a9"].answer.value == F(180 - top, 2)
        third, k = ints_in(q["a10"].prompt)[:2]
        assert q["a10"].answer.value * (k + 1) == 180 - third
        diff = ints_in(q["a11"].prompt)[0]
        assert q["a11"].answer.value == F(180 + diff, 2)
        a, p, b, qq = [int(x) for x in re.search(r"(\d)x \+ (\d+) et (\d)x − (\d+)", q["a12"].prompt).groups()]
        x = q["a12"].answer.value
        assert a * x + p == b * x - qq and x.denominator == 1


@pytest.fixture
def student(app, make_user):
    make_user("ndour@example.com", "secret123", "Ndour")
    client = app.test_client()
    client.post("/login", data={"email": "ndour@example.com", "password": "secret123"})
    client.post("/settings/curriculum", data={"curriculum": "sn:5e"})
    return client


def test_pages_render_and_degrees_are_read(student):
    for path in ["", "/practice", "/summary", "/assessment?seed=abcd1234", "/s/adjacents", "/s/opposes", "/s/triangle", "/s/problemes"]:
        for headers in ({}, {"Accept-Language": "fr-FR,fr;q=0.9"}):
            assert student.get(f"/curriculum/{ANG.id}{path}", headers=headers).status_code == 200, path
    for typed in ["28", "28°", "28 deg", "28 degrés"]:
        assert student.post("/curriculum/check", json={"exercise": f"{ANG.id}/s1-g1", "answer": typed}).get_json()["status"] == "correct", typed
    assert student.post("/curriculum/check", json={"exercise": f"{ANG.id}/s1-g4", "answer": "22,5°"}).get_json()["status"] == "correct"
