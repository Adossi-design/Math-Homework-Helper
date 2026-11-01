"""Cinquième chapter 12 (axial symmetry), recomputed independently."""
import random
import re
from fractions import Fraction as F

import pytest

from mathhelper.curriculum.chapters.sn_5e_symetrie_axiale import CHAPTER as SYM, assessment

BY_ID = {e.id.split("/")[1]: e for e in SYM.exercises().values()}


def ints_in(prompt):
    """Read the signed whole numbers of a prompt."""
    return [int(x.replace("−", "-")) for x in re.findall(r"[−-]?\d+", prompt)]


def test_fixed_answers_match_an_independent_recalculation():
    plain = {"s1-g1": 2 * 6, "s1-g2": F(9, 2), "s1-g3": F(17, 2), "s1-g4": 90,
             "s2-g1": F(15, 2), "s2-g2": 48, "s2-g3": 36, "s2-g4": 4,
             "s3-g1": 4, "s3-g2": 1, "s3-g3": 2, "s3-g4": 50,
             "s4-g1": 2 * 5 - 9, "s4-g2": (-4 + 8) // 2, "s4-g3": 18 // 2, "s4-g4": 2 * 7,
             "p1": 7, "p2": F(11, 2), "p3": 12, "p4": 90, "p5": 5, "p6": 2 + 5,
             "p8": 27, "p9": 125, "p10": 9 * 4, "p11": 10 // 2, "p12": 4, "p13": 15,
             "p16": 3, "p17": 2, "p18": 2, "p19": 1, "p20": 4, "p21": (180 - 80) // 2, "p22": 180 - 2 * 70,
             "p25": 2 * 4 - 11, "p26": 2 * -2 - 1, "p27": (3 + 15) // 2, "p28": 12 // 2, "p29": 2 * F(13, 2), "p30": 5, "p31": (34 - 10) // 2, "p32": 5 + 5 + 6}
    for key, value in plain.items():
        assert BY_ID[key].answer.value == F(value), (key, BY_ID[key].answer.value, value)
    choices = {"s1-g5": 0, "s2-g5": 0, "s3-g5": 0, "p7": 0, "p14": 0, "p15": 0, "p23": 0, "p24": 0}
    for key, index in choices.items():
        assert BY_ID[key].answer.value == index, key
    assert set(plain) | set(choices) == set(BY_ID)


def test_chapter_shape_and_figures():
    assert SYM.number == 12 and SYM.level == "5e" and len(SYM.sections) == 4 and SYM.also_for == ("ci",)
    assert len([b for s in SYM.sections for b in s.blocks if b["type"] == "figure"]) >= 2


def test_assessment_keys_match_a_recalculation_from_each_prompt():
    axes = {"un carré": 4, "un rectangle qui n'est pas un carré": 2, "un losange qui n'est pas un carré": 2, "un triangle équilatéral": 3, "un triangle isocèle qui n'est pas équilatéral": 1}
    for seed in range(300):
        q = {x.id.split("/")[1]: x for x in assessment(random.Random(f"sym{seed}"))}
        assert sorted(q, key=lambda k: int(k[1:])) == [f"a{i}" for i in range(1, 13)]
        assert q["a1"].answer.value == 2 * ints_in(q["a1"].prompt)[0]
        assert q["a2"].answer.value * 2 == ints_in(q["a2"].prompt)[0]
        assert q["a3"].answer.value == ints_in(q["a3"].prompt)[0]
        assert q["a4"].answer.value == ints_in(q["a4"].prompt)[0]
        assert q["a5"].answer.value == sum(ints_in(q["a5"].prompt)[:3])
        a, b = ints_in(q["a6"].prompt)[:2]
        assert q["a6"].answer.value == a * b
        assert q["a7"].answer.value == ints_in(q["a7"].prompt)[0]
        name = max((k for k in axes if k in q["a8"].prompt), key=len)
        assert q["a8"].answer.value == axes[name]
        k, x = ints_in(q["a9"].prompt)[:2]
        assert q["a9"].answer.value == 2 * k - x
        assert q["a10"].answer.value == 2 * ints_in(q["a10"].prompt)[0]
        apex = ints_in(q["a11"].prompt)[0]
        assert q["a11"].answer.value == F(180 - apex, 2)
        a, b = ints_in(q["a12"].prompt)[:2]
        assert (a + b) % 2 == 0 and q["a12"].answer.value == F(a + b, 2)


@pytest.fixture
def student(app, make_user):
    make_user("sy@example.com", "secret123", "Sy")
    client = app.test_client()
    client.post("/login", data={"email": "sy@example.com", "password": "secret123"})
    client.post("/settings/curriculum", data={"curriculum": "sn:5e"})
    return client


def test_pages_render(student):
    for path in ["", "/practice", "/summary", "/assessment?seed=abcd1234", "/s/point", "/s/figures", "/s/axes", "/s/problemes"]:
        for headers in ({}, {"Accept-Language": "fr-FR,fr;q=0.9"}):
            assert student.get(f"/curriculum/{SYM.id}{path}", headers=headers).status_code == 200, path
    assert student.post("/curriculum/check", json={"exercise": f"{SYM.id}/s1-g1", "answer": "12 cm"}).get_json()["status"] == "correct"
