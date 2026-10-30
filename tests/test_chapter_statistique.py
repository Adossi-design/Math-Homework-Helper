"""Chapter 9 (statistics: counts and frequencies), recounted independently from the data shown in each prompt."""
import random
import re
from fractions import Fraction as F

import pytest

from mathhelper.curriculum.chapters.sn_6e_statistique import CHAPTER as STAT, assessment

BY_ID = {e.id.split("/")[1]: e for e in STAT.exercises().values()}


def letters_in(prompt):
    """Read the list of ballots written in a prompt."""
    return re.search(r"bulletins : ([A-Z ]+)\.", prompt).group(1).split()


def notes_in(prompt):
    """Read the list of marks written in a prompt."""
    return [int(x) for x in re.search(r"notes sont : ([\d ;]+)\.", prompt).group(1).split(";")]


def test_fixed_answers_match_an_independent_recount():
    ballots = letters_in(BY_ID["s1-g1"].prompt)
    assert len(ballots) == 20 and BY_ID["s1-g1"].answer.value == ballots.count("M")
    marks = notes_in(BY_ID["s1-g5"].prompt)
    assert BY_ID["s1-g5"].answer.value == marks.count(15)
    ballots_25 = letters_in(BY_ID["p1"].prompt)
    assert len(ballots_25) == 25 and BY_ID["p1"].answer.value == ballots_25.count("F") and BY_ID["p2"].answer.value == ballots_25.count("K")
    assert BY_ID["p13"].answer.value == F(ballots_25.count("F") * 100, 25)
    assert BY_ID["p5"].answer.value == marks.count(8)
    assert BY_ID["p6"].answer.value == len([n for n in marks if n >= 10])
    assert BY_ID["p20"].answer.value == round(F(100 * marks.count(12), len(marks)))
    plain = {"s1-g2": 7 + 9 + 4, "s1-g3": 40 - (14 + 9), "s1-g4": 0, "s2-g1": F(9, 36), "s2-g2": F(12 * 100, 40), "s2-g3": F(18 * 100, 24), "s2-g4": 1 - F(25, 100) - F(4, 10), "s2-g5": 1,
             "s3-g1": F(50 * 30, 100), "s3-g2": F(24 * 100, 40), "s3-g3": 50 - (12 + 18), "s3-g4": F(20 * 100, 50), "s3-g5": F(400 * 35, 100),
             "p3": 11 + 7 + 15 + 7, "p4": 45 - (8 + 13 + 9), "p7": 1, "p8": 30 - (12 + 7), "p9": F(10, 40), "p10": F(5, 25), "p11": F(7 * 100, 20), "p12": F(30 * 100, 50),
             "p14": F(14 * 100, 80), "p15": 100 - 22 - 48, "p16": 1, "p17": 0, "p18": 1, "p19": 1, "p21": F(80 * 25, 100), "p22": F(500 * 18, 100), "p23": F(36 * 100, 45),
             "p24": F(21 * 100, 30), "p25": 100 - 42 - 35, "p26": F(40 * 45, 100), "p27": F(40 * 35, 100), "p28": 40 - (18 + 14), "p29": F(360 * 100, 45), "p30": F(250 * (100 - 40 - 28), 100),
             "s4-g1": 0, "s4-g2": F(300 * (100 - 40 - 35), 100), "s4-g3": F(14 * 100, 50), "s4-g4": F(45 * 100, 30), "s4-g5": F((80 - 24 - 36) * 100, 80),
             "p31": max(F(8 * 100, 25), F(14 * 100, 40)), "p32": F(400 * 15, 100), "p33": F(36 * 100, 45), "p34": F((250 - 60 - 100) * 100, 250), "p35": F(150 * 40, 100), "p36": 1}
    for key, value in plain.items():
        assert BY_ID[key].answer.value == F(value), (key, BY_ID[key].answer.value, value)
    accounted = set(plain) | {"s1-g1", "s1-g5", "p1", "p2", "p5", "p6", "p13", "p20"}
    assert accounted == set(BY_ID)


def test_chapter_shape_vocabulary_and_alignment():
    assert STAT.number == 9 and len(STAT.sections) == 4 and STAT.also_for == ("ci",)
    text = repr([s.blocks for s in STAT.sections]) + repr([e.prompt for e in STAT.exercises().values()]) + STAT.intro
    for word in ("modalité", "caractère", "population"):
        assert word not in text.lower(), word
    assert "lesson 13 of the C" in STAT.status_note


