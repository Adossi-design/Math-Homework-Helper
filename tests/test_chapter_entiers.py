"""Chapter 8 (natural numbers, multiples, divisors, divisibility), recalculated independently."""
import random
import re
from fractions import Fraction as F

import pytest

from mathhelper.curriculum.chapters.sn_6e_entiers import CHAPTER as ENT, assessment


def divisors_of(n):
    """Count the divisors with a plain loop, written separately from the chapter."""
    return [k for k in range(1, n + 1) if n % k == 0]


def digit_total(n):
    """Add the digits of a number."""
    return sum(map(int, str(n)))


INDEPENDENT = {
    "s1-g1": 350, "s1-g2": 999, "s1-g3": len(range(48, 63)), "s1-g4": len(range(30, 46)), "s1-g5": 1,
    "s2-g1": 45, "s2-g2": len([n for n in range(1, 101) if n % 7 == 0]), "s2-g3": len(divisors_of(48)), "s2-g4": 1, "s2-g5": max(k for k in divisors_of(60) if k != 60),
    "s3-g1": 1, "s3-g2": len([n for n in (84, 95, 126, 207, 330) if digit_total(n) % 3 == 0]), "s3-g3": min(c for c in range(10) if int(f"52{c}") % 3 == 0),
    "s3-g4": 2, "s3-g5": len([n for n in (1200, 3450, 7000, 9100) if n % 100 == 0]),
    "p1": 3000, "p2": len(range(106, 120)), "p3": len(range(200, 216)), "p4": 28, "p5": 0, "p6": 0,
    "p7": min(n for n in range(101, 200) if n % 12 == 0), "p8": len([n for n in range(1, 101) if n % 6 == 0]), "p9": len(divisors_of(30)), "p10": len(divisors_of(17)),
    "p11": max(k for k in divisors_of(84) if k != 84), "p12": 0, "p13": len(divisors_of(36)) - 1,
    "p14": min(n for n in range(1, 100) if n % 4 == 0 and n % 6 == 0), "p15": 1, "p16": 1,
    "p17": len([n for n in (120, 225, 400, 505, 710) if n % 10 == 0]), "p18": min(c for c in range(10) if int(f"3{c}4") % 9 == 0),
    "p19": len([n for n in (63, 81, 104, 222, 459) if n % 9 == 0]), "p20": len([n for n in (135, 250, 90, 165) if n % 15 == 0]), "p21": 0,
    "p22": min(n for n in range(100, 1000) if n % 5 == 0 and n % 9 == 0), "p23": len([n for n in range(1, 51) if n % 5 == 0]),
    "p24": max(c for c in range(10) if int(f"6{c}5") % 3 == 0),
    "p25": len([n for n in range(1, 21) if n % 2 == 0]), "p26": 1, "p27": len([n for n in (3000, 4500, 6200, 8000) if n % 1000 == 0]),
}


def test_answers_match_an_independent_recalculation():
    by_id = {e.id.split("/")[1]: e for e in ENT.exercises().values()}
    assert set(by_id) == set(INDEPENDENT)
    for key, value in INDEPENDENT.items():
        assert by_id[key].answer.value == F(value), (key, by_id[key].answer.value, value)


def test_the_divisibility_choices_have_exactly_one_correct_option():
    by_id = {e.id.split("/")[1]: e for e in ENT.exercises().values()}
    for key, rule in [("s3-g1", lambda n: n % 5 == 0), ("s3-g4", lambda n: n % 9 == 0), ("p16", lambda n: n % 2 == 0), ("s2-g4", lambda n: 45 % n == 0)]:
        numbers = [int(o.replace(" ", "")) for o in by_id[key].options]
        assert [i for i, n in enumerate(numbers) if rule(n)] == [by_id[key].answer.value], key


def test_assessment_keys_match_a_recalculation_from_each_prompt():
    for seed in range(400):
        q = {x.id.split("/")[1]: x for x in assessment(random.Random(f"en{seed}"))}
        assert sorted(q, key=lambda k: int(k[1:])) == [f"a{i}" for i in range(1, 13)]
        a, b = [int(x) for x in re.search(r"strictement compris entre (\d+) et (\d+)", q["a1"].prompt).groups()]
        assert q["a1"].answer.value == len(range(a + 1, b))
        a, b = [int(x) for x in re.search(r"de (\d+) à (\d+), ces deux", q["a2"].prompt).groups()]
        assert q["a2"].answer.value == len(range(a, b + 1))
        total = int(re.search(r"pour somme (\d+)", q["a3"].prompt).group(1))
        smallest = q["a3"].answer.value
        assert smallest + (smallest + 1) + (smallest + 2) == total
        k, bound = [int(x) for x in re.search(r"multiple de (\d+) supérieur à (\d+)", q["a4"].prompt).groups()]
        assert q["a4"].answer.value == min(n for n in range(bound + 1, bound + k + 1) if n % k == 0)
        n = int(re.search(r"Combien de diviseurs a (\d+)", q["a5"].prompt).group(1))
        assert q["a5"].answer.value == len(divisors_of(n))
        n = int(re.search(r"plus grand diviseur de (\d+)", q["a6"].prompt).group(1))
        assert q["a6"].answer.value == max(k for k in divisors_of(n) if k != n)
        k = int(re.search(r"multiple de (\d+) \?", q["a7"].prompt).group(1))
        options = [int(o) for o in q["a7"].options]
        assert [i for i, v in enumerate(options) if v % k == 0] == [q["a7"].answer.value]
        for key, modulus in (("a8", 3), ("a9", 9)):
            assert "le plus petit possible" in q[key].prompt
            first, last = [int(x) for x in re.search(r"le nombre (\d)c(\d) soit", q[key].prompt).groups()]
            good = [c for c in range(10) if int(f"{first}{c}{last}") % modulus == 0]
            assert q[key].answer.value == min(good), (key, first, last)
        listed = [int(x) for x in re.search(r"Parmi (.+), combien", q["a10"].prompt).group(1).split(" ; ")]
        assert q["a10"].answer.value == len([n for n in listed if n % 3 == 0 and n % 5 == 0])
        n = int(re.search(r"range (\d+) oranges", q["a11"].prompt).group(1))
        assert q["a11"].answer.value == len(divisors_of(n)) - 1
        n = int(re.search(r"« (\d+) est divisible par 9", q["a12"].prompt).group(1))
        assert n % 3 == 0 and n % 9 != 0
        assert q["a12"].options[q["a12"].answer.value].startswith("Elle a tort : la somme des chiffres")


@pytest.fixture
def student(app, make_user):
    make_user("kone2@example.com", "secret123", "Kone")
    client = app.test_client()
    client.post("/login", data={"email": "kone2@example.com", "password": "secret123"})
    client.post("/settings/curriculum", data={"curriculum": "ci:6e"})
    return client


def test_pages_render_and_checks_work_for_a_cote_d_ivoire_student(student):
    for path in ["", "/practice", "/summary", "/assessment?seed=abcd1234", "/s/consecutifs", "/s/multiples", "/s/criteres"]:
        for headers in ({}, {"Accept-Language": "fr-FR,fr;q=0.9"}):
            assert student.get(f"/curriculum/{ENT.id}{path}", headers=headers).status_code == 200, path
    reply = student.post("/curriculum/check", json={"exercise": f"{ENT.id}/s1-g3", "answer": "15"}).get_json()
    assert reply["status"] == "correct"
    assert student.post("/curriculum/check", json={"exercise": f"{ENT.id}/s1-g3", "answer": "16"}).get_json()["status"] == "wrong"
    assert "lesson 9 of the C" in ENT.status_note
