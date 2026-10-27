"""Checks that run over every chapter, and the independent recalculation of chapter 2 (multiplication)."""
import random
import re
from fractions import Fraction

import pytest

from mathhelper.curriculum import checker
from mathhelper.curriculum.catalog import CHAPTERS, chapters_for
from mathhelper.curriculum.chapters.kit import d
from mathhelper.curriculum.chapters.sn_6e_multiplication import CHAPTER as MULT, assessment as mult_assessment, round_unit
from mathhelper.curriculum.progress import prerequisites
from mathhelper.models import ChapterAttempt

BY_ID = {c.id: c for c in CHAPTERS}
ALL = [pytest.param(c, id=c.id) for c in CHAPTERS]
CONTROL = "\t\f\b\r\a\v\x00"


def strings(node):
    """Yield every string inside nested content."""
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for value in node.values():
            yield from strings(value)
    elif isinstance(node, (list, tuple)):
        for value in node:
            yield from strings(value)
    elif hasattr(node, "__dict__"):
        yield from strings(vars(node))


@pytest.mark.parametrize("chapter", ALL)
def test_every_chapter_is_well_formed_and_free_of_broken_escapes(chapter):
    content = [chapter.intro, chapter.objectives, chapter.sections, chapter.practice, chapter.summary, chapter.concepts, chapter.prerequisites]
    for seed in range(40):
        content.append(chapter.assessment(random.Random(f"w{seed}")))
    for text in strings(content):
        assert not any(ch in text for ch in CONTROL), text[:60]
    ids = [e.id for e in chapter.practice] + [e.id for s in chapter.sections for e in s.guided]
    assert len(ids) == len(set(ids)) and all(i.startswith(chapter.id + "/") for i in ids)
    for section in chapter.sections:
        assert section.concept in chapter.concepts and chapter.concepts[section.concept][1] == section.id
        assert section.blocks and section.guided
    for entry in chapter.concepts.values():
        assert chapter.section(entry[1]) is not None
    assert all(e.hints and e.solution and e.concept in chapter.concepts for e in chapter.exercises().values())
    assert len(chapter.assessment(random.Random("x1234"))) == 12


@pytest.mark.parametrize("chapter", ALL)
def test_every_worked_example_of_every_chapter_verifies(chapter):
    count = 0
    for section in chapter.sections:
        for block in section.blocks:
            if block["type"] == "example":
                assert eval(block["verify"], {"d": d, "round_unit": round_unit, "math": __import__("math")}), (chapter.id, section.id, block["title"])
                count += 1
    assert count >= 12


def typed(e):
    """Write the correct answer of an exercise the way a student would type it."""
    if e.answer.kind == "choice":
        return str(e.answer.value)
    if e.answer.kind == "numbers":
        return " ; ".join(checker.show(v) for v in e.answer.value)
    if e.answer.kind == "between":
        return checker.show((e.answer.value + e.answer.high) / 2)
    if e.answer.form == "decimal_fraction":
        return f"{int(e.answer.value * 1000)}/1000"
    if e.answer.form in ("fraction", "irreducible"):
        value = e.answer.value
        return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
    return checker.show(e.answer.value)


@pytest.mark.parametrize("chapter", ALL)
def test_every_fixed_exercise_accepts_its_own_answer_and_rejects_a_nearby_one(chapter):
    for e in chapter.exercises().values():
        assert checker.check(e.answer, typed(e)).status == "correct", e.id
        if e.answer.kind == "number":
            assert checker.check(e.answer, checker.show(e.answer.value + Fraction(1, 1000))).status in ("wrong", "wrong_form"), e.id
        if e.answer.kind == "choice":
            assert 0 <= e.answer.value < len(e.options) and len(e.options) >= 2
            assert all(0 <= key < len(e.options) and key != e.answer.value for key in e.wrong), e.id


@pytest.mark.parametrize("chapter", ALL)
def test_assessments_accept_their_own_answers_for_many_seeds(chapter):
    for seed in range(150):
        for q in chapter.assessment(random.Random(f"k{seed}")):
            assert checker.check(q.answer, typed(q)).status == "correct", (q.id, seed)
            if q.answer.kind == "choice":
                assert len(set(q.options)) == len(q.options)