def test_assessment_keys_match_a_recount_from_each_prompt():
    for seed in range(400):
        q = {x.id.split("/")[1]: x for x in assessment(random.Random(f"st{seed}"))}
        assert sorted(q, key=lambda k: int(k[1:])) == [f"a{i}" for i in range(1, 13)]
        ballots = letters_in(q["a1"].prompt)
        total = int(re.search(r"Voici (\d+) bulletins", q["a1"].prompt).group(1))
        target = re.search(r"voix pour ([A-Z])", q["a1"].prompt).group(1)
        assert len(ballots) == total and q["a1"].answer.value == ballots.count(target)
        values = [int(x) for x in re.search(r"tableau sont ([\d, ]+)\. Quel", q["a2"].prompt).group(1).split(", ")]
        assert q["a2"].answer.value == sum(values)
        first, second, whole = [int(x) for x in re.search(r"effectifs : (\d+), (\d+) et \?\. L'effectif total est (\d+)", q["a3"].prompt).groups()]
        assert q["a3"].answer.value == whole - first - second > 0
        total, count = [int(x) for x in re.search(r"Sur (\d+) données, un résultat apparaît (\d+) fois", q["a4"].prompt).groups()]
        assert q["a4"].answer.value == F(count, total)
        total, count = [int(x) for x in re.search(r"école de (\d+) élèves, (\d+) viennent à pied", q["a5"].prompt).groups()]
        assert q["a5"].answer.value == F(count * 100, total)
        c1, t1, c2, t2 = [int(x) for x in re.search(r"a (\d+) voix sur (\d+) et un autre candidat a (\d+) voix sur (\d+)", q["a6"].prompt).groups()]
        assert F(c1, t1) != F(c2, t2) and q["a6"].answer.value == (0 if F(c1, t1) > F(c2, t2) else 1)
        total, p = [int(x) for x in re.search(r"Sur (\d+) élèves, (\d+) % aiment", q["a7"].prompt).groups()]
        assert q["a7"].answer.value == F(total * p, 100) and (total * p) % 100 == 0
        count, p = [int(x) for x in re.search(r"^(\d+) élèves représentent (\d+) %", q["a8"].prompt).groups()]
        assert q["a8"].answer.value * p == count * 100
        a, b = [int(x) for x in re.search(r"résultats sont (\d+) %, (\d+) %", q["a9"].prompt).groups()]
        assert q["a9"].answer.value == 100 - a - b
        threshold, total, votes = [int(x) for x in re.search(r"au moins (\d+) % des (\d+) suffrages\. Un candidat a (\d+) voix", q["a10"].prompt).groups()]
        assert q["a10"].answer.value == (0 if F(votes * 100, total) >= threshold else 1)
        total, walking, cycling = [int(x) for x in re.search(r"classe de (\d+) élèves, (\d+) viennent à pied et (\d+) à vélo", q["a11"].prompt).groups()]
        assert q["a11"].answer.value == F((total - walking - cycling) * 100, total)
        votes, total = [int(x) for x in re.search(r"« (\d+) voix sur (\d+), c'est", q["a12"].prompt).groups()]
        assert q["a12"].options[q["a12"].answer.value].startswith("Il a tort : ") and "÷" in q["a12"].options[q["a12"].answer.value] and F(votes, total) != F(votes, 100)


@pytest.fixture
def student(app, make_user):
    make_user("traore@example.com", "secret123", "Traore")
    client = app.test_client()
    client.post("/login", data={"email": "traore@example.com", "password": "secret123"})
    client.post("/settings/curriculum", data={"curriculum": "ci:6e"})
    return client


def test_pages_render_and_percent_answers_are_read(student):
    for path in ["", "/practice", "/summary", "/assessment?seed=abcd1234", "/s/effectif", "/s/frequence", "/s/tableaux"]:
        for headers in ({}, {"Accept-Language": "fr-FR,fr;q=0.9"}):
            assert student.get(f"/curriculum/{STAT.id}{path}", headers=headers).status_code == 200, path
    for typed in ["30", "30 %", "30%", "30 pour cent"]:
        assert student.post("/curriculum/check", json={"exercise": f"{STAT.id}/s2-g2", "answer": typed}).get_json()["status"] == "correct", typed
    assert student.post("/curriculum/check", json={"exercise": f"{STAT.id}/s2-g2", "answer": "12/40"}).get_json()["status"] == "wrong_form"
