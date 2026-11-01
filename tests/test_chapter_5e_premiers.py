"""Cinquième chapter 1 (powers, division, prime numbers), recomputed independently."""
import random
import re
from fractions import Fraction as F

import pytest

from mathhelper.curriculum.chapters.sn_5e_premiers import CHAPTER as PRE, assessment

BY_ID = {e.id.split("/")[1]: e for e in PRE.exercises().values()}


def primes_to(n):
    """Return the primes up to n with a sieve, independent of the chapter's own helper."""
    sieve = [True] * (n + 1)
    sieve[0:2] = [False, False]
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = [False] * len(sieve[i * i::i])
    return [i for i, ok in enumerate(sieve) if ok]


def factors(n):
    """Return the prime factors of n by trial division."""
    out, p = [], 2
    while n > 1:
        while n % p == 0:
            out.append(p)
            n //= p
        p += 1
    return out


def test_fixed_answers_match_an_independent_recalculation():
    plain = {"s1-g1": 4**3, "s1-g2": 5**5, "s1-g3": 6**2, "s1-g4": 3 + 2 * 16,
             "s2-g1": 53 // 7, "s2-g2": 53 % 7, "s2-g4": 8 * 11 + 3,
             "s3-g2": len([p for p in primes_to(20)]), "s3-g3": 2, "s3-g4": max(primes_to(49)), "s3-g5": 2,
             "s4-g4": 2**3 * 3**2,
             "p1": 3**4, "p2": 10**5, "p3": 2**7, "p4": 12**2, "p5": 5 + 3 * 8, "p6": 20 - 16, "p7": 3**3, "p8": 100, "p9": 6**3, "p10": 12**3,
             "p13": 200 // 17, "p14": 200 % 17, "p15": 15 * 9 + 7, "p18": 500 // 12, "p19": 500 % 12, "p20": 13 * 8 + 5, "p21": 6,
             "p25": len([p for p in primes_to(40) if p > 20]), "p26": min(p for p in primes_to(120) if p > 90), "p30": 2,
             "p36": 4 * 9 * 5, "p37": 210, "p38": len(factors(72))}
    for key, value in plain.items():
        assert BY_ID[key].answer.value == F(value), (key, BY_ID[key].answer.value, value)
    lists = {"s2-g3": [96, 108], "s4-g1": factors(30), "s4-g2": factors(36), "s4-g3": factors(100), "p16": [240, 280], "p17": [72, 81],
             "p31": factors(18), "p32": factors(60), "p33": factors(90), "p34": factors(126), "p35": factors(210)}
    for key, value in lists.items():
        assert list(BY_ID[key].answer.value) == [F(v) for v in value], key
    assert 40 * 6 <= 250 < 40 * 7 and 9 * 8 <= 77 < 9 * 9 and 12 * 8 <= 100 < 12 * 9
    choices = {"s1-g5": 1, "s2-g5": 1, "s3-g1": 1, "s4-g5": 1, "p11": 1, "p12": 1, "p22": 1, "p23": 1, "p24": 2, "p27": 1, "p28": 1, "p29": 1, "p39": 0}
    for key, index in choices.items():
        assert BY_ID[key].answer.value == index, key
    assert 41 in primes_to(50) and 39 not in primes_to(50) and 49 not in primes_to(50) and 51 not in primes_to(60) and 37 in primes_to(50)
    assert set(plain) | set(lists) | set(choices) == set(BY_ID)


def test_chapter_shape_and_alignment():
    assert PRE.number == 1 and PRE.level == "5e" and len(PRE.sections) == 4 and PRE.also_for == ("ci",)
    assert "lesson 1 of the C" in PRE.status_note and "not been checked against the official Senegalese" in PRE.status_note


def test_assessment_keys_match_a_recalculation_from_each_prompt():
    for seed in range(300):
        q = {x.id.split("/")[1]: x for x in assessment(random.Random(f"pre{seed}"))}
        assert sorted(q, key=lambda k: int(k[1:])) == [f"a{i}" for i in range(1, 13)]
        base, exponent = [int(x) for x in re.findall(r"\d+", q["a1"].prompt)[:2]]
        assert q["a1"].answer.value == base**exponent
        digits = [int(x) for x in re.findall(r"\d+", q["a2"].prompt)]
        assert q["a2"].answer.value == digits[0] ** digits[1] * digits[2] ** digits[3] and digits[0] == digits[2]
        a, b, k = [int(x) for x in re.findall(r"\d+", q["a3"].prompt)]
        assert q["a3"].answer.value == (a * b) ** k
        x, y, z, two = [int(v) for v in re.findall(r"\d+", q["a4"].prompt)]
        assert q["a4"].answer.value == x + y * z**2 and two == 2
        a, b = [int(v) for v in re.findall(r"\d+", q["a5"].prompt)]
        assert q["a5"].answer.value == a // b
        a, b = [int(v) for v in re.findall(r"\d+", q["a6"].prompt)]
        assert q["a6"].answer.value == a % b and a % b != 0
        a, b = [int(v) for v in re.findall(r"\d+", q["a7"].prompt)[:2]]
        assert list(q["a7"].answer.value) == [F(a // b * b), F((a // b + 1) * b)] and a % b != 0
        options = [int(o) for o in q["a8"].options]
        assert [i for i, o in enumerate(options) if o in primes_to(100)] == [q["a8"].answer.value]
        start = int(re.findall(r"\d+", q["a9"].prompt)[0])
        assert q["a9"].answer.value == len([p for p in primes_to(start + 19) if p >= start])
        n = int(re.findall(r"\d+", q["a10"].prompt)[0])
        assert list(q["a10"].answer.value) == [F(p) for p in factors(n)]
        side = int(re.findall(r"\d+", q["a12"].prompt)[0])
        assert q["a12"].answer.value == side**3


@pytest.fixture
def student(app, make_user):
    make_user("diallo@example.com", "secret123", "Diallo")
    client = app.test_client()
    client.post("/login", data={"email": "diallo@example.com", "password": "secret123"})
    client.post("/settings/curriculum", data={"curriculum": "sn:5e"})
    return client


def test_pages_render_for_a_cinquieme_student(student):
    hub = student.get("/curriculum/").get_data(as_text=True)
    assert hub.count("chapter-card") >= 1 and "Puissances, division et nombres premiers" in hub
    for path in ["", "/practice", "/summary", "/assessment?seed=abcd1234", "/s/puissances", "/s/division", "/s/premiers", "/s/decomposition"]:
        for headers in ({}, {"Accept-Language": "fr-FR,fr;q=0.9"}):
            assert student.get(f"/curriculum/{PRE.id}{path}", headers=headers).status_code == 200, path
    for typed in ["2 ; 3 ; 5", "2;3;5", "2, 3, 5", "2 3 5"]:
        assert student.post("/curriculum/check", json={"exercise": f"{PRE.id}/s4-g1", "answer": typed}).get_json()["status"] == "correct", typed
    assert student.post("/curriculum/check", json={"exercise": f"{PRE.id}/s4-g1", "answer": "3 ; 2 ; 5"}).get_json()["status"] == "wrong"