def test_chapters_of_the_same_level_come_in_order_and_declare_real_prerequisites():
    assert [c.number for c in chapters_for("sn", "6e")] == [1, 2, 3, 4, 5, 6]
    for chapter in CHAPTERS:
        for item in chapter.prerequisites:
            assert "chapter" in item and item["chapter"] in BY_ID and BY_ID[item["chapter"]].number < chapter.number or "course" in item
    done = {f"cur:sn-6e-decimaux:{s.id}" for s in BY_ID["sn-6e-decimaux"].sections}
    assert [p["done"] for p in prerequisites(MULT, done)] == [True, False]
    assert [p["done"] for p in prerequisites(MULT, set())] == [False, False]


# ----- Chapter 2, recalculated independently with integers -----

F = Fraction
INDEPENDENT = {
    "s1-g1": F(32 * 2, 10), "s1-g2": F(14 * 6, 100), "s1-g3": F(65 * 34, 100), "s1-g4": 29 * 3, "s1-g5": 0,
    "s2-g1": F(528, 10), "s2-g2": F(58, 10), "s2-g3": F(125, 100), "s2-g4": 100, "s2-g5": 2350,
    "s3-g1": 0, "s3-g2": 73, "s3-g3": F(42 * 101, 10), "s3-g4": 26,
    "s4-g1": 64, "s4-g2": F(121, 100), "s4-g3": F(8, 1000), "s4-g4": 1, "s4-g5": F(35 * 35, 100),
    "p1": 12, "p2": F(12, 10), "p3": 1, "p4": 10, "p5": F(405 * 6, 100), "p6": F(314 * 25, 1000), "p7": 42 * 5, "p8": 1, "p9": F(125 * 84, 100),
    "p10": 3500 * 18 // 10, "p11": 0, "p12": 73, "p13": 86, "p14": 5400, "p15": 64, "p16": F(95, 1000), "p17": 360, "p18": 1000, "p19": 0,
    "p20": F(72), "p21": 850, "p22": F(65 * 102, 10), "p23": 73, "p24": F(599 * 8, 100), "p25": 1, "p26": 1, "p27": 0,
    "p28": 36, "p29": F(25, 100), "p30": F(625, 100), "p31": 64, "p32": F(27, 1000), "p33": 1, "p34": F(15 * 15 * 15, 1000), "p35": F(125, 10) * 480 + 8 * 350, "p36": F(4 * 4, 100) * 50,
}


def test_chapter_two_answers_match_an_independent_recalculation():
    by_id = {e.id.split("/")[1]: e for e in MULT.exercises().values()}
    assert set(by_id) == set(INDEPENDENT)
    for key, value in INDEPENDENT.items():
        assert by_id[key].answer.value == F(value), (key, by_id[key].answer.value, value)


def test_chapter_two_shape():
    assert len(MULT.sections) == 4 and len(MULT.practice) == 36 and sum(len(s.guided) for s in MULT.sections) == 19
    assert MULT.number == 2 and "not been checked against the official" in MULT.status_note


def test_chapter_two_required_forms():
    by_id = {e.id.split("/")[1]: e for e in MULT.exercises().values()}
    assert checker.check(by_id["s1-g1"].answer, "64/10").status == "wrong_form"
    assert checker.check(by_id["p2"].answer, "12/10").status == "wrong_form"
    assert checker.check(by_id["s2-g5"].answer, "2 350 m").status == "correct"
    assert checker.check(by_id["p9"].answer, "105 m²").status == "correct"
    assert checker.check(by_id["p10"].answer, "6300 F").status == "correct"


def prompt_numbers(text):
    """Read every number written as math in a prompt, as exact fractions."""
    return [d(x.replace("{,}", ",")) for x in re.findall(r"\$?([0-9]+(?:\{,\}[0-9]+)?)", text.replace("\\times", " "))]


