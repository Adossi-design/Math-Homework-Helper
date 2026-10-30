"""Chapter 14 (the parallelogram), recomputed independently from the numbers shown in each prompt."""
import random
import re
from fractions import Fraction as F

import pytest

from mathhelper.curriculum.chapters.sn_6e_parallelogramme import CHAPTER as PAR, assessment

BY_ID = {e.id.split("/")[1]: e for e in PAR.exercises().values()}


def numbers_in(prompt):
    """Read the decimal numbers written in a prompt, comma as the decimal mark."""
    return [F(x.replace(",", ".")) for x in re.findall(r"\d+(?:,\d+)?", prompt)]


def test_fixed_answers_match_an_independent_recalculation():
    plain = {"s1-g1": 9, "s1-g2": 16 // 2, "s1-g3": F(11, 2), "s2-g4": 6 + 6, "s2-g5": 2,
             "s3-g1": 2 * (9 + 4), "s3-g2": 2 * (F(75, 10) + F(25, 10)), "s3-g3": 36 // 2 - 11, "s3-g4": 50 // 2 - 15, "s3-g5": 2 * (30 + 20) * 500,
             "s4-g1": 10 * 6, "s4-g2": 84 // 7, "s4-g3": 70 // 2, "s4-g4": F(85, 10) * 4,
             "p1": F(65, 10), "p2": 20 // 2, "p3": 2 * F(42, 10), "p4": 5, "p7": 14 // 2 + 10 // 2, "p11": 2 * F(35, 10), "p12": 2, "p13": 4,
             "p14": 2 * (12 + 7), "p15": 2 * (F(42, 10) + F(53, 10)), "p16": 42 // 2 - 8, "p17": F(25, 2) - F(65, 10), "p18": 2 * (60 + 45), "p19": (64 // 2) // 4,
             "p20": F(2 * (80 + 50), 100) * 20,
             "p21": 15 * 8, "p22": F(65, 10) * 4, "p23": 96 // 12, "p24": 150 // 6, "p25": 2 * 42, "p26": 10 * 5, "p27": 40 * 25 * 200, "p29": 56 // 2, "p30": 5 * F(32, 10)}
    for key, value in plain.items():
        assert BY_ID[key].answer.value == F(value), (key, BY_ID[key].answer.value, value)
    choices = {"s1-g4": 1, "s1-g5": 1, "s2-g1": 0, "s2-g2": 1, "s2-g3": 0, "s4-g5": 0,
               "p5": 1, "p6": 1, "p8": 0, "p9": 1, "p10": 1, "p28": 0, "p31": 0, "p32": 0}
    for key, index in choices.items():
        assert BY_ID[key].answer.value == index, key
    assert set(plain) | set(choices) == set(BY_ID)


def test_chapter_shape_and_alignment():
    assert PAR.number == 14 and len(PAR.sections) == 4 and PAR.also_for == ("ci",)
    assert "lesson 6 of the C" in PAR.status_note and "not been checked against the official Senegalese" in PAR.status_note
    assert len([b for s in PAR.sections for b in s.blocks if b["type"] == "figure"]) >= 4


def test_assessment_keys_match_a_recalculation_from_each_prompt():
    for seed in range(300):
        q = {x.id.split("/")[1]: x for x in assessment(random.Random(f"par{seed}"))}
        assert sorted(q, key=lambda k: int(k[1:])) == [f"a{i}" for i in range(1, 13)]
        assert q["a1"].answer.value == numbers_in(q["a1"].prompt)[0]
        assert q["a2"].answer.value * 2 == numbers_in(q["a2"].prompt)[0]
        assert q["a3"].answer.value == 2 * numbers_in(q["a3"].prompt)[0]
        a, b = numbers_in(q["a4"].prompt)[:2]
        assert q["a4"].answer.value == 2 * (a + b)
        perimeter, side = numbers_in(q["a5"].prompt)[:2]
        assert q["a5"].answer.value == perimeter / 2 - side > 0
        base, height = numbers_in(q["a6"].prompt)[:2]
        assert q["a6"].answer.value == base * height
        area, base = numbers_in(q["a7"].prompt)[:2]
        assert q["a7"].answer.value * base == area
        area, height = numbers_in(q["a8"].prompt)[:2]
        assert q["a8"].answer.value * height == area
        assert q["a9"].answer.value * 2 == numbers_in(q["a9"].prompt)[0]
        good = ("Les deux paires de côtés opposés sont égales", "Les diagonales se coupent en leur milieu")
        assert [i for i, o in enumerate(q["a10"].options) if o in good] == [q["a10"].answer.value]
        a, b, price = numbers_in(q["a11"].prompt)[:3]
        assert q["a11"].answer.value == 2 * (a + b) * price
        base, side, height = numbers_in(q["a12"].prompt)[:3]
        assert q["a12"].options[q["a12"].answer.value] == "Il a pris le côté penché au lieu de la hauteur" and side > height


@pytest.fixture
def student(app, make_user):
    make_user("gueye@example.com", "secret123", "Gueye")
    client = app.test_client()
    client.post("/login", data={"email": "gueye@example.com", "password": "secret123"})
    client.post("/settings/curriculum", data={"curriculum": "sn:6e"})
    return client


def test_pages_render(student):
    for path in ["", "/practice", "/summary", "/assessment?seed=abcd1234", "/s/definition", "/s/justifier", "/s/perimetre", "/s/aire"]:
        for headers in ({}, {"Accept-Language": "fr-FR,fr;q=0.9"}):
            assert student.get(f"/curriculum/{PAR.id}{path}", headers=headers).status_code == 200, path
    assert student.post("/curriculum/check", json={"exercise": f"{PAR.id}/s4-g1", "answer": "60 cm²"}).get_json()["status"] == "correct"
    assert student.post("/curriculum/check", json={"exercise": f"{PAR.id}/s4-g1", "answer": "30"}).get_json()["status"] == "wrong"
