"""Chapter 10 (boxes, cubes and cylinders), recomputed independently from the numbers shown in each prompt."""
import random
import re
from fractions import Fraction as F

import pytest

from mathhelper.curriculum.chapters.sn_6e_solides import CHAPTER as SOL, assessment

BY_ID = {e.id.split("/")[1]: e for e in SOL.exercises().values()}
PI = F(314, 100)


def numbers_in(prompt):
    """Read the decimal numbers written in a prompt, comma as the decimal mark."""
    return [F(x.replace(",", ".")) for x in re.findall(r"\d+(?:,\d+)?", prompt)]


def test_fixed_answers_match_an_independent_recalculation():
    plain = {"s1-g1": 6, "s1-g2": 12, "s1-g3": 8, "s1-g4": 12 * 7, "s1-g5": 4 * (5 + 3 + 2),
             "s2-g1": 16, "s2-g2": 6 * 9, "s2-g3": 2 * (5 + 3) * 4, "s2-g4": 2 * (15 + 10 + 6),
             "s3-g1": 60, "s3-g2": 27, "s3-g3": F(45, 10), "s3-g4": 1000 * F(1) * F(5, 10) * F(4, 10), "s3-g5": F(120, 30),
             "s4-g1": PI * 4, "s4-g2": 2 * PI * 4, "s4-g3": 2 * PI * 3 * 5, "s4-g4": PI * 4 * 10,
             "p1": 12, "p2": 8, "p3": 6, "p4": 3, "p5": 108, "p6": 64, "p7": 2 * PI * 5, "p9": 216, "p10": 52, "p11": 100, "p12": 600, "p13": 600 + 1000,
             "p14": 25, "p15": 5, "p17": 120, "p18": 125, "p19": F(2750, 1000), "p20": 3500, "p21": F(60 * 30 * 40, 1000), "p22": F(150, 50),
             "p23": F(12, 10) ** 3, "p24": 1000 * 2 * F(15, 10), "p25": 60, "p27": PI * 100, "p28": 2 * PI * 7, "p29": 2 * PI * 2 * 10,
             "p30": PI * 25 * 4, "p31": PI * 100 * 30 / 1000, "p32": 16}
    for key, value in plain.items():
        assert BY_ID[key].answer.value == F(value), (key, BY_ID[key].answer.value, value)
    choices = {"s2-g5": 2, "s4-g5": 1, "p8": 2, "p16": 0, "p26": 0}
    for key, index in choices.items():
        assert BY_ID[key].answer.value == index, key
    assert F(15) * F(628, 100) < 100 < 16 * F(628, 100)
    assert set(plain) | set(choices) == set(BY_ID)


def test_chapter_shape_and_alignment():
    assert SOL.number == 10 and len(SOL.sections) == 4 and SOL.also_for == ("ci",)
    assert "lesson 8 of the C" in SOL.status_note


def test_assessment_keys_match_a_recalculation_from_each_prompt():
    for seed in range(300):
        q = {x.id.split("/")[1]: x for x in assessment(random.Random(f"so{seed}"))}
        assert sorted(q, key=lambda k: int(k[1:])) == [f"a{i}" for i in range(1, 13)]
        a, b, c = numbers_in(q["a1"].prompt)[:3]
        assert q["a1"].answer.value == 4 * (a + b + c)
        assert q["a2"].answer.value == 12 * numbers_in(q["a2"].prompt)[0]
        a, b, c = numbers_in(q["a3"].prompt)[:3]
        assert q["a3"].answer.value == 2 * (a + b) * c
        a, b, c = numbers_in(q["a4"].prompt)[:3]
        assert q["a4"].answer.value == 2 * (a * b + a * c + b * c)
        assert q["a5"].answer.value == 6 * numbers_in(q["a5"].prompt)[0] ** 2
        a, b, c = numbers_in(q["a6"].prompt)[:3]
        assert q["a6"].answer.value == a * b * c
        assert q["a7"].answer.value == numbers_in(q["a7"].prompt)[0] ** 3
        assert q["a8"].answer.value == numbers_in(q["a8"].prompt)[0] / 1000
        volume, length, width = numbers_in(q["a9"].prompt)[:3]
        assert q["a9"].answer.value * length * width == volume
        r, h = numbers_in(q["a10"].prompt)[:2]
        assert q["a10"].answer.value == PI * r * r * h
        r, h = numbers_in(q["a11"].prompt)[:2]
        assert q["a11"].answer.value == 2 * PI * r * h
        assert q["a12"].options[q["a12"].answer.value].startswith("Il a calculé")


@pytest.fixture
def student(app, make_user):
    make_user("diop@example.com", "secret123", "Diop")
    client = app.test_client()
    client.post("/login", data={"email": "diop@example.com", "password": "secret123"})
    client.post("/settings/curriculum", data={"curriculum": "ci:6e"})
    return client


def test_pages_render_and_unit_answers_are_read(student):
    for path in ["", "/practice", "/summary", "/assessment?seed=abcd1234", "/s/elements", "/s/aires", "/s/volumes", "/s/cylindre"]:
        for headers in ({}, {"Accept-Language": "fr-FR,fr;q=0.9"}):
            assert student.get(f"/curriculum/{SOL.id}{path}", headers=headers).status_code == 200, path
    for typed in ["84", "84 cm", "84cm"]:
        assert student.post("/curriculum/check", json={"exercise": f"{SOL.id}/s1-g4", "answer": typed}).get_json()["status"] == "correct", typed
    for typed in ["16 cm²", "16 cm2", "16"]:
        assert student.post("/curriculum/check", json={"exercise": f"{SOL.id}/s2-g1", "answer": typed}).get_json()["status"] == "correct", typed