def test_chapter_two_assessment_keys_match_a_recalculation_from_each_prompt():
    for seed in range(300):
        q = {x.id.split("/")[1]: x for x in mult_assessment(random.Random(f"m{seed}"))}
        assert sorted(q, key=lambda k: int(k[1:])) == [f"a{i}" for i in range(1, 13)]
        for key in ("a1", "a2", "a3"):
            left, right = [d(x.replace("{,}", ",")) for x in re.findall(r"([0-9]+(?:\{,\}[0-9]+)?) \\times ([0-9]+(?:\{,\}[0-9]+)?)", q[key].prompt)[0]]
            assert q[key].answer.value == left * right, (key, q[key].prompt)
        left, right = [d(x.replace("{,}", ",")) for x in re.findall(r"([0-9]+(?:\{,\}[0-9]+)?) \\times ([0-9]+(?:\{,\}[0-9]+)?)", q["a4"].prompt)[0]]
        assert q["a4"].answer.value == int(left + F(1, 2)) * int(right + F(1, 2))
        left, power = [d(x.replace("{,}", ",")) for x in re.findall(r"([0-9]+(?:\{,\}[0-9]+)?) \\times ([0-9]+(?:\{,\}[0-9]+)?)", q["a5"].prompt)[0]]
        assert q["a5"].answer.value == left * power and power in (10, 100, 1000)
        left, small = [d(x.replace("{,}", ",")) for x in re.findall(r"([0-9]+(?:\{,\}[0-9]+)?) \\times ([0-9]+(?:\{,\}[0-9]+)?)", q["a6"].prompt)[0]]
        assert q["a6"].answer.value == left * small and small in (F(1, 10), F(1, 100), F(1, 1000))
        base, result = prompt_numbers(q["a7"].prompt)
        assert base * q["a7"].answer.value == result
        first, middle, last = [d(x.replace("{,}", ",")) for x in re.findall(r"([0-9]+(?:\{,\}[0-9]+)?)", q["a8"].prompt)[:3]]
        assert q["a8"].answer.value == first * middle * last and first * last == 100
        left, multiplier = [d(x.replace("{,}", ",")) for x in re.findall(r"([0-9]+(?:\{,\}[0-9]+)?) \\times ([0-9]+)", q["a9"].prompt)[0]]
        assert q["a9"].answer.value == left * multiplier
        base = prompt_numbers(q["a10"].prompt)[0]
        power = int(re.search(r"\^([23])", q["a10"].prompt).group(1))
        assert q["a10"].answer.value == base**power
        if "rectangle" in q["a11"].prompt:
            length, width = [d(x.replace(".", ",")) for x in re.findall(r"(\d+(?:,\d+)?) m ", q["a11"].prompt.replace("{,}", ","))[:2]]
            assert q["a11"].answer.value == length * width
        else:
            price = int(re.search(r"coûte (\d+) F", q["a11"].prompt).group(1))
            weight = d(re.search(r"achète (\d+(?:,\d+)?) kg", q["a11"].prompt).group(1))
            assert q["a11"].answer.value == price * weight and q["a11"].answer.value.denominator == 1
        whole, factor = [d(x.replace("{,}", ",")) for x in re.findall(r"([0-9]+(?:\{,\}[0-9]+)?)", q["a12"].prompt)[:2]]
        assert factor < 1 and q["a12"].options[q["a12"].answer.value].startswith("Elle a tort : ")
        assert sum(o.startswith("Elle a tort : ") and "plus petit que 1" in o for o in q["a12"].options) == 1


# ----- Chapter 2 in the app -----

CID = MULT.id


@pytest.fixture
def student(logged_in):
    logged_in.post("/settings/curriculum", data={"curriculum": "sn:6e"})
    return logged_in


def test_both_chapters_are_listed_and_the_second_links_to_the_first(student):
    hub = student.get("/curriculum/").get_data(as_text=True)
    assert "Les nombres décimaux arithmétiques" in hub or "decimal" in hub.lower()
    assert hub.count("course-card") == 6
    page = student.get(f"/curriculum/{CID}").get_data(as_text=True)
    assert "/curriculum/sn-6e-decimaux" in page and "Open the chapter" in page


@pytest.mark.parametrize("path", ["", "/practice", "/summary", "/assessment?seed=abcd1234", "/s/produit", "/s/decalage", "/s/proprietes", "/s/puissances"])
def test_chapter_two_pages_render_in_both_languages(student, path):
    for headers in ({}, {"Accept-Language": "fr-FR,fr;q=0.9"}):
        assert student.get(f"/curriculum/{CID}{path}", headers=headers).status_code == 200


