"""Cinquième chapter 5 (statistics), recomputed independently."""
import random
import re
from fractions import Fraction as F

import pytest

from mathhelper.curriculum.chapters.sn_5e_statistique import CHAPTER as STA, assessment

BY_ID = {e.id.split("/")[1]: e for e in STA.exercises().values()}


def ints_in(prompt):
    """Read the whole numbers of a prompt."""
    return [int(x) for x in re.findall(r"\d+", prompt)]


def mean(values, efforts):
    """Return the exact mean of a series from its values and counts."""
    return F(sum(v * e for v, e in zip(values, efforts)), sum(efforts))


def test_fixed_answers_match_an_independent_recalculation():
    plain = {"s1-g4": 7 + 12 + 9 + 12, "s1-g5": 100 * F(8, 40),
             "s2-g1": 12 + 8 + 5 + 15, "s2-g2": 7 * 4, "s2-g3": 36 // 4, "s2-g4": 80 * F(35, 100), "s2-g5": 100 - 30 - 25 - 20,
             "s3-g1": 3 + 6 + 8 + 3, "s3-g2": 100 * F(5, 25), "s3-g3": 4 + 2, "s3-g4": mean([10, 12, 16], [2, 3, 5]),
             "s4-g1": 60 * F(100 - 25 - 40 - 15, 100), "s4-g3": F(6 + 8 + 8 + 10 + 13, 5), "s4-g4": 150 * F(36, 100), "s4-g5": 60 - 15 - 25,
             "p4": 5, "p5": 11 + 6 + 8 + 15, "p6": 100 * F(15, 50), "p7": 80 * F(35, 100), "p8": F(18) / F(45, 100),
             "p9": 9 + 14 + 6 + 11, "p10": 9 * 3, "p11": 45 // 5, "p12": 100 - 20 - 35 - 15, "p13": 120 * F(45, 100), "p14": 160 * F(25, 100),
             "p17": 4 + 6 + 8 + 2, "p18": 6 + 8 + 2, "p19": 100 * F(8, 20), "p20": mean([7, 10, 13, 16], [4, 6, 8, 2]), "p21": mean([150, 155, 160], [3, 5, 2]),
             "p22": 2 + 5 + 7 + 4 + 2, "p23": mean([0, 1, 2, 3, 4], [2, 5, 7, 4, 2]), "p24": 2,
             "p26": 80 * F(100 - 20 - 35 - 25, 100), "p27": max(100 * F(9, 30), 100 * F(12, 50)), "p28": 250 * F(36, 100), "p29": F(4 + 6 + 6 + 8 + 9 + 9 + 9 + 13, 8), "p30": 18 // 6, "p32": 40 - 8 - 12 - 12}
    for key, value in plain.items():
        assert BY_ID[key].answer.value == F(value), (key, BY_ID[key].answer.value, value)
    choices = {"s1-g1": 0, "s1-g2": 1, "s1-g3": 0, "s3-g5": 0, "s4-g2": 0, "p1": 0, "p2": 1, "p3": 0, "p15": 0, "p16": 0, "p25": 0, "p31": 0}
    for key, index in choices.items():
        assert BY_ID[key].answer.value == index, key
    assert F(12, 30) == F(14, 35) == F(4, 10)
    assert set(plain) | set(choices) == set(BY_ID)


def test_chapter_shape_and_diagrams():
    assert STA.number == 5 and STA.level == "5e" and len(STA.sections) == 4 and STA.also_for == ("ci",)
    figures = [b for s in STA.sections for b in s.blocks if b["type"] == "figure"]
    assert len(figures) >= 3 and all("<rect" in b["svg"] or "fig-stick" in b["svg"] for b in figures)


def test_assessment_keys_match_a_recalculation_from_each_prompt():
    for seed in range(300):
        q = {x.id.split("/")[1]: x for x in assessment(random.Random(f"s5{seed}"))}
        assert sorted(q, key=lambda k: int(k[1:])) == [f"a{i}" for i in range(1, 13)]
        qualitative = any(word in q["a1"].prompt for word in ("couleur", "transport", "sport", "ville"))
        assert q["a1"].answer.value == (0 if qualitative else 1)
        assert q["a2"].answer.value == sum(ints_in(q["a2"].prompt.split(". Quel")[0]))
        total, count = ints_in(q["a3"].prompt)[:2]
        assert q["a3"].answer.value == F(count * 100, total) and F(count * 100, total).denominator == 1
        assert q["a4"].answer.value == sum(ints_in(q["a4"].prompt.split(" élèves.")[0])[0:4])
        scale, squares = ints_in(q["a5"].prompt)[1:3]
        assert q["a5"].answer.value == scale * squares
        number_, scale = (lambda v: (v[0], v[2]))(ints_in(q["a6"].prompt))
        assert q["a6"].answer.value * scale == number_
        total, percent = ints_in(q["a7"].prompt)[:2]
        assert q["a7"].answer.value == F(total * percent, 100) and F(total * percent, 100).denominator == 1
        parts = ints_in(q["a8"].prompt)[:3]
        assert q["a8"].answer.value == 100 - sum(parts) > 0
        pairs = [(int(v), int(e)) for v, e in re.findall(r"(\d+) \((\d+) élèves\)", q["a9"].prompt)]
        threshold = int(re.search(r"au moins (\d+)", q["a9"].prompt).group(1))
        assert q["a9"].answer.value == sum(e for v, e in pairs if v >= threshold)
        pairs = [(int(v), int(e)) for v, e in re.findall(r"(\d+) \((\d+) élèves\)", q["a10"].prompt)]
        assert q["a10"].answer.value == mean([v for v, _ in pairs], [e for _, e in pairs])
        assert q["a10"].answer.value.denominator in (1, 2, 4, 5, 8, 10, 20, 25, 40, 50)
        a, b, total = ints_in(q["a11"].prompt)[:3]
        assert q["a11"].answer.value == total - a - b > 0
        a_count, a_total, b_count, b_total = ints_in(q["a12"].prompt)[:4]
        assert q["a12"].answer.value == (0 if F(a_count, a_total) > F(b_count, b_total) else 1)


@pytest.fixture
def student(app, make_user):
    make_user("sarr@example.com", "secret123", "Sarr")
    client = app.test_client()
    client.post("/login", data={"email": "sarr@example.com", "password": "secret123"})
    client.post("/settings/curriculum", data={"curriculum": "sn:5e"})
    return client


def test_pages_render_with_diagrams(student):
    for path in ["", "/practice", "/summary", "/assessment?seed=abcd1234", "/s/vocabulaire", "/s/bandes", "/s/batons", "/s/problemes"]:
        for headers in ({}, {"Accept-Language": "fr-FR,fr;q=0.9"}):
            assert student.get(f"/curriculum/{STA.id}{path}", headers=headers).status_code == 200, path
    assert student.get(f"/curriculum/{STA.id}/s/bandes").get_data(as_text=True).count('<svg class="fig"') == 2
    assert student.post("/curriculum/check", json={"exercise": f"{STA.id}/s1-g5", "answer": "20 %"}).get_json()["status"] == "correct"
