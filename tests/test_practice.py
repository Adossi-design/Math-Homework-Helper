"""Practice generators, scoring and the practice pages."""
import re

import pytest

from mathhelper.practice import SKILLS, build_round, score_round


@pytest.mark.parametrize("skill_id", sorted(SKILLS))
def test_every_skill_makes_valid_rounds(skill_id):
    for seed in range(150):
        questions = build_round(skill_id, f"seed{seed}")
        assert len(questions) == 10
        for q in questions:
            assert len(q.choices) == 4 and len(set(q.choices)) == 4
            assert 0 <= q.answer < 4
            for text in [q.prompt, q.explanation, *q.choices]:
                assert text.count("$") % 2 == 0, text
                assert "\x0c" not in text and "{n}" not in text


def test_rounds_repeat_exactly_for_the_same_seed():
    first = [q.prompt for q in build_round("quadratics", "abc")]
    assert first == [q.prompt for q in build_round("quadratics", "abc")]
    assert first != [q.prompt for q in build_round("quadratics", "xyz")]


def test_linear_answers_satisfy_their_equation():
    for seed in range(100):
        for q in build_round("linear-equations", str(seed)):
            match = re.fullmatch(r"Solve for \$x\$: \$(-?\d*)x ([+-]) (\d+) = (-?\d+)\$", q.prompt)
            if not match:
                continue
            a = int(match[1]) if match[1] not in ("", "-") else (-1 if match[1] == "-" else 1)
            b = int(match[3]) * (1 if match[2] == "+" else -1)
            x = int(q.choices[q.answer].strip("$"))
            assert a * x + b == int(match[4])


def test_score_round_counts_correct_answers():
    questions = build_round("fractions", "s")
    perfect = [q.answer for q in questions]
    assert score_round("fractions", "s", perfect)[2] == 10
    assert score_round("fractions", "s", [])[2] == 0


def test_round_finish_and_results(logged_in):
    page = logged_in.get("/practice/slope").get_data(as_text=True)
    seed = re.search(r'name="seed" value="([0-9a-f]{16})"', page)[1]
    perfect = ",".join(str(q.answer) for q in build_round("slope", seed))
    response = logged_in.post("/practice/slope/finish", data={"seed": seed, "answers": perfect})
    assert response.status_code == 302
    results = logged_in.get(response.location).get_data(as_text=True)
    assert "10/10" in results and "Perfect round!" in results
    assert "Best 10/10" in logged_in.get("/practice/").get_data(as_text=True)


def test_finish_rejects_bad_input(logged_in):
    assert logged_in.post("/practice/slope/finish", data={"seed": "../../etc", "answers": ""}).status_code == 400
    assert logged_in.post("/practice/unknown/finish", data={"seed": "0" * 16}).status_code == 404
    response = logged_in.post("/practice/slope/finish", data={"seed": "0" * 16, "answers": "x,--1,9,2"})
    assert response.status_code == 302