def test_chapter_two_exercises_progress_and_assessment_work(app, student):
    reply = student.post("/curriculum/check", json={"exercise": f"{CID}/s1-g3", "answer": "22.10"}).get_json()
    assert reply["status"] == "correct" and reply["solved"]
    assert student.post("/curriculum/check", json={"exercise": f"{CID}/s1-g3", "answer": "2,21"}).get_json()["status"] == "wrong"
    seed = "multi0001"
    answers = [typed(q) for q in mult_assessment(random.Random(seed))]
    location = student.post(f"/curriculum/{CID}/assessment", data={"seed": seed, **{f"q{i}": a for i, a in enumerate(answers)}}).location
    page = student.get(location).get_data(as_text=True)
    assert "12<span>/12</span>" in page and "Well done" in page
    student.post(f"/curriculum/{CID}/s/produit/complete")
    assert "1 of 4 sections done" in student.get(f"/curriculum/{CID}").get_data(as_text=True)
    with app.app_context():
        from mathhelper.extensions import db
        assert db.session.query(ChapterAttempt).filter_by(chapter_id=CID).count() == 1


# ----- Chapter 3 (division), recalculated independently with integers -----

from mathhelper.curriculum.chapters.sn_6e_division import CHAPTER as DIV, assessment as div_assessment, terminates

INDEPENDENT_DIV = {
    "s1-g1": F(25, 10), "s1-g2": F(114, 100), "s1-g3": F(875, 1000), "s1-g4": 0, "s1-g5": F(175, 100),
    "s2-g1": 36 // 9, "s2-g2": 540 // 6, "s2-g3": F(49, 10), "s2-g4": 1, "s2-g5": 450 // 75,
    "s3-g1": F(83, 10), "s3-g2": F(56, 1000), "s3-g3": 47, "s3-g4": 35, "s3-g5": F(375, 100),
    "s4-g1": 29 // 4, "s4-g2": F(5 * 10 // 3 + 1, 10), "s4-g3": F(2 * 100 // 7, 100), "s4-g4": F(31, 10), "s4-g5": 1,
    "p1": F(225, 100), "p2": F(126, 100), "p3": F(225, 1000), "p4": F(525, 100), "p5": F(625, 1000), "p6": F(105, 100), "p7": F(175, 100), "p8": F(46875, 100),
    "p9": 0, "p10": 2, "p11": 48 // 6, "p12": 72 // 8, "p13": 900 // 25, "p14": 156 // 12, "p15": 720 // 45, "p16": 1, "p17": 750 // 25, "p18": 360 // 15,
    "p19": 46, "p20": F(96, 1000), "p21": F(53, 1000), "p22": 86, "p23": 75, "p24": F(36, 10), "p25": F(175, 100), "p26": 0,
    "p27": 38 // 7, "p28": 38 // 7 + 1, "p29": F(14 * 10 // 3, 10), "p30": F(30 * 100 // 7 + 1, 100), "p31": F(28, 10), "p32": F(100 // 6, 100), "p33": F(50 * 100 // 7, 100), "p34": 0, "p35": F(47 * 10 // 9, 10) , "p36": (144 // 6) * 250, "p37": 630 // 45,
}


def test_chapter_three_answers_match_an_independent_recalculation():
    by_id = {e.id.split("/")[1]: e for e in DIV.exercises().values()}
    assert set(by_id) == set(INDEPENDENT_DIV)
    for key, value in INDEPENDENT_DIV.items():
        assert by_id[key].answer.value == F(value), (key, by_id[key].answer.value, value)


def test_chapter_three_shape_and_required_forms():
    assert DIV.number == 3 and len(DIV.sections) == 4 and len(DIV.practice) == 37
    by_id = {e.id.split("/")[1]: e for e in DIV.exercises().values()}
    assert checker.check(by_id["s1-g1"].answer, "5/2").status == "wrong_form"
    assert checker.check(by_id["p29"].answer, "46/10").status == "wrong_form"
    assert checker.check(by_id["p33"].answer, "7,14 litres").status == "correct"


