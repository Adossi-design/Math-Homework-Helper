"""Chapter 12 (angles), recomputed independently from the numbers shown in each prompt."""
import random
import re
from fractions import Fraction as F

import pytest

from mathhelper.curriculum.chapters.sn_6e_angles import CHAPTER as ANG, assessment

BY_ID = {e.id.split("/")[1]: e for e in ANG.exercises().values()}


def numbers_in(prompt):
    """Read the whole numbers written in a prompt."""
    return [int(x) for x in re.findall(r"\d+", prompt)]


def smallest_clock_angle(hour):
    """Return the smaller angle between the hands of a clock at a whole hour."""
    return min(30 * hour, 360 - 30 * hour)


def test_fixed_answers_match_an_independent_recalculation():
    plain = {"s1-g2": 5 * 4 // 2, "s1-g5": 6 * 5 // 2,
             "s2-g3": 3 * 90, "s2-g4": 360 // 8,
             "s3-g1": 40 + 55, "s3-g2": 130 - 60, "s3-g3": 180 - 115, "s3-g4": 90 - 37,
             "s4-g1": 84 // 2, "s4-g2": 2 * 33, "s4-g3": smallest_clock_angle(5), "s4-g4": smallest_clock_angle(8), "s4-g5": 180 - 135,
             "p2": 7 * 6 // 2, "p3": 1, "p9": 360 // 2, "p10": 5 * 90, "p11": 360 // 6, "p12": 2 * 360 + 180,
             "p13": 25 + 70, "p14": 150 - 62, "p15": 180 - 73, "p16": 90 - 41, "p17": 180 - 50 - 75, "p18": 90 // 3, "p19": 180 // 4, "p20": 180 // 3,
             "p22": 110 // 2, "p23": 2 * 47, "p24": 90 // 2, "p25": 180 // 2, "p26": smallest_clock_angle(3), "p27": smallest_clock_angle(10), "p28": smallest_clock_angle(6),
             "p29": 360 // 12, "p30": 35 + 50, "p31": 120 - 75}
    for key, value in plain.items():
        assert BY_ID[key].answer.value == F(value), (key, BY_ID[key].answer.value, value)
    choices = {"s1-g1": 1, "s1-g3": 0, "s1-g4": 1, "s2-g1": 0, "s2-g2": 2, "s2-g5": 1, "s3-g5": 0,
               "p1": 1, "p4": 0, "p5": 1, "p6": 0, "p7": 2, "p8": 2, "p21": 1, "p32": 0, "p33": 0}
    for key, index in choices.items():
        assert BY_ID[key].answer.value == index, key
    assert set(plain) | set(choices) == set(BY_ID)


def test_chapter_shape_and_alignment():
    assert ANG.number == 12 and len(ANG.sections) == 4 and ANG.also_for == ("ci",)
    assert "lesson 4 of the C" in ANG.status_note and "not been checked against the official Senegalese" in ANG.status_note
    figures = [b for s in ANG.sections for b in s.blocks if b["type"] == "figure"]
    assert len(figures) >= 6


def test_assessment_keys_match_a_recalculation_from_each_prompt():
    for seed in range(300):
        q = {x.id.split("/")[1]: x for x in assessment(random.Random(f"ang{seed}"))}
        assert sorted(q, key=lambda k: int(k[1:])) == [f"a{i}" for i in range(1, 13)]
        measure = numbers_in(q["a1"].prompt)[0]
        expected = 1 if measure == 90 else 3 if measure == 180 else 0 if measure < 90 else 2
        assert q["a1"].answer.value == expected
        x, y = numbers_in(q["a2"].prompt)[-2:]
        assert q["a2"].answer.value == x + y and x + y < 180
        assert q["a3"].answer.value == 180 - numbers_in(q["a3"].prompt)[0] > 0
        assert q["a4"].answer.value == 90 - numbers_in(q["a4"].prompt)[0] > 0
        assert q["a5"].answer.value == numbers_in(q["a5"].prompt)[-1] // 2 and numbers_in(q["a5"].prompt)[-1] % 2 == 0
        assert q["a6"].answer.value == smallest_clock_angle(numbers_in(q["a6"].prompt)[0])
        n = numbers_in(q["a7"].prompt)[0]
        assert q["a7"].answer.value == n * (n - 1) // 2
        assert q["a8"].answer.value == 90 * numbers_in(q["a8"].prompt)[0]
        total, part = numbers_in(q["a9"].prompt)[-2:]
        assert q["a9"].answer.value == total - part > 0
        options = [int(o.rstrip("°")) for o in q["a10"].options]
        assert [i for i, v in enumerate(options) if 90 < v < 180] == [q["a10"].answer.value]
        assert q["a11"].answer.value == 2 * numbers_in(q["a11"].prompt)[-1]
        k = numbers_in(q["a12"].prompt)[-2] if False else int(re.search(r"est (\d+) fois", q["a12"].prompt).group(1))
        assert q["a12"].answer.value * (k + 1) == 90


@pytest.fixture
def student(app, make_user):
    make_user("ndiaye@example.com", "secret123", "Ndiaye")
    client = app.test_client()
    client.post("/login", data={"email": "ndiaye@example.com", "password": "secret123"})
    client.post("/settings/curriculum", data={"curriculum": "sn:6e"})
    return client


def test_pages_render_and_degree_answers_are_read(student):
    for path in ["", "/practice", "/summary", "/assessment?seed=abcd1234", "/s/angle", "/s/mesure", "/s/calculs", "/s/bissectrice"]:
        for headers in ({}, {"Accept-Language": "fr-FR,fr;q=0.9"}):
            assert student.get(f"/curriculum/{ANG.id}{path}", headers=headers).status_code == 200, path
    for typed in ["270", "270°", "270 °", "270 degrés"]:
        assert student.post("/curriculum/check", json={"exercise": f"{ANG.id}/s2-g3", "answer": typed}).get_json()["status"] == "correct", typed
    assert student.post("/curriculum/check", json={"exercise": f"{ANG.id}/s2-g3", "answer": "180"}).get_json()["status"] == "wrong"
