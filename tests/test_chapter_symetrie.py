"""Chapter 15 (central symmetry), recomputed independently from the numbers shown in each prompt."""
import random
import re
from fractions import Fraction as F

import pytest

from mathhelper.curriculum.chapters.sn_6e_symetrie import CHAPTER as SYM, assessment

BY_ID = {e.id.split("/")[1]: e for e in SYM.exercises().values()}


def numbers_in(prompt):
    """Read the numbers written in a prompt, comma as the decimal mark, with an optional minus sign."""
    return [F(x.replace(",", ".").replace("−", "-")) for x in re.findall(r"[−-]?\d+(?:,\d+)?", prompt)]


def symmetric(o, a):
    """Return the symmetric of the point a through the point o."""
    return [2 * o[0] - a[0], 2 * o[1] - a[1]]


def test_fixed_answers_match_an_independent_recalculation():
    plain = {"s1-g1": 7, "s1-g2": 2 * F(55, 10), "s1-g3": 18 // 2, "s2-g1": 9, "s2-g2": 62, "s2-g3": F(45, 10), "s2-g5": 24,
             "s3-g1": 20 // 2, "s3-g2": 16 // 2, "s3-g3": 2 * 7, "s4-g1": 2 * 5 + 2 * 3, "s4-g4": 12 * 7, "s4-g5": 30 // 2,
             "p1": 12, "p2": 2 * F(85, 10), "p3": F(25, 2), "p11": F(38, 10), "p12": 113, "p13": 9 + 12 + 15, "p14": 10 // 2, "p17": 36, "p18": 4 + 5,
             "p19": 18 // 2, "p20": 2 * F(46, 10), "p21": F(15, 2), "p22": 20, "p26": 2 * F(35, 10) + 2 * F(25, 10), "p29": 2 * (9 + 6), "p30": 24 // 2, "p32": (6 + 10) + 2 * 6}
    for key, value in plain.items():
        assert BY_ID[key].answer.value == F(value), (key, BY_ID[key].answer.value, value)
    lists = {"s1-g4": symmetric((1, 2), (4, 6)), "s1-g5": [F(7 + 3, 2), F(1 + 5, 2)], "s4-g2": symmetric((3, 4), (8, 1)), "s4-g3": [F(9 + 3, 2), F(2 + 8, 2)],
             "p4": symmetric((0, 0), (3, 5)), "p5": symmetric((2, 2), (6, 3)), "p6": symmetric((5, 4), (1, 7)), "p7": [F(2 + 10, 2), F(8 + 4, 2)], "p8": [F(-3 + 5, 2), F(2 - 4, 2)],
             "p27": symmetric((4, 1), (9, 6)), "p28": [F(0 + 8, 2), F(0 + 6, 2)]}
    for key, value in lists.items():
        assert list(BY_ID[key].answer.value) == [F(v) for v in value], key
    choices = {"s2-g4": 0, "s3-g4": 2, "s3-g5": 1, "p9": 0, "p10": 1, "p15": 0, "p16": 1, "p23": 1, "p24": 0, "p25": 1, "p31": 1}
    for key, index in choices.items():
        assert BY_ID[key].answer.value == index, key
    assert set(plain) | set(lists) | set(choices) == set(BY_ID)


def test_chapter_shape_and_alignment():
    assert SYM.number == 15 and len(SYM.sections) == 4 and SYM.also_for == ("ci",)
    assert "lesson 7 of the C" in SYM.status_note and "not been checked against the official Senegalese" in SYM.status_note
    assert len([b for s in SYM.sections for b in s.blocks if b["type"] == "figure"]) >= 4


def test_assessment_keys_match_a_recalculation_from_each_prompt():
    for seed in range(300):
        q = {x.id.split("/")[1]: x for x in assessment(random.Random(f"sym{seed}"))}
        assert sorted(q, key=lambda k: int(k[1:])) == [f"a{i}" for i in range(1, 13)]
        a, b, x, y = [int(n) for n in re.findall(r"\d+", q["a1"].prompt)[:4]]
        assert list(q["a1"].answer.value) == [F(2 * a - x), F(2 * b - y)]
        assert q["a2"].answer.value == 2 * numbers_in(q["a2"].prompt)[0]
        assert q["a3"].answer.value * 2 == numbers_in(q["a3"].prompt)[0]
        assert q["a4"].answer.value == numbers_in(q["a4"].prompt)[0]
        assert q["a5"].answer.value == numbers_in(q["a5"].prompt)[0]
        assert q["a6"].answer.value * 2 == numbers_in(q["a6"].prompt)[0]
        assert q["a7"].answer.value == sum(numbers_in(q["a7"].prompt)[:3])
        u, v = numbers_in(q["a8"].prompt)[:2]
        assert q["a8"].answer.value == u * v
        assert q["a9"].options[q["a9"].answer.value] in ("Un parallélogramme", "Un cercle", "Un segment")
        assert sum(1 for o in q["a9"].options if o.startswith("Un triangle")) == 2
        x, y, xp, yp = [int(n) for n in re.findall(r"-?\d+", q["a10"].prompt)[:4]]
        assert list(q["a10"].answer.value) == [F(x + xp, 2), F(y + yp, 2)]
        oa, ob = numbers_in(q["a11"].prompt)[:2]
        assert q["a11"].answer.value == 2 * (oa + ob)
        assert q["a12"].answer.value * 2 == numbers_in(q["a12"].prompt)[0]


@pytest.fixture
def student(app, make_user):
    make_user("ba@example.com", "secret123", "Ba")
    client = app.test_client()
    client.post("/login", data={"email": "ba@example.com", "password": "secret123"})
    client.post("/settings/curriculum", data={"curriculum": "sn:6e"})
    return client


def test_pages_render_and_coordinate_answers_are_read(student):
    for path in ["", "/practice", "/summary", "/assessment?seed=abcd1234", "/s/point", "/s/figures", "/s/centre", "/s/problemes"]:
        for headers in ({}, {"Accept-Language": "fr-FR,fr;q=0.9"}):
            assert student.get(f"/curriculum/{SYM.id}{path}", headers=headers).status_code == 200, path
    for typed in ["-2 ; -2", "(-2 ; -2)", "−2 ; −2", "-2;-2"]:
        assert student.post("/curriculum/check", json={"exercise": f"{SYM.id}/s1-g4", "answer": typed}).get_json()["status"] == "correct", typed
    assert student.post("/curriculum/check", json={"exercise": f"{SYM.id}/s1-g4", "answer": "-2 ; 2"}).get_json()["status"] == "wrong"
