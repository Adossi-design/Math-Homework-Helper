"""Shared fixtures that build an isolated app with a fake AI."""
import io

import pytest
from PIL import Image

from mathhelper import ai, create_app, mailer, schema
from mathhelper.extensions import db
from mathhelper.models import User


def fake_result(topic="Algebra"):
    """Return a small structured solution like the AI would."""
    return ai.SolveResult(problems=[ai.Problem(
        problem="Solve $2x + 3 = 11$", topic=topic, start="$2x + 3 = 11$", answer="$x = 4$",
        steps=[ai.Step(title="Subtract 3", result="$2x = 8$", work="Take $3$ from both sides."),
               ai.Step(title="Divide by 2", result="$x = 4$", work="Halve both sides.")],
        tip="Undo addition before multiplication.",
    )])


@pytest.fixture
def app(tmp_path, monkeypatch):
    monkeypatch.setattr(ai, "solve_text", lambda text, grade=None: fake_result())
    monkeypatch.setattr(ai, "solve_image", lambda data, grade=None: fake_result("Fractions"))
    monkeypatch.setattr(ai, "ask_tutor", lambda problems, history, question, grade=None: f"Here is help with **{question}** and $x^2$.")
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{tmp_path / 'test.db'}",
        "WTF_CSRF_ENABLED": False,
        "GEMINI_API_KEY": "test-key",
        "GOOGLE_CLIENT_ID": "",
        "GOOGLE_CLIENT_SECRET": "",
        "RESEND_API_KEY": "test-mail-key",
        "SMTP_USER": "",
        "SMTP_PASSWORD": "",
        "SUPPORT_EMAIL": "",
        "ADMIN_EMAIL": "",
        "ADMIN_PASSWORD": "",
    })
    app.outbox = []
    monkeypatch.setattr(mailer, "send_email", lambda to, subject, html, text: app.outbox.append({"to": to, "subject": subject, "html": html, "text": text}))
    yield app


@pytest.fixture
def outbox(app):
    """Return the list of emails the app tried to send."""
    return app.outbox


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def make_user(app):
    def make(email="ama@example.com", password="secret123", name="Ama Mensah", grade="4e"):
        with app.app_context():
            user = User(name=name, email=email, grade=grade)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return user.id
    return make


@pytest.fixture
def logged_in(client, make_user):
    make_user()
    client.post("/login", data={"email": "ama@example.com", "password": "secret123"})
    return client


@pytest.fixture
def admin(app):
    """Create the admin account and return a separate browser signed in as the admin."""
    with app.app_context():
        schema.ensure_admin("boss@example.com", "correct-horse-battery")
    browser = app.test_client()
    browser.post("/login", data={"email": "boss@example.com", "password": "correct-horse-battery"})
    return browser


@pytest.fixture
def png_bytes():
    buffer = io.BytesIO()
    Image.new("RGBA", (300, 200), (255, 0, 0, 128)).save(buffer, "PNG")
    return buffer.getvalue()
