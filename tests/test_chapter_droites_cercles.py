"""Chapter 11 (lines, segments, circles and discs), recomputed independently from the numbers shown in each prompt, and its figures."""
import random
import re
from fractions import Fraction as F

import pytest

from mathhelper.curriculum.chapters.figures import Figure, figure
from mathhelper.curriculum.chapters.sn_6e_droites_cercles import CHAPTER as GEO, assessment

BY_ID = {e.id.split("/")[1]: e for e in GEO.exercises().values()}
PI = F(314, 100)


def numbers_in(prompt):
    """Read the decimal numbers written in a prompt, comma as the decimal mark."""
    return [F(x.replace(",", ".")) for x in re.findall(r"\d+(?:,\d+)?", prompt)]


def test_fixed_answers_match_an_independent_recalculation():
    plain = {"s1-g1": 1, "s1-g2": 5 * 4 // 2, "s1-g3": F(115, 10), "s1-g4": 12 - 5,
             "s2-g3": 5 * 4 // 2,
             "s3-g1": 14, "s3-g2": 2 * PI * 3, "s3-g3": PI * 16, "s4-g1": 7, "s4-g2": F(64, 10), "s4-g3": 5, "s4-g4": 6 * F(15, 10),
             "p1": 1, "p2": 4 * 3 // 2, "p3": 6 * 5 // 2, "p4": F(85, 10) + F(63, 10), "p5": 15 - 6, "p6": F(28, 10) + 5,
             "p12": 6 * 5 // 2, "p13": 0, "p16": 9, "p17": PI * 10, "p18": 2 * PI * 7, "p19": PI * 100, "p20": PI * 36, "p21": F(628, 10) / PI, "p22": F(3768, 100) / PI / 2,
             "p26": PI * 4, "p27": 2 * PI * 30, "p28": F(7, 2), "p29": 2 * F(48, 10), "p30": 4 * F(25, 10), "p31": 8 * F(125, 100)}
    for key, value in plain.items():
        assert BY_ID[key].answer.value == F(value), (key, BY_ID[key].answer.value, value)
    choices = {"s1-g5": 2, "s2-g1": 0, "s2-g2": 1, "s2-g4": 1, "s2-g5": 1, "s3-g4": 0, "s3-g5": 0, "s4-g5": 1,
               "p7": 1, "p8": 1, "p9": 0, "p10": 0, "p11": 1, "p14": 0, "p15": 1, "p23": 1, "p24": 2, "p25": 0, "p32": 0, "p33": 0}
    for key, index in choices.items():
        assert BY_ID[key].answer.value == index, key
    assert set(plain) | set(choices) == set(BY_ID)


def test_chapter_shape_and_alignment():
    assert GEO.number == 11 and len(GEO.sections) == 4 and GEO.also_for == ("ci",)
    assert "lessons 1 to 3 of the C" in GEO.status_note and "not been checked against the official Senegalese" in GEO.status_note
    figures = [b for s in GEO.sections for b in s.blocks if b["type"] == "figure"]
    assert len(figures) >= 8 and all(b["alt"] and b["caption"] and b["svg"].startswith("<svg") for b in figures)


def test_assessment_keys_match_a_recalculation_from_each_prompt():
    for seed in range(300):
        q = {x.id.split("/")[1]: x for x in assessment(random.Random(f"geo{seed}"))}
        assert sorted(q, key=lambda k: int(k[1:])) == [f"a{i}" for i in range(1, 13)]
        x, y = numbers_in(q["a1"].prompt)[:2]
        assert q["a1"].answer.value == x + y
        total, ab = numbers_in(q["a2"].prompt)[:2]
        assert q["a2"].answer.value == total - ab > 0
        n = int(numbers_in(q["a3"].prompt)[0])
        assert q["a3"].answer.value == n * (n - 1) // 2
        assert q["a4"].options[q["a4"].answer.value] in ("Elles sont parallèles", "Elles sont perpendiculaires")
        assert ("perpendiculaires" if "// (d₂)" in q["a4"].prompt else "parallèles") in q["a4"].options[q["a4"].answer.value]
        n = int(numbers_in(q["a5"].prompt)[0])
        assert q["a5"].answer.value == n * (n - 1) // 2
        assert q["a6"].answer.value == PI * numbers_in(q["a6"].prompt)[0]
        radius = numbers_in(q["a7"].prompt)[0]
        assert q["a7"].answer.value == PI * radius * radius
        perimeter = numbers_in(q["a8"].prompt)[0]
        assert q["a8"].answer.value * 2 * PI == perimeter
        radius, distance = numbers_in(q["a9"].prompt)[:2]
        expected = 0 if distance == radius else 1 if distance < radius else 2
        assert q["a9"].answer.value == expected
        assert q["a10"].answer.value * 2 == numbers_in(q["a10"].prompt)[0]
        assert q["a11"].answer.value == 2 * numbers_in(q["a11"].prompt)[0]
        assert q["a12"].answer.value * 4 == numbers_in(q["a12"].prompt)[0]


def test_figures_are_valid_svg_and_never_contain_scripts():
    fig = Figure().point("A", 40, 100).point("B", 200, 80).line("A", "B").ray("B", "A").segment("A", "B").circle("A", 30).right_angle("A", "B", "B").tick("A", "B", 2).arrow_mark("A", "B", 2)
    block = figure(fig, "Un dessin <test> & \"autre\"", "Légende")
    assert block["svg"].count("<svg") == 1 and block["svg"].endswith("</svg>") and "<script" not in block["svg"] and "aria-hidden" in block["svg"]
    assert block["alt"] == "Un dessin <test> & \"autre\""
    dangerous = Figure().point("<script>", 10, 10)
    assert "<script>" not in dangerous.svg() and "&lt;script&gt;" in dangerous.svg()


@pytest.fixture
def student(app, make_user):
    make_user("fall@example.com", "secret123", "Fall")
    client = app.test_client()
    client.post("/login", data={"email": "fall@example.com", "password": "secret123"})
    client.post("/settings/curriculum", data={"curriculum": "sn:6e"})
    return client


def test_pages_render_with_their_figures_in_both_languages(student):
    for path in ["", "/practice", "/summary", "/assessment?seed=abcd1234", "/s/points", "/s/paralleles", "/s/cercles", "/s/milieu"]:
        for headers in ({}, {"Accept-Language": "fr-FR,fr;q=0.9"}):
            assert student.get(f"/curriculum/{GEO.id}{path}", headers=headers).status_code == 200, path
    page = student.get(f"/curriculum/{GEO.id}/s/cercles").get_data(as_text=True)
    assert page.count('<svg class="fig"') == 2 and 'class="fig-box"' in page and "&lt;svg" not in page
    assert student.post("/curriculum/check", json={"exercise": f"{GEO.id}/s1-g1", "answer": "1 droite"}).get_json()["status"] == "correct"
    assert student.post("/curriculum/check", json={"exercise": f"{GEO.id}/s3-g1", "answer": "14 cm"}).get_json()["status"] == "correct"
