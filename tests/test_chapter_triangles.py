"""Chapter 13 (triangles), recomputed independently from the numbers shown in each prompt."""
import random
import re
from fractions import Fraction as F

import pytest

from mathhelper.curriculum.chapters.sn_6e_triangles import CHAPTER as TRI, assessment, is_triangle

BY_ID = {e.id.split("/")[1]: e for e in TRI.exercises().values()}


def numbers_in(prompt):
    """Read the decimal numbers written in a prompt, comma as the decimal mark."""
    return [F(x.replace(",", ".")) for x in re.findall(r"\d+(?:,\d+)?", prompt)]


def test_fixed_answers_match_an_independent_recalculation():
    plain = {"s1-g3": 25 - 18, "s1-g4": 36 // 3,
             "s2-g1": 3 + 4 + 5, "s2-g2": 2 * F(65, 10) + 4, "s2-g3": 3 * F(85, 10), "s2-g4": 30 - 11 - 8, "s2-g5": (20 + 35 + 45) * 200,
             "s3-g1": F(10 * 6, 2), "s3-g2": F(5 * 12, 2), "s3-g3": F(2 * 24, 8), "s3-g4": F(9 * 4, 2),
             "s4-g1": 18 // 2, "s4-g2": 48 // 2, "s4-g5": F(9 * 12, 2),
             "p5": 40 - 24, "p6": 51 // 3, "p7": 32 - 20,
             "p9": 7 + 8 + 9, "p10": F(24, 10) + F(36, 10) + F(45, 10), "p11": 2 * 9 + 6, "p12": 3 * F(125, 10), "p13": 45 - 14 - 17, "p14": 60 + 80 + 100,
             "p15": F(12, 10) + F(8, 10) + 1, "p16": F(45, 10) / 3, "p17": (25 + 30 + 45) * 800,
             "p18": F(12 * 7, 2), "p19": F(5) * F(32, 10) / 2, "p20": F(7 * 10, 2), "p21": F(2 * 36, 9), "p22": F(2 * 45, 15), "p23": F(30 * 50, 2), "p24": F(8 * 5, 2) / 4, "p25": F(14 * 6, 2),
             "p27": 2 * 7, "p28": 70 // 2, "p29": 3, "p31": F(2 * (9 * 12 // 2), 15), "p32": 3}
    for key, value in plain.items():
        assert BY_ID[key].answer.value == F(value), (key, BY_ID[key].answer.value, value)
    choices = {"s1-g1": 0, "s1-g2": 1, "s1-g5": 1, "s3-g5": 1, "s4-g3": 1, "s4-g4": 1,
               "p1": 2, "p2": 0, "p3": 1, "p4": 1, "p8": 1, "p26": 0, "p30": 1}
    for key, index in choices.items():
        assert BY_ID[key].answer.value == index, key
    assert set(plain) | set(choices) == set(BY_ID)


def test_chapter_shape_and_alignment():
    assert TRI.number == 13 and len(TRI.sections) == 4 and TRI.also_for == ("ci",)
    assert "lesson 5 of the C" in TRI.status_note and "sum of the angles" in TRI.status_note
    assert len([b for s in TRI.sections for b in s.blocks if b["type"] == "figure"]) >= 6


def test_assessment_keys_match_a_recalculation_from_each_prompt():
    for seed in range(300):
        q = {x.id.split("/")[1]: x for x in assessment(random.Random(f"tri{seed}"))}
        assert sorted(q, key=lambda k: int(k[1:])) == [f"a{i}" for i in range(1, 13)]
        sides = sorted(int(x) for x in numbers_in(q["a1"].prompt)[:3])
        expected = 1 if len(set(sides)) == 1 else 0 if len(set(sides)) == 2 else 2
        assert q["a1"].answer.value == expected
        assert q["a2"].answer.value == sum(numbers_in(q["a2"].prompt)[:3])
        assert is_triangle(numbers_in(q["a1"].prompt)[:3]) and is_triangle(numbers_in(q["a2"].prompt)[:3])
        assert is_triangle(list(numbers_in(q["a10"].prompt)[:3]))
        assert is_triangle(numbers_in(q["a5"].prompt)[1:3] + [q["a5"].answer.value])
        a3, b3 = numbers_in(q["a3"].prompt)[:2]
        assert is_triangle([a3, a3, b3])
        a, b = numbers_in(q["a3"].prompt)[:2]
        assert q["a3"].answer.value == 2 * a + b
        assert q["a4"].answer.value * 3 == numbers_in(q["a4"].prompt)[0]
        p, s1, s2 = numbers_in(q["a5"].prompt)[:3]
        assert q["a5"].answer.value == p - s1 - s2 > 0
        base, height = numbers_in(q["a6"].prompt)[:2]
        assert q["a6"].answer.value == base * height / 2
        u, v = numbers_in(q["a7"].prompt)[:2]
        assert q["a7"].answer.value == u * v / 2 and (u * v) % 2 == 0
        area, base = numbers_in(q["a8"].prompt)[:2]
        assert q["a8"].answer.value * base == 2 * area
        assert q["a9"].answer.value * 2 == numbers_in(q["a9"].prompt)[0]
        s1, s2, s3, price = numbers_in(q["a10"].prompt)[:4]
        assert q["a10"].answer.value == (s1 + s2 + s3) * price
        assert q["a11"].answer.value * 2 == numbers_in(q["a11"].prompt)[0]
        assert q["a12"].options[q["a12"].answer.value] == "Il a oublié de diviser par 2"


@pytest.fixture
def student(app, make_user):
    make_user("sow@example.com", "secret123", "Sow")
    client = app.test_client()
    client.post("/login", data={"email": "sow@example.com", "password": "secret123"})
    client.post("/settings/curriculum", data={"curriculum": "sn:6e"})
    return client


def test_pages_render(student):
    for path in ["", "/practice", "/summary", "/assessment?seed=abcd1234", "/s/natures", "/s/perimetre", "/s/aire", "/s/droites"]:
        for headers in ({}, {"Accept-Language": "fr-FR,fr;q=0.9"}):
            assert student.get(f"/curriculum/{TRI.id}{path}", headers=headers).status_code == 200, path
    assert student.post("/curriculum/check", json={"exercise": f"{TRI.id}/s3-g1", "answer": "30 cm²"}).get_json()["status"] == "correct"
    assert student.post("/curriculum/check", json={"exercise": f"{TRI.id}/s3-g1", "answer": "60"}).get_json()["status"] == "wrong"
