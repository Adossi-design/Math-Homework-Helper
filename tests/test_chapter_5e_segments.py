"""Cinquième chapter 7 (segments and perpendicular bisector), recomputed independently."""
import random
import re
from fractions import Fraction as F

import pytest

from mathhelper.curriculum.chapters.sn_5e_segments import CHAPTER as SEG, assessment

BY_ID = {e.id.split("/")[1]: e for e in SEG.exercises().values()}


def numbers_in(prompt):
    """Read the decimal numbers written in a prompt, comma as the decimal mark."""
    return [F(x.replace(",", ".")) for x in re.findall(r"\d+(?:,\d+)?", prompt)]


def test_fixed_answers_match_an_independent_recalculation():
    plain = {"s1-g1": F(85, 10), "s1-g3": 10 + 10 + 12, "s1-g4": 30 // 2,
             "s2-g3": 15 - F(65, 10), "s2-g4": 12 + 11 - 20, "s2-g5": F(25, 10) + 4,
             "s3-g4": 12 - F(75, 10), "s3-g5": 5 + 8 - 1,
             "s4-g1": 7 + 7 + 8, "s4-g2": 2 * F(55, 10), "s4-g4": 14 + 9 - 20, "s4-g5": 12 // 2,
             "p1": F(42, 10), "p2": 5 + 5 + 6, "p3": F(9, 2), "p4": 18 // 2, "p7": 13 + 13 + 10, "p8": 2 * F(75, 10), "p11": 20 - F(85, 10), "p12": F(32, 10) + F(49, 10),
             "p13": 700 + 600 - 1200, "p14": F(15, 10) + 1 - F(25, 10), "p21": 14 - F(55, 10), "p22": 9 - 6 + 1, "p23": 6 + 9 - 1,
             "p25": 9 + 9 + 10, "p26": 2 * F(65, 10), "p27": F(85, 10) + 9 - 15, "p28": 16 // 2, "p30": 0, "p31": F(32, 10) + F(48, 10), "p32": 0}
    for key, value in plain.items():
        assert BY_ID[key].answer.value == F(value), (key, BY_ID[key].answer.value, value)
    assert 3 + 4 == 7 and 6 + 5 > 10 and 12 ** 2 == 144 and 12 + 5 != 13
    choices = {"s1-g2": 0, "s1-g5": 0, "s2-g1": 0, "s2-g2": 1, "s3-g1": 0, "s3-g2": 1, "s3-g3": 1, "s4-g3": 0,
               "p5": 1, "p6": 0, "p9": 0, "p10": 1, "p15": 0, "p16": 0, "p17": 0, "p18": 1, "p19": 0, "p20": 1, "p24": 0, "p29": 0}
    for key, index in choices.items():
        assert BY_ID[key].answer.value == index, key
    assert set(plain) | set(choices) == set(BY_ID)


def test_chapter_shape_and_figures():
    assert SEG.number == 7 and SEG.level == "5e" and len(SEG.sections) == 4 and SEG.also_for == ("ci",)
    assert len([b for s in SEG.sections for b in s.blocks if b["type"] == "figure"]) >= 3
    assert "Pythag" not in repr([s.blocks for s in SEG.sections]) and "Quatrième" not in repr([s.blocks for s in SEG.sections])


def test_assessment_keys_match_a_recalculation_from_each_prompt():
    for seed in range(300):
        q = {x.id.split("/")[1]: x for x in assessment(random.Random(f"g5{seed}"))}
        assert sorted(q, key=lambda k: int(k[1:])) == [f"a{i}" for i in range(1, 13)]
        assert q["a1"].answer.value == numbers_in(q["a1"].prompt)[0]
        ma, ab = numbers_in(q["a2"].prompt)[:2]
        assert q["a2"].answer.value == 2 * ma + ab
        assert q["a3"].answer.value * 2 == numbers_in(q["a3"].prompt)[0]
        am, mb, ab = numbers_in(q["a4"].prompt)[:3]
        assert q["a4"].answer.value == (0 if am + mb == ab else 1)
        ab, am = numbers_in(q["a5"].prompt)[:2]
        assert q["a5"].answer.value == ab - am > 0
        direct, first, second = numbers_in(q["a6"].prompt)[:3]
        assert q["a6"].answer.value == first + second - direct > 0
        ab, bc, ac = numbers_in(q["a7"].prompt)[:3]
        assert q["a7"].answer.value == (0 if ab + bc == ac else 1)
        a, b, c = numbers_in(q["a8"].prompt)[:3]
        sides = sorted([a, b, c])
        assert q["a8"].answer.value == (0 if sides[2] < sides[0] + sides[1] else 1)
        a, b = numbers_in(q["a9"].prompt)[:2]
        assert q["a9"].answer.value == a + b - 1
        ab, bc = numbers_in(q["a10"].prompt)[:2]
        assert q["a10"].answer.value == ab + bc
        assert q["a11"].answer.value * 2 == numbers_in(q["a11"].prompt)[0]
        assert q["a12"].answer.value == 2 * numbers_in(q["a12"].prompt)[0]


@pytest.fixture
def student(app, make_user):
    make_user("thiam@example.com", "secret123", "Thiam")
    client = app.test_client()
    client.post("/login", data={"email": "thiam@example.com", "password": "secret123"})
    client.post("/settings/curriculum", data={"curriculum": "sn:5e"})
    return client


def test_pages_render(student):
    for path in ["", "/practice", "/summary", "/assessment?seed=abcd1234", "/s/mediatrice", "/s/appartenance", "/s/alignement", "/s/problemes"]:
        for headers in ({}, {"Accept-Language": "fr-FR,fr;q=0.9"}):
            assert student.get(f"/curriculum/{SEG.id}{path}", headers=headers).status_code == 200, path
    assert student.post("/curriculum/check", json={"exercise": f"{SEG.id}/s1-g3", "answer": "32 cm"}).get_json()["status"] == "correct"