def number_of(text):
    """Read the first number in a piece of text, written with {,} or a comma, as an exact fraction."""
    return d(re.search(r"[0-9]+(?:\{,\}[0-9]+|,[0-9]+)?", text).group(0).replace("{,}", ","))


def test_chapter_three_assessment_keys_match_a_recalculation_from_each_prompt():
    num = r"([0-9]+(?:\{,\}[0-9]+)?)"
    for seed in range(300):
        q = {x.id.split("/")[1]: x for x in div_assessment(random.Random(f"v{seed}"))}
        assert sorted(q, key=lambda k: int(k[1:])) == [f"a{i}" for i in range(1, 13)]
        for key in ("a1", "a2", "a5", "a6", "a7", "a8"):
            left, right = [d(x.replace("{,}", ",")) for x in re.findall(num + r" \\div " + num, q[key].prompt)[0]]
            assert q[key].answer.value * right == left, (key, q[key].prompt)
        numerator, denominator = [int(x) for x in re.search(r"dfrac\{(\d+)\}\{(\d+)\}", q["a3"].prompt).groups()]
        assert q["a3"].answer.value == F(numerator, denominator)
        total, people = [d(x.replace("{,}", ",")) for x in re.search(r"corde entre", q["a4"].prompt) and re.findall(r"(\d+(?:,\d+)?) m de corde entre (\d+)", q["a4"].prompt.replace("{,}", ","))[0]]
        assert q["a4"].answer.value * people == total
        for key in ("a9", "a10", "a11"):
            a, b = [int(x) for x in re.search(r"\$(\d+) \\div (\d+)\$", q[key].prompt).groups()]
            places = 0 if "unité" in q[key].prompt else 2 if ("0,01" in q[key].prompt or "centième" in q[key].prompt) else 1
            scaled = a * 10**places
            low, rest = divmod(scaled, b)
            assert rest != 0
            expected = {"a9": F(low, 10**places), "a10": F(low + 1, 10**places), "a11": F(low + (2 * rest > b), 10**places)}[key]
            assert q[key].answer.value == expected, (key, q[key].prompt)
        assert q["a12"].options[q["a12"].answer.value].startswith("Il a tort : ") and "plus grand que" in q["a12"].options[q["a12"].answer.value]
        divisor = d(re.findall(num, q["a12"].prompt.split("est plus petit")[0])[1].replace("{,}", ","))
        assert divisor < 1


def test_chapter_three_is_in_the_app(student_division):
    page = student_division.get("/curriculum/").get_data(as_text=True)
    assert page.count("course-card") == 6
    for path in ["", "/practice", "/summary", "/assessment?seed=abcd1234", "/s/quotient", "/s/diviseur_decimal", "/s/decalage_div", "/s/approche"]:
        assert student_division.get(f"/curriculum/{DIV.id}{path}").status_code == 200, path


@pytest.fixture
def student_division(logged_in):
    logged_in.post("/settings/curriculum", data={"curriculum": "sn:6e"})
    return logged_in


# ----- Chapter 4 (organising a calculation), recalculated independently -----

from mathhelper.curriculum.chapters.sn_6e_calcul import CHAPTER as CALC, assessment as calc_assessment

INDEPENDENT_CALC = {
    "s1-g1": 5 + 4 * 3, "s1-g2": 20 - 6 // 2, "s1-g3": 50 - 8 + 5, "s1-g4": 36 // 6 * 3, "s1-g5": 1,
    "s2-g1": (7 + 5) * 3, "s2-g2": 4 * (9 - 6) + 2, "s2-g3": 30 - (8 + 7), "s2-g4": 2 * (3 + 4 * 2), "s2-g5": 0,
    "s3-g1": (12 + 8) * 3, "s3-g2": 6 * 4 - 5, "s3-g3": (20 - 6) // 2, "s3-g4": 4 * 150 + 3 * 100, "s3-g5": 1,
    "p1": 8 + 2 * 5, "p2": 30 - 4 * 5, "p3": 6 * 7 - 12 // 3, "p4": 100 - 25 + 5, "p5": 90 // 9 * 5, "p6": F(25, 10) + F(15, 10) * 4,
    "p7": 18 // 3 + 4 * F(25, 10), "p8": F(72, 10) - 2 * F(6, 10) + F(5, 10), "p9": 0, "p10": 1,
    "p11": (9 + 6) * 4, "p12": 5 * (12 - 7), "p13": 45 - (18 + 7), "p14": (F(75, 10) - F(25, 10)) * 4 + 3, "p15": 3 * (4 + 2 * 5), "p16": 80 // (2 + 3),
    "p17": (50 - 14) // 4 + 6, "p18": 100 - (20 + (15 - 5) * 2), "p19": 0, "p20": 0,
    "p21": 2 * (6 + 9), "p22": 48 // (11 - 5), "p23": F(25, 10) * (3 + 1), "p24": 3 * 7 + 20 // 4, "p25": 1,
    "p26": 2000 - (3 * 350 + 125), "p27": 2 * (F(125, 10) + 8), "p28": (6 - 4) * 25, "p29": 1800 + 2 * 450 - 300, "p30": (120 + 80) // 4,
}


