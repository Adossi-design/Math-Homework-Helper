"""Cinquième chapter 10 (rectangle, rhombus and square), recomputed independently."""
import random
import re
from fractions import Fraction as F

import pytest

from mathhelper.curriculum.chapters.sn_5e_parallelogrammes import CHAPTER as PAR, assessment

BY_ID = {e.id.split("/")[1]: e for e in PAR.exercises().values()}


def numbers_in(prompt):
    """Read the decimal numbers written in a prompt, comma as the decimal mark."""
    return [F(x.replace(",", ".")) for x in re.findall(r"\d+(?:,\d+)?", prompt)]


def test_fixed_answers_match_an_independent_recalculation():
    plain = {"s1-g1": 18, "s1-g2": F(13, 2), "s1-g3": 2 * (9 + 4), "s1-g4": 9 * 4,
             "s2-g1": 4 * F(85, 10), "s2-g2": 14 * 8 // 2, "s2-g3": 16 // 2, "s2-g4": 180 - 70,
             "s3-g1": 4 * 12, "s3-g2": 12 * 12, "s3-g3": 36 // 4, "s3-g4": 20 // 2,
             "s4-g2": 2 * (50 + 30) * 500, "s4-g3": 20 * 15 // 2, "s4-g4": 12 * 12 - 10 * 10,
             "p1": 25, "p2": 2 * F(15, 2), "p3": 2 * (15 + 8), "p4": 15 * 8, "p5": 20 - 6, "p6": 84 // 12,
             "p9": 4 * 11, "p10": F(50, 4), "p11": 9 * 12 // 2, "p12": 2 * 48 // 12, "p13": F(9, 2), "p14": 180 - 50, "p15": 80 // 2, "p16": 90,
             "p18": 4 * F(75, 10), "p19": F(75, 10) ** 2, "p20": (44 // 4) ** 2, "p21": 15, "p22": 45,
             "p26": 2 * (60 + 40) * 1200, "p27": 25 * 25, "p28": 2 * 96 // 12, "p29": 12 * 12 - 8 * 8,
             "p31": 2 * (18 + 10) // 4, "p32": 2}
    # p29 is a 2 cm border all around, so the outer side is 8 + 2 * 2 = 12
    assert 8 + 2 * 2 == 12
    for key, value in plain.items():
        assert BY_ID[key].answer.value == F(value), (key, BY_ID[key].answer.value, value)
    assert 18 * 10 == 180 and 14 * 14 == 196 and 196 > 180
    choices = {"s1-g5": 0, "s2-g5": 0, "s3-g5": 0, "s4-g1": 0, "s4-g5": 0, "p7": 0, "p8": 0, "p17": 0, "p23": 0, "p24": 0, "p25": 0, "p30": 0}
    for key, index in choices.items():
        assert BY_ID[key].answer.value == index, key
    assert set(plain) | set(choices) == set(BY_ID)


def test_chapter_shape_and_figures():
    assert PAR.number == 10 and PAR.level == "5e" and len(PAR.sections) == 4 and PAR.also_for == ("ci",)
    assert len([b for s in PAR.sections for b in s.blocks if b["type"] == "figure"]) >= 3


def test_assessment_keys_match_a_recalculation_from_each_prompt():
    for seed in range(300):
        q = {x.id.split("/")[1]: x for x in assessment(random.Random(f"par{seed}"))}
        assert sorted(q, key=lambda k: int(k[1:])) == [f"a{i}" for i in range(1, 13)]
        assert q["a1"].answer.value == numbers_in(q["a1"].prompt)[0]
        assert q["a2"].answer.value * 2 == numbers_in(q["a2"].prompt)[0]
        length, width = numbers_in(q["a3"].prompt)[:2]
        assert q["a3"].answer.value == 2 * (length + width)
        length, width = numbers_in(q["a4"].prompt)[:2]
        assert q["a4"].answer.value == length * width
        assert q["a5"].answer.value == 4 * numbers_in(q["a5"].prompt)[0]
        big, small = numbers_in(q["a6"].prompt)[:2]
        assert q["a6"].answer.value == big * small / 2
        area, diag = numbers_in(q["a7"].prompt)[:2]
        assert q["a7"].answer.value * diag == 2 * area
        assert q["a8"].answer.value == 180 - numbers_in(q["a8"].prompt)[0]
        side = numbers_in(q["a9"].prompt)[0]
        assert q["a9"].answer.value == side * side
        perimeter = numbers_in(q["a10"].prompt)[0]
        assert q["a10"].answer.value == (perimeter / 4) ** 2
        text = q["a11"].prompt
        both = "égales et perpendiculaires" in text
        expected = 2 if both else 0 if "égales" in text else 1
        assert q["a11"].answer.value == expected
        side, border = numbers_in(q["a12"].prompt)[:2]
        assert q["a12"].answer.value == (side + 2 * border) ** 2 - side**2


@pytest.fixture
def student(app, make_user):
    make_user("fall@example.com", "secret123", "Fall")
    client = app.test_client()
    client.post("/login", data={"email": "fall@example.com", "password": "secret123"})
    client.post("/settings/curriculum", data={"curriculum": "sn:5e"})
    return client


def test_pages_render(student):
    for path in ["", "/practice", "/summary", "/assessment?seed=abcd1234", "/s/rectangle", "/s/losange", "/s/carre", "/s/problemes"]:
        for headers in ({}, {"Accept-Language": "fr-FR,fr;q=0.9"}):
            assert student.get(f"/curriculum/{PAR.id}{path}", headers=headers).status_code == 200, path
    assert student.post("/curriculum/check", json={"exercise": f"{PAR.id}/s1-g3", "answer": "26 cm"}).get_json()["status"] == "correct"
