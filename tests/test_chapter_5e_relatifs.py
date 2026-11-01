"""Cinquième chapter 2 (relative decimal numbers), recomputed independently."""
import random
import re
from fractions import Fraction as F

import pytest

from mathhelper.curriculum.chapters.sn_5e_relatifs import CHAPTER as REL, assessment

BY_ID = {e.id.split("/")[1]: e for e in REL.exercises().values()}


def num(text):
    """Read a decimal number written with a comma, an optional minus sign and optional braces."""
    return F(text.replace("{,}", ".").replace(",", ".").replace("−", "-"))


def signed_numbers(prompt):
    """Return every number of a prompt, with its minus sign when it has one."""
    return [num(x) for x in re.findall(r"-?\d+(?:\{,\}\d+|,\d+)?", prompt)]


def test_fixed_answers_match_an_independent_recalculation():
    plain = {"s1-g1": 5 - 9, "s1-g2": -6 + 2, "s1-g3": F(-15, 10) - 2, "s1-g4": 12 + 7,
             "s2-g1": 6 - 9 + 4, "s2-g2": -3 - 5 + 8, "s2-g3": F(-25, 10) + F(175, 100) - F(25, 100), "s2-g4": 12 - 7 - 6,
             "s3-g1": -6 * 3, "s3-g2": -4 * -5, "s3-g3": F(-25, 10) * -4, "s3-g4": (-1) ** 5,
             "s4-g1": 1 - 3, "s4-g2": -9 + 5, "s4-g3": 2 + F(15, 10), "s4-g4": -3 + 8, "s4-g5": -7,
             "p1": 9 - 14, "p2": -3 - 8, "p3": -7 + 12, "p4": F(45, 10) + F(15, 10), "p5": F(-8, 10) + F(23, 10), "p6": 15 + 4, "p7": 25 + 18,
             "p11": 5 - 12 + 4, "p12": -8 + 3 - 2 + 10, "p13": -4 + 9 + 3, "p14": 6 - 8 + 5 - 2, "p15": F(-32, 10) + F(57, 10) - F(15, 10), "p16": F(24, 10) - F(39, 10) + F(5, 10),
             "p17": 5000 - 2500 - 1800 + 700, "p18": -1 + 6 - 4 + 3,
             "p20": -7 * 6, "p21": -8 * -9, "p22": F(5, 10) * -12, "p23": F(-15, 10) * F(-15, 10), "p24": -2 * -3 * -4, "p25": -5 * -2 * 3 * -1, "p26": 0, "p27": 4 * F(-35, 10),
             "p30": 3 - 8, "p31": 10 + 3, "p32": -6 + 4, "p33": 1 - F(25, 10), "p34": 5 - 3, "p35": -3 + 9, "p36": -4 + 15}
    for key, value in plain.items():
        assert BY_ID[key].answer.value == F(value), (key, BY_ID[key].answer.value, value)
    lists = {"s1-g5": sorted([F(-2), F(15, 10), F(-25, 10), F(0)]), "p8": sorted([F(5, 10), F(-1), F(-12, 10), F(1), F(-1, 10)]),
             "p9": sorted([F(-4), F(35, 10), F(-35, 10), F(0)], reverse=True)}
    for key, value in lists.items():
        assert list(BY_ID[key].answer.value) == value, key
    choices = {"s2-g5": 0, "s3-g5": 1, "p10": 2, "p19": 0, "p28": 0, "p29": 0}
    for key, index in choices.items():
        assert BY_ID[key].answer.value == index, key
    assert 5 - (-3) + (-2) == 6 and (-3) + (-4) == -7 and (-3) * (-4) == 12
    assert set(plain) | set(lists) | set(choices) == set(BY_ID)


def test_chapter_shape_and_alignment():
    assert REL.number == 2 and REL.level == "5e" and len(REL.sections) == 4 and REL.also_for == ("ci",)
    assert "lesson 2 of the C" in REL.status_note and "not been checked against the official Senegalese" in REL.status_note


def test_assessment_keys_match_a_recalculation_from_each_prompt():
    for seed in range(300):
        q = {x.id.split("/")[1]: x for x in assessment(random.Random(f"r5{seed}"))}
        assert sorted(q, key=lambda k: int(k[1:])) == [f"a{i}" for i in range(1, 13)]
        a, b = signed_numbers(q["a1"].prompt)[:2]
        assert q["a1"].answer.value == a - b
        a, b = signed_numbers(q["a2"].prompt)[:2]
        assert q["a2"].answer.value == a - b
        high, low = [int(x) for x in re.findall(r"-?\d+", q["a3"].prompt)[:2]]
        assert q["a3"].answer.value == high - low and high > low
        prompt = q["a4"].prompt.strip("$")
        terms = [int(t.replace(" ", "")) for t in re.findall(r"[-+]?\s*\d+", prompt)]
        assert len(terms) == 4 and q["a4"].answer.value == sum(terms)
        a, b, c = signed_numbers(q["a5"].prompt)[:3]
        assert q["a5"].answer.value == a + b - c
        amounts = [int(x) for x in re.findall(r"[+-]\d+", q["a6"].prompt)]
        assert len(amounts) == 4 and q["a6"].answer.value == sum(amounts)
        a, b = signed_numbers(q["a7"].prompt)[:2]
        assert q["a7"].answer.value == a * b
        a, b = signed_numbers(q["a8"].prompt)[:2]
        assert q["a8"].answer.value == a * b
        factors = signed_numbers(q["a9"].prompt)
        negatives = sum(1 for f in factors if f < 0)
        assert q["a9"].answer.value == (0 if negatives % 2 == 0 else 1)
        match = re.search(r"x ([+-]) (-?[\d{,}]+) = (-?[\d{,}]+)", q["a10"].prompt)
        sign, b, a = match.group(1), num(match.group(2)), num(match.group(3))
        b = b if sign == "+" else -b
        assert q["a10"].answer.value == a - b and q["a10"].answer.value + b == a
        match = re.search(r"x ([+-]) ([\d{,}]+) = (-?[\d{,}]+)", q["a11"].prompt)
        sign, b, a = match.group(1), num(match.group(2)), num(match.group(3))
        b = b if sign == "+" else -b
        assert q["a11"].answer.value + b == a
        drop, now = [int(x) for x in re.findall(r"-?\d+", q["a12"].prompt)[:2]]
        assert q["a12"].answer.value - drop == now


@pytest.fixture
def student(app, make_user):
    make_user("kone@example.com", "secret123", "Kone")
    client = app.test_client()
    client.post("/login", data={"email": "kone@example.com", "password": "secret123"})
    client.post("/settings/curriculum", data={"curriculum": "sn:5e"})
    return client


def test_pages_render_and_negative_answers_are_read(student):
    hub = student.get("/curriculum/").get_data(as_text=True)
    assert hub.count("chapter-card") >= 2
    for path in ["", "/practice", "/summary", "/assessment?seed=abcd1234", "/s/difference", "/s/somme", "/s/produit", "/s/equation"]:
        for headers in ({}, {"Accept-Language": "fr-FR,fr;q=0.9"}):
            assert student.get(f"/curriculum/{REL.id}{path}", headers=headers).status_code == 200, path
    for typed in ["-4", "−4", "(-4)", "-4,0"]:
        assert student.post("/curriculum/check", json={"exercise": f"{REL.id}/s1-g1", "answer": typed}).get_json()["status"] == "correct", typed
    assert student.post("/curriculum/check", json={"exercise": f"{REL.id}/s1-g1", "answer": "4"}).get_json()["status"] == "wrong"
