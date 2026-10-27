"""Chapter 7 (relative numbers), recalculated independently."""
import random
import re
from fractions import Fraction as F

import pytest

from mathhelper.curriculum import checker
from mathhelper.curriculum.chapters.kit import d
from mathhelper.curriculum.chapters.sn_6e_relatifs import CHAPTER as REL, assessment
from tests.test_chapters import evaluate

INDEPENDENT = {
    "s1-g1": 7, "s1-g2": F(-45, 10), "s1-g3": -3, "s1-g4": 1, "s1-g5": -3,
    "s2-g1": 0, "s2-g3": -3, "s2-g5": -6,
    "s3-g1": -5 - 2, "s3-g2": -(9 - 4), "s3-g3": 6 - 10, "s3-g4": 0, "s3-g5": -1500 + 4000,
    "p1": 12, "p2": F(-38, 10), "p3": 5, "p4": F(-7, 2), "p5": -12, "p6": 2, "p7": F(-42, 10), "p8": 1, "p9": 0, "p10": 0, "p13": -5, "p14": 0,
    "p16": -(4 + 6), "p17": 8 - 3, "p18": -(8 - 3), "p19": -(F(25, 10) + F(15, 10)), "p20": F(13, 10) - F(8, 10), "p21": -(F(75, 10) - F(225, 100)), "p22": 0,
    "p23": -5 + 8 - 6, "p24": (4 - 2) + (0 - 3), "p25": -6 + 9, "p26": -2000 + 1200, "p27": 0, "p28": 1, "p29": -40 + 15 - 10, "p30": F(-175, 100) + F(-25, 100) + 3,
}


def test_answers_match_an_independent_recalculation():
    by_id = {e.id.split("/")[1]: e for e in REL.exercises().values()}
    for key, value in INDEPENDENT.items():
        assert by_id[key].answer.value == F(value), (key, by_id[key].answer.value, value)
    assert set(by_id) - set(INDEPENDENT) == {"s2-g2", "s2-g4", "p11", "p12", "p15"}
    assert list(by_id["s2-g2"].answer.value) == sorted([F(-2), F(15, 10), F(-4), F(0)])
    assert list(by_id["p11"].answer.value) == sorted([F(3), F(-1), F(-6), F(0), F(-5, 10)])
    assert list(by_id["p12"].answer.value) == sorted([F(-25, 10), F(-2), F(-205, 100), F(2, 10)], reverse=True)


def test_negative_answers_are_read_in_every_usual_way():
    answer = checker.Answer("number", F(-7, 2), form="decimal")
    for typed in ["-3,5", "−3,5", "-3.5", "(-3,5)", " - 3,5 ".replace(" - ", "-"), "-3,50"]:
        assert checker.check(answer, typed).status == "correct", typed
    for typed in ["3,5", "+3,5", "-3,6", "-7/2"]:
        assert checker.check(answer, typed).status in ("wrong", "wrong_form"), typed
    assert checker.check(checker.Answer("number", F(3), form="decimal"), "+3").status == "correct"


def test_chapter_shape_and_alignment_claims():
    assert REL.number == 7 and len(REL.sections) == 3 and REL.also_for == ("ci",)
    assert "lesson 10 of the C" in REL.status_note and "not been checked against the official Senegalese" in REL.status_note
    assert [s.id for s in REL.sections] == ["sens", "comparer", "addition"]


def test_assessment_keys_match_a_recalculation_from_each_prompt():
    number = r"(-?\d+(?:\{,\}\d+)?)"
    for seed in range(400):
        q = {x.id.split("/")[1]: x for x in assessment(random.Random(f"rel{seed}"))}
        assert sorted(q, key=lambda k: int(k[1:])) == [f"a{i}" for i in range(1, 13)]
        given = d(re.search(r"\$" + number + r"\$", q["a1"].prompt).group(1).replace("{,}", ","))
        assert q["a1"].answer.value == -given
        unit = d(re.search(r"graduée de (\d+(?:,\d+)?) en", q["a2"].prompt).group(1))
        count = int(re.search(r"est à (\d+) graduations", q["a2"].prompt).group(1))
        side = -1 if "à gauche" in q["a2"].prompt else 1
        assert q["a2"].answer.value == side * unit * count
        left, right = [d(x.replace("{,}", ",")) for x in re.findall(number, q["a3"].prompt.split("entre")[1])]
        assert left != right and q["a3"].answer.value == (0 if left < right else 1)
        listed = [d(x.replace("{,}", ",")) for x in re.findall(r"\$" + number + r"\$", q["a4"].prompt)]
        assert len(set(listed)) == 4 and list(q["a4"].answer.value) == sorted(listed)
        options = [d(re.search(number, o).group(1).replace("{,}", ",")) for o in q["a5"].options]
        assert len(set(options)) == 3 and options.index(min(options)) == q["a5"].answer.value
        for key in ("a6", "a7", "a8", "a9"):
            expression = re.search(r"\$(.+)\$", q[key].prompt).group(1)
            assert q[key].answer.value == evaluate(expression), (key, expression)
        start = int(re.search(r"est de (-?\d+) °C", q["a10"].prompt).group(1)) if "monte" in q["a10"].prompt else int(re.search(r"est de (\d+) °C", q["a10"].prompt).group(1))
        amount = int(re.search(r"de (\d+) °C\. Quelle", q["a10"].prompt).group(1))
        assert q["a10"].answer.value == (start + amount if "monte" in q["a10"].prompt else start - amount)
        matches = [(int(a), int(b)) for a, b in re.findall(r"(\d+) marqués et (\d+) encaissés", q["a11"].prompt)]
        assert len(matches) == 3 and q["a11"].answer.value == sum(a - b for a, b in matches)
        low, high = [int(x) for x in re.search(r"« (-\d+) est plus grand que (-\d+)", q["a12"].prompt).groups()]
        assert low < high and q["a12"].options[q["a12"].answer.value].startswith("Il a tort")


@pytest.fixture
def student(app, make_user):
    make_user("diallo@example.com", "secret123", "Diallo")
    client = app.test_client()
    client.post("/login", data={"email": "diallo@example.com", "password": "secret123"})
    client.post("/settings/curriculum", data={"curriculum": "ci:6e"})
    return client


def test_pages_render_for_a_cote_d_ivoire_student(student):
    for path in ["", "/practice", "/summary", "/assessment?seed=abcd1234", "/s/sens", "/s/comparer", "/s/addition"]:
        for headers in ({}, {"Accept-Language": "fr-FR,fr;q=0.9"}):
            assert student.get(f"/curriculum/{REL.id}{path}", headers=headers).status_code == 200, path
    reply = student.post("/curriculum/check", json={"exercise": f"{REL.id}/s3-g2", "answer": "-5"}).get_json()
    assert reply["status"] == "correct"
    assert student.post("/curriculum/check", json={"exercise": f"{REL.id}/s3-g2", "answer": "5"}).get_json()["status"] == "wrong"
