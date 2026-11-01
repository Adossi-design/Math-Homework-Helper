"""Cinquième chapter 4 (proportionality, speed, flow rate, density), recomputed independently."""
import random
import re
from fractions import Fraction as F

import pytest

from mathhelper.curriculum.chapters.figures import Graph
from mathhelper.curriculum.chapters.sn_5e_proportionnalite import CHAPTER as PRO, assessment

BY_ID = {e.id.split("/")[1]: e for e in PRO.exercises().values()}


def numbers_in(prompt):
    """Read the decimal numbers written in a prompt, comma as the decimal mark."""
    return [F(x.replace(",", ".")) for x in re.findall(r"\d+(?:,\d+)?", prompt)]


def test_fixed_answers_match_an_independent_recalculation():
    plain = {"s1-g3": F(20, 8), "s1-g4": 40 * F(25, 10),
             "s2-g1": 360 // 4, "s2-g2": 60 * F(25, 10), "s2-g3": 180 // 90, "s2-g4": 36 / F(36, 10), "s2-g5": 12 * 2,
             "s3-g1": 600 // 12, "s3-g2": 25 * 8, "s3-g3": F(540, 200), "s3-g4": 9 / F(75, 100),
             "s4-g1": 14 * F(10, 4), "s4-g2": 100 // 50 + 100 // 100, "s4-g3": 400 // (15 + 25), "s4-g5": F(125, 10),
             "p3": F(21, 6), "p4": 15 * F(8, 10), "p5": 20 / F(8, 10), "p7": 330 / F(55, 10), "p8": 18 * F(7, 3), "p9": F(45, 10) / 3, "p10": 800 * 3, "p11": 90 / F(36, 10), "p12": 20 * F(36, 10),
             "p13": 100 // 10, "p14": 10 * F(36, 10), "p15": 120 * F(75, 100), "p16": 15 * 3,
             "p17": 450 // 18, "p18": 40 * 15, "p19": F(90, 12), "p20": 18 // 6, "p21": F(300, 400), "p22": F(78, 10) * 50, "p23": F(45, 10) / F(9, 10), "p24": F(136, 10) * 10,
             "p26": 10 * F(4500, 6), "p27": 30 // 15 + 30 // 10, "p28": F(60, 5), "p29": 900 // (30 + 45), "p30": 600 // (20 - 5), "p32": F(8, 10) * 3000}
    for key, value in plain.items():
        assert BY_ID[key].answer.value == F(value), (key, BY_ID[key].answer.value, value)
    choices = {"s1-g1": 0, "s1-g2": 1, "s1-g5": 0, "s3-g5": 0, "s4-g4": 0, "p1": 0, "p2": 1, "p6": 0, "p25": 0, "p31": 0}
    for key, index in choices.items():
        assert BY_ID[key].answer.value == index, key
    assert F(90, 15) / 10 > F(100, 2) / 100 and F(90) / F(15, 10) > F(100) / 2 and F(120) / 2 > F(150) / 3
    assert set(plain) | set(choices) == set(BY_ID)


def test_chapter_shape_and_figures():
    assert PRO.number == 4 and PRO.level == "5e" and len(PRO.sections) == 4 and PRO.also_for == ("ci",)
    assert len([b for s in PRO.sections for b in s.blocks if b["type"] == "figure"]) >= 3
    graph = Graph(30, 45, 5, 15, "a<b", "c&d").line(0, 0, 30, 45).point(10, 15, "<A>")
    svg = graph.svg()
    assert svg.startswith("<svg") and svg.endswith("</svg>") and "<script" not in svg and "&lt;A&gt;" in svg and "a&lt;b" in svg and "c&amp;d" in svg
    assert graph.px(0) < graph.px(30) and graph.py(0) > graph.py(45)


def test_assessment_keys_match_a_recalculation_from_each_prompt():
    for seed in range(300):
        q = {x.id.split("/")[1]: x for x in assessment(random.Random(f"p5{seed}"))}
        assert sorted(q, key=lambda k: int(k[1:])) == [f"a{i}" for i in range(1, 13)]
        pairs = [(int(a), int(b)) for a, b in re.findall(r"(\d+) → (\d+)", q["a1"].prompt)]
        assert q["a1"].answer.value == (0 if len({F(y, x) for x, y in pairs}) == 1 else 1)
        x, y = numbers_in(q["a2"].prompt)[:2]
        assert q["a2"].answer.value == y / x
        d_, t = numbers_in(q["a3"].prompt)[:2]
        assert q["a3"].answer.value == d_ / t
        v, t = numbers_in(q["a4"].prompt)[:2]
        assert q["a4"].answer.value == v * t
        v, d_ = numbers_in(q["a5"].prompt)[:2]
        assert q["a5"].answer.value == d_ / v
        kmh = numbers_in(q["a6"].prompt)[0]
        assert q["a6"].answer.value == kmh / F(36, 10) and q["a6"].answer.value.denominator == 1
        volume, t = numbers_in(q["a7"].prompt)[:2]
        assert q["a7"].answer.value == volume / t
        qq, t = numbers_in(q["a8"].prompt)[:2]
        assert q["a8"].answer.value == qq * t
        vol, mass = numbers_in(q["a9"].prompt)[:2]
        assert q["a9"].answer.value == mass / vol
        rho, volume = numbers_in(q["a10"].prompt)[:2]
        assert q["a10"].answer.value == rho * volume
        a, b, volume = numbers_in(q["a11"].prompt)[:3]
        assert q["a11"].answer.value == volume / (a + b) and q["a11"].answer.value.denominator == 1
        distance, v1, v2 = numbers_in(q["a12"].prompt)[:3]
        assert q["a12"].answer.value == 2 * distance / (distance / v1 + distance / v2)


@pytest.fixture
def student(app, make_user):
    make_user("sy@example.com", "secret123", "Sy")
    client = app.test_client()
    client.post("/login", data={"email": "sy@example.com", "password": "secret123"})
    client.post("/settings/curriculum", data={"curriculum": "sn:5e"})
    return client


def test_pages_render_with_graphs_and_units_are_read(student):
    for path in ["", "/practice", "/summary", "/assessment?seed=abcd1234", "/s/reconnaitre", "/s/vitesse", "/s/debit", "/s/problemes"]:
        for headers in ({}, {"Accept-Language": "fr-FR,fr;q=0.9"}):
            assert student.get(f"/curriculum/{PRO.id}{path}", headers=headers).status_code == 200, path
    assert student.get(f"/curriculum/{PRO.id}/s/reconnaitre").get_data(as_text=True).count('<svg class="fig"') == 2
    for typed in ["90", "90 km/h", "90km/h"]:
        assert student.post("/curriculum/check", json={"exercise": f"{PRO.id}/s2-g1", "answer": typed}).get_json()["status"] == "correct", typed
    for typed in ["2,7", "2,7 g/cm3", "2,7 g/cm³"]:
        assert student.post("/curriculum/check", json={"exercise": f"{PRO.id}/s3-g3", "answer": typed}).get_json()["status"] == "correct", typed
