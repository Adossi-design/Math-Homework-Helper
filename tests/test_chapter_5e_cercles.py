"""Cinquième chapter 9 (circles and the circumscribed circle), recomputed independently."""
import random
import re
from fractions import Fraction as F

import pytest

from mathhelper.curriculum.chapters.sn_5e_cercles import CHAPTER as CER, assessment

BY_ID = {e.id.split("/")[1]: e for e in CER.exercises().values()}
PI = F(314, 100)


def numbers_in(prompt):
    """Read the decimal numbers written in a prompt, comma as the decimal mark."""
    return [F(x.replace(",", ".")) for x in re.findall(r"\d+(?:,\d+)?", prompt)]


def position(distance, radius):
    """Return 0 for inside, 1 for on the circle and 2 for outside."""
    return 0 if distance < radius else 1 if distance == radius else 2


def test_fixed_answers_match_an_independent_recalculation():
    plain = {"s1-g4": F(65, 10) - 5, "s2-g1": F(65, 10), "s2-g2": 5 + 5 + 8, "s2-g3": 2, "s2-g5": 18 // 2,
             "s3-g1": 14 // 2, "s3-g2": 2 * 8, "s3-g3": 2 * F(45, 10),
             "s4-g1": 7 - 4, "s4-g2": 2 * PI * 8, "s4-g3": PI * 25, "s4-g5": 7 - 4,
             "p5": F(9) - F(65, 10), "p6": 5 - 2, "p9": F(38, 10), "p10": 7 + 7 + 10, "p11": F(15, 2), "p12": 3, "p13": 3, "p16": 2 * 5,
             "p17": 9, "p18": F(11, 2), "p19": 2 * 12, "p20": 2 * F(65, 10), "p23": 10 // 2, "p24": 20 // 2,
             "p25": 5 + 2, "p26": PI * 49, "p27": 2 * PI * 4, "p28": F(85, 10) - 3, "p29": 8 - 6, "p32": 30 // 2}
    for key, value in plain.items():
        assert BY_ID[key].answer.value == F(value), (key, BY_ID[key].answer.value, value)
    choices = {"s1-g1": position(5, 8), "s1-g2": position(8, 8), "s1-g3": position(11, 8), "s1-g5": 0, "s2-g4": 0, "s3-g4": 0, "s3-g5": 0, "s4-g4": 0,
               "p1": position(6, 10), "p2": position(10, 10), "p3": position(13, 10), "p4": position(F(305, 100), F(35, 10)), "p7": 0, "p8": 0, "p14": 0, "p15": 0,
               "p21": 0, "p22": 0, "p30": 0, "p31": 0}
    for key, index in choices.items():
        assert BY_ID[key].answer.value == index, key
    assert set(plain) | set(choices) == set(BY_ID)


def test_chapter_shape_and_figures():
    assert CER.number == 9 and CER.level == "5e" and len(CER.sections) == 4 and CER.also_for == ("ci",)
    assert len([b for s in CER.sections for b in s.blocks if b["type"] == "figure"]) >= 3


def test_assessment_keys_match_a_recalculation_from_each_prompt():
    for seed in range(300):
        q = {x.id.split("/")[1]: x for x in assessment(random.Random(f"c5{seed}"))}
        assert sorted(q, key=lambda k: int(k[1:])) == [f"a{i}" for i in range(1, 13)]
        for key in ("a1", "a2"):
            r, om = numbers_in(q[key].prompt)[:2]
            assert q[key].answer.value == position(om, r) and om > 0
        r, om = numbers_in(q["a3"].prompt)[1], numbers_in(q["a3"].prompt)[0]
        assert q["a3"].answer.value == om - r > 0
        assert q["a4"].answer.value == numbers_in(q["a4"].prompt)[0]
        oa, ab = numbers_in(q["a5"].prompt)[:2]
        assert q["a5"].answer.value == 2 * oa + ab
        assert q["a6"].answer.value * 2 == numbers_in(q["a6"].prompt)[0]
        assert q["a7"].answer.value * 2 == numbers_in(q["a7"].prompt)[0]
        assert q["a8"].answer.value == 2 * numbers_in(q["a8"].prompt)[0]
        assert q["a9"].answer.value * 2 == numbers_in(q["a9"].prompt)[0]
        assert q["a10"].answer.value == PI * numbers_in(q["a10"].prompt)[0]
        hyp = numbers_in(q["a11"].prompt)[0]
        assert q["a11"].answer.value == PI * (hyp / 2) ** 2
        r, ob = numbers_in(q["a12"].prompt)[:2]
        assert q["a12"].answer.value == (r - ob if "plus petite" in q["a12"].prompt else r + ob)


@pytest.fixture
def student(app, make_user):
    make_user("cisse@example.com", "secret123", "Cisse")
    client = app.test_client()
    client.post("/login", data={"email": "cisse@example.com", "password": "secret123"})
    client.post("/settings/curriculum", data={"curriculum": "sn:5e"})
    return client


def test_pages_render(student):
    for path in ["", "/practice", "/summary", "/assessment?seed=abcd1234", "/s/position", "/s/circonscrit", "/s/rectangle", "/s/problemes"]:
        for headers in ({}, {"Accept-Language": "fr-FR,fr;q=0.9"}):
            assert student.get(f"/curriculum/{CER.id}{path}", headers=headers).status_code == 200, path
    assert student.post("/curriculum/check", json={"exercise": f"{CER.id}/s3-g1", "answer": "7 cm"}).get_json()["status"] == "correct"