def test_chapter_four_answers_match_an_independent_recalculation():
    by_id = {e.id.split("/")[1]: e for e in CALC.exercises().values()}
    assert set(by_id) == set(INDEPENDENT_CALC)
    for key, value in INDEPENDENT_CALC.items():
        assert by_id[key].answer.value == F(value), (key, by_id[key].answer.value, value)


def evaluate(text):
    """Evaluate an expression written with times, div and decimal commas, using exact fractions and normal priority rules."""
    text = text.replace("\\times", "*").replace("\\div", "/").replace("{,}", ".")
    return eval(re.sub(r"\d+(?:\.\d+)?", lambda m: f'F("{m.group(0)}")', text), {"F": Fraction})


def test_chapter_four_assessment_keys_match_a_recalculation_from_each_prompt():
    for seed in range(300):
        q = {x.id.split("/")[1]: x for x in calc_assessment(random.Random(f"c{seed}"))}
        assert sorted(q, key=lambda k: int(k[1:])) == [f"a{i}" for i in range(1, 13)]
        for key in ("a1", "a2", "a3", "a4", "a5", "a6", "a7"):
            expression = re.search(r"\$(.+)\$", q[key].prompt).group(1)
            value = evaluate(expression)
            assert q[key].answer.value == value and value > 0, (key, expression)
        expression = re.search(r"\$(.+)\$", q["a8"].prompt).group(1)
        right_option = q["a8"].options[q["a8"].answer.value]
        assert evaluate(right_option.strip("$")) == evaluate(expression) and len(set(q["a8"].options)) == 3
        a, b, c = [int(x) for x in re.findall(r"\d+", q["a9"].prompt)]
        assert q["a9"].answer.value == a * (b + c)
        x, y, z = [int(v) for v in re.findall(r"\d+", q["a10"].prompt)]
        assert q["a10"].answer.value == F(x, y - z) and x % (y - z) == 0
        n1, p1, n2, p2, bill = [int(v) for v in re.search(r"achète (\d+) cahiers à (\d+) F et (\d+) stylos à (\d+) F\. Il paie avec (\d+) F", q["a11"].prompt).groups()]
        assert q["a11"].answer.value == bill - (n1 * p1 + n2 * p2) > 0
        shown = re.search(r"\$(.+) = (\d+)\$", q["a12"].prompt)
        assert evaluate(shown.group(1)) != int(shown.group(2))
        assert q["a12"].options[q["a12"].answer.value].startswith("Il a fait l'addition avant la multiplication")


def test_chapter_four_is_in_the_app(student_division):
    for path in ["", "/practice", "/summary", "/assessment?seed=abcd1234", "/s/priorites", "/s/parentheses", "/s/traduire"]:
        assert student_division.get(f"/curriculum/{CALC.id}{path}").status_code == 200, path
    assert checker.check({e.id.split("/")[1]: e for e in CALC.exercises().values()}["p6"].answer, "17/2").status == "wrong_form"


# ----- Chapter 5 (proportionality), recalculated independently -----

from mathhelper.curriculum.chapters.sn_6e_proportionnalite import CHAPTER as PROP, assessment as prop_assessment

