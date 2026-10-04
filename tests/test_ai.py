"""The Gemini layer: JSON repair, model fallback and friendly errors."""
import json
from types import SimpleNamespace

import pytest
from google.genai import errors

from mathhelper import ai
from mathhelper.ai import solve_text as real_solve_text

GOOD_JSON = json.dumps({"problems": [{"problem": "p", "topic": "algebra", "answer": "a", "steps": [], "tip": ""}]})


def test_repair_keeps_valid_escapes():
    raw = r'{"a": "line\nnext", "b": "quote \" ok", "c": "\\frac{1}{2}", "d": "\u00e9"}'
    assert json.loads(ai.repair_json(raw)) == json.loads(raw)


def test_repair_fixes_unescaped_latex():
    raw = r'{"work": "$\frac{8}{2} = 4$ and $\times$ and $\sqrt{9}$ and $\beta$ and $a \neq b$ and $\underline{x}$"}'
    text = json.loads(ai.repair_json(raw))["work"]
    for command in [r"\frac", r"\times", r"\sqrt", r"\beta", r"\neq", r"\underline"]:
        assert command in text
    assert "\x0c" not in text and "\t" not in text


class FakeModels:
    def __init__(self, outcomes):
        self.outcomes, self.calls = list(outcomes), []

    def generate_content(self, model, contents, config):
        self.calls.append(model)
        outcome = self.outcomes.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return SimpleNamespace(text=outcome)


def use_fake(monkeypatch, outcomes):
    models = FakeModels(outcomes)
    monkeypatch.setattr(ai, "_client", lambda: SimpleNamespace(models=models))
    return models


def test_busy_model_falls_back_to_backup(app, monkeypatch):
    busy = errors.ServerError(503, {"error": {"message": "high demand", "status": "UNAVAILABLE"}})
    models = use_fake(monkeypatch, [busy, GOOD_JSON])
    with app.app_context():
        result = real_solve_text("2+2")
    assert models.calls == ["gemini-flash-latest", "gemini-flash-lite-latest"]
    assert result.problems[0].topic == "Algebra"


def test_unreadable_reply_also_falls_back(app, monkeypatch):
    use_fake(monkeypatch, ["not json at all", GOOD_JSON])
    with app.app_context():
        assert len(real_solve_text("2+2").problems) == 1


def test_rate_limit_gives_a_friendly_message(app, monkeypatch):
    limited = errors.ClientError(429, {"error": {"message": "quota", "status": "RESOURCE_EXHAUSTED"}})
    use_fake(monkeypatch, [limited, limited])
    with app.app_context(), pytest.raises(ai.AIError, match="usage limit"):
        real_solve_text("2+2")


def test_bad_key_stops_without_retrying(app, monkeypatch):
    bad_key = errors.ClientError(400, {"error": {"message": "API key not valid", "status": "INVALID_ARGUMENT"}})
    models = use_fake(monkeypatch, [bad_key, GOOD_JSON])
    with app.app_context(), pytest.raises(ai.AIError, match="GEMINI_API_KEY"):
        real_solve_text("2+2")
    assert len(models.calls) == 1


def test_missing_key_is_explained(app):
    app.config["GEMINI_API_KEY"] = ""
    with app.app_context(), pytest.raises(ai.AIError, match="not set up"):
        real_solve_text("2+2")


def test_the_solver_asks_for_the_full_working_and_mentions_no_level(app, monkeypatch):
    seen = {}

    class Recorder(FakeModels):
        def generate_content(self, model, contents, config):
            seen["instructions"] = config.system_instruction
            return super().generate_content(model, contents, config)

    models = Recorder([GOOD_JSON])
    monkeypatch.setattr(ai, "_client", lambda: SimpleNamespace(models=models))
    with app.app_context():
        real_solve_text("3x - 2 = -x + 6")
    assert '"start"' in seen["instructions"] and '"result"' in seen["instructions"] and "teachers" in seen["instructions"]
    assert "level" not in seen["instructions"].lower()
    assert set(ai.Step.model_fields) == {"title", "result", "work"} and "start" in ai.Problem.model_fields


def test_tutor_sees_the_working_lines():
    text = ai._describe([{"problem": "p", "start": "$3x = 6$", "answer": "$x = 2$",
                          "steps": [{"title": "Divide", "result": "$x = 2$", "work": "Split by 3."}]}])
    assert "Start: $3x = 6$" in text and "Step 1. Divide: $x = 2$ Split by 3." in text


def test_working_lines_without_dollar_signs_are_marked_as_math(app, monkeypatch):
    reply = json.dumps({"problems": [{"problem": "p", "topic": "Algebra", "start": "3x - 2 = -x + 6", "answer": "x = 2",
                                      "steps": [{"title": "t", "result": r"x = \frac{8}{4}", "work": "w"},
                                                {"title": "t", "result": "$x = 2$", "work": "w"}, {"title": "t", "result": "", "work": "w"}]}]})
    use_fake(monkeypatch, [reply])
    with app.app_context():
        problem = real_solve_text("3x - 2 = -x + 6").problems[0]
    assert problem.start == "$3x - 2 = -x + 6$"
    assert [step.result for step in problem.steps] == [r"$x = \frac{8}{4}$", "$x = 2$", ""]