INDEPENDENT_PROP = {
    "s1-g1": 40 // 5, "s1-g2": F(15, 1), "s1-g3": 0, "s1-g4": 4500 // 3, "s1-g5": 1,
    "s2-g1": 10 * 14 // 4 if (10 * 14) % 4 == 0 else F(10 * 14, 4), "s2-g2": 10 * 3600 // 6, "s2-g3": 3 * 10, "s2-g4": F(5 * 25, 10), "s2-g5": 5 * (8 // 2),
    "s3-g1": 80 // 4, "s3-g2": 200 * 15 // 100, "s3-g3": 12 * 100 // 40, "s3-g4": 4 * 1000 // 100, "s3-g5": 5000 - 5000 // 10,
    "p1": F(9, 2), "p2": 5 * 12, "p3": 0, "p4": 1, "p5": F(35, 10) * 600, "p6": 36 // 4, "p7": 1, "p8": 12 + 28,
    "p9": 5 * (18000 // 12), "p10": 5 * (2000 // 8), "p11": 5 * (2100 // 3), "p12": 5 * (240 // 3), "p13": 10 * (600 // 4), "p14": 20 + 20 // 2, "p15": 5 * (9000 // 12),
    "p16": 12 * (1050 // 7), "p17": F(10 * 15, 6), "p18": F(10 * 18, 4), "p19": 360 // 2, "p20": 4500 // 10, "p21": 120 // 4, "p22": 30 * 100 // 120, "p23": 45 * 100 // 60,
    "p24": 3500 - 3500 * 20 // 100, "p25": 400 * 35 // 100, "p26": 250 * 12 // 100, "p27": 3 * 10000 // 100, "p28": 8 * 25000 // 100000, "p29": 300000 // 50000,
    "p30": 7 * 500 // 100, "p31": 0, "p32": 15 * 100000 // 3,
}


def test_chapter_five_answers_match_an_independent_recalculation():
    by_id = {e.id.split("/")[1]: e for e in PROP.exercises().values()}
    assert set(by_id) == set(INDEPENDENT_PROP)
    for key, value in INDEPENDENT_PROP.items():
        assert by_id[key].answer.value == F(value), (key, by_id[key].answer.value, value)


def test_chapter_five_assessment_keys_match_a_recalculation_from_each_prompt():
    for seed in range(300):
        q = {x.id.split("/")[1]: x for x in prop_assessment(random.Random(f"q{seed}"))}
        assert sorted(q, key=lambda k: int(k[1:])) == [f"a{i}" for i in range(1, 13)]
        base, value = [d(x.replace("{,}", ",")) for x in re.search(r"^Dans un tableau de proportionnalité, (\d+) correspond à ([\d,]+)\.", q["a1"].prompt).groups()]
        assert q["a1"].answer.value == value / base
        base, value, other = [d(x) for x in re.search(r"(\d+) correspond à ([\d,]+)\. Quel nombre correspond à (\d+) \?", q["a2"].prompt).groups()]
        assert q["a2"].answer.value == other * value / base
        n, total, m = [int(x) for x in re.search(r"(\d+) cahiers coûtent (\d+) F\. Combien coûtent (\d+) cahiers", q["a3"].prompt).groups()]
        assert q["a3"].answer.value == F(m * total, n) and total % n == 0
        a, b, target = [int(x) for x in re.search(r"(\d+) correspond à (\d+)\. Quel nombre correspond à (\d+) \?", q["a4"].prompt).groups()]
        assert target % a == 0 and q["a4"].answer.value == b * (target // a)
        a, first, c, second, target = [d(x) for x in re.search(r"(\d+) correspond à ([\d,]+) et (\d+) correspond à ([\d,]+)\. Quel nombre correspond à (\d+) \?", q["a5"].prompt).groups()]
        assert target == a + c and q["a5"].answer.value == first + second
        proportional = []
        for index, option in enumerate(q["a6"].options):
            rows = re.findall(r"\$([\d ;]+)\$", option)
            top, bottom = [[int(x) for x in row.split(";")] for row in rows]
            if len({F(b, t) for t, b in zip(top, bottom)}) == 1:
                proportional.append(index)
        assert proportional == [q["a6"].answer.value]
        p, quantity = [int(x) for x in re.search(r"Calcule (\d+) % de (\d+)\.", q["a7"].prompt).groups()]
        assert q["a7"].answer.value == F(p * quantity, 100)
        price, p = [int(x) for x in re.search(r"coûte (\d+) F\. Il est soldé avec (\d+) %", q["a8"].prompt).groups()]
        assert q["a8"].answer.value == F(price * (100 - p), 100)
        total, part = [int(x) for x in re.search(r"groupe de (\d+) élèves, (\d+) portent", q["a9"].prompt).groups()]
        assert q["a9"].answer.value == F(part * 100, total)
        scale, cm = [int(x) for x in re.search(r"échelle 1/(\d+), deux villages sont séparés de (\d+) cm", q["a10"].prompt).groups()]
        assert q["a10"].answer.value == F(cm * scale, 100000)
        scale, meters = [int(x) for x in re.search(r"réelle de (\d+) m est dessinée sur un plan à l'échelle 1/(\d+)", q["a11"].prompt).groups()][::-1]
        assert q["a11"].answer.value == F(meters * 100, scale)
        assert q["a12"].options[q["a12"].answer.value].startswith("Il a tort : la taille")


def test_chapter_five_is_offered_to_cote_d_ivoire_students_with_an_honest_note(app, make_user):
    make_user("yao@example.com", "secret123", "Yao")
    client = app.test_client()
    client.post("/login", data={"email": "yao@example.com", "password": "secret123"})
    client.post("/settings/curriculum", data={"curriculum": "ci:6e"})
    hub = client.get("/curriculum/").get_data(as_text=True)
    assert hub.count("course-card") == 2
    page = client.get(f"/curriculum/{PROP.id}").get_data(as_text=True)
    assert "lesson 12 of the C" in page and "Sixième programme (proportional" in page and "belongs to another curriculum" not in page
    for path in ["", "/practice", "/summary", "/assessment?seed=abcd1234", "/s/reconnaitre", "/s/calculer", "/s/pourcentage"]:
        assert client.get(f"/curriculum/{PROP.id}{path}").status_code == 200, path
    other = client.get("/curriculum/sn-6e-decimaux").get_data(as_text=True)
    assert "belongs to another curriculum" in other
    client.post("/settings/curriculum", data={"curriculum": "td:6e"})
    assert "No chapters here yet" in client.get("/curriculum/").get_data(as_text=True)


def test_every_division_and_proportion_answer_must_be_a_decimal_not_the_question_retyped():
    for chapter in (DIV, PROP):
        for e in chapter.exercises().values():
            if e.answer.kind == "number":
                assert e.answer.form in ("decimal", "decimal_fraction"), e.id
    by_id = {e.id.split("/")[1]: e for e in DIV.exercises().values()}
    for key, typed_back in [("s1-g2", "4,56/4"), ("s2-g1", "3,6/0,9"), ("p4", "21/4"), ("p13", "9/0,25"), ("s3-g1", "83/10")]:
        assert checker.check(by_id[key].answer, typed_back).status == "wrong_form", key
    for _ in range(300):
        for q in div_assessment(random.Random(f"r{_}")):
            if q.answer.kind == "number":
                assert q.answer.form == "decimal", q.id


def test_the_truncated_digits_in_the_approximation_solution_are_never_rounded():
    for seed in range(300):
        q = {x.id.split("/")[1]: x for x in div_assessment(random.Random(f"t{seed}"))}["a9"]
        line = q.solution[0]
        assert ",,," not in line and line.endswith("...")
        a, b = [int(x) for x in re.search(r"(\d+) ÷ (\d+) = ", line).groups()]
        written = re.search(r"= ([\d,]+)\.\.\.", line).group(1).replace(",", ".")
        assert F(int(F(a, b) * 10000), 10000) == F(written)


def test_units_synonyms_and_a_comma_without_leading_zero_are_accepted():
    by_id = {e.id.split("/")[1]: e for e in MULT.exercises().values()}
    for typed_text in ["6300 FCFA", "6300 francs", "6300 F"]:
        assert checker.check(by_id["p10"].answer, typed_text).status == "correct", typed_text
    assert checker.parse_number(",84") == F(84, 100) and checker.parse_number(".5") == F(1, 2)
    assert checker.parse_number(",") is None and checker.parse_number("1,") is None
