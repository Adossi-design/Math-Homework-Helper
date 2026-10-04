"""Forgot password emails, reset links and photo storage."""
import io
import re
from types import SimpleNamespace

import pytest

from mathhelper import mailer
from mathhelper.config import _database_url
from mathhelper.extensions import db
from mathhelper.mailer import send_email as real_send_email
from mathhelper.models import Photo


def ask_for_reset(client, email="ama@example.com"):
    return client.post("/forgot-password", data={"email": email}).get_data(as_text=True)


def link_from(outbox):
    return re.search(r"http://localhost(/reset-password/\S+)", outbox[-1]["text"])[1]


def test_full_reset_flow(client, make_user, outbox):
    make_user()
    assert "Check your email" in ask_for_reset(client, "Ama@Example.com")
    assert len(outbox) == 1 and outbox[0]["to"] == "ama@example.com"
    assert "Reset your" in outbox[0]["subject"] and "Hi Ama" in outbox[0]["html"]

    link = link_from(outbox)
    assert client.get(link).status_code == 200
    assert "do not match" in client.post(link, data={"password": "newpass99", "confirm": "other"}).get_data(as_text=True)
    assert client.post(link, data={"password": "newpass99", "confirm": "newpass99"}).location.endswith("/home")
    assert client.get("/home").status_code == 200

    # The link stops working once the password has changed.
    client.post("/logout")
    assert client.get(link).location.endswith("/forgot-password")
    assert "do not match" in client.post("/login", data={"email": "ama@example.com", "password": "secret123"}).get_data(as_text=True)
    assert client.post("/login", data={"email": "ama@example.com", "password": "newpass99"}).location.endswith("/home")


def test_unknown_email_is_explained_and_no_email_is_sent(client, outbox):
    assert "No account uses that email" in ask_for_reset(client, "nobody@example.com")
    assert outbox == []
    assert "valid email" in ask_for_reset(client, "not-an-email")


def test_reset_emails_are_limited_per_hour(client, make_user, outbox):
    make_user()
    for _ in range(5):
        assert "Check your email" in ask_for_reset(client)
    assert len(outbox) == 3


def test_tampered_and_expired_links_are_refused(client, make_user, outbox, monkeypatch):
    make_user()
    ask_for_reset(client)
    link = link_from(outbox)
    assert client.get(link[:-3] + "abc").location.endswith("/forgot-password")
    monkeypatch.setattr(mailer, "RESET_MINUTES", -1)
    assert client.get(link).location.endswith("/forgot-password")


def test_failed_send_and_missing_key_are_explained(app, client, make_user, monkeypatch):
    make_user()

    def broken(*args):
        raise mailer.MailError("refused")
    monkeypatch.setattr(mailer, "send_email", broken)
    assert "could not send the email" in ask_for_reset(client).lower()
    app.config["RESEND_API_KEY"] = ""
    assert "not set up yet" in ask_for_reset(client)


def test_send_email_talks_to_resend(app, monkeypatch):
    calls = []

    def fake_post(url, json, headers, timeout):
        calls.append((url, json, headers))
        return SimpleNamespace(status_code=200 if len(calls) == 1 else 403, text="domain is not verified")
    monkeypatch.setattr(mailer.requests, "post", fake_post)
    with app.app_context():
        real_send_email("ama@example.com", "Hello", "<p>Hi</p>", "Hi")
        with pytest.raises(mailer.MailError):
            real_send_email("ama@example.com", "Hello", "<p>Hi</p>", "Hi")
    url, payload, headers = calls[0]
    assert url == "https://api.resend.com/emails" and headers["Authorization"] == "Bearer test-mail-key"
    assert payload["to"] == ["ama@example.com"] and payload["from"].endswith("<onboarding@resend.dev>")


def test_photos_live_in_the_database_and_are_removed_with_the_solution(app, logged_in, png_bytes):
    logged_in.post("/solve", data={"mode": "photo", "photo": (io.BytesIO(png_bytes), "hw.png")}, content_type="multipart/form-data")
    with app.app_context():
        photo = db.session.scalar(db.select(Photo))
        assert photo.data[:3] == b"\xff\xd8\xff"
    logged_in.post("/solutions/1/delete")
    with app.app_context():
        assert db.session.scalar(db.select(db.func.count()).select_from(Photo)) == 0


def test_database_url_is_normalized_for_postgres(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgres://u:p@host/db?sslmode=require")
    assert _database_url() == "postgresql+psycopg://u:p@host/db?sslmode=require"
    monkeypatch.setenv("DATABASE_URL", "postgresql://u:p@host/db")
    assert _database_url() == "postgresql+psycopg://u:p@host/db"


class FakeMailbox:
    """Stand in for smtplib.SMTP_SSL that records what the app does."""
    sent = []

    def __init__(self, host, port, timeout):
        self.host, self.port = host, port

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def login(self, user, password):
        if password == "wrongpassword":
            raise mailer.smtplib.SMTPAuthenticationError(535, b"bad credentials")
        self.login_used = (user, password)

    def send_message(self, message):
        FakeMailbox.sent.append((self.host, self.port, self.login_used, message))


def test_gmail_is_used_when_a_mailbox_login_is_set(app, monkeypatch):
    FakeMailbox.sent = []
    monkeypatch.setattr(mailer.smtplib, "SMTP_SSL", FakeMailbox)
    monkeypatch.setattr(mailer.requests, "post", lambda *a, **k: pytest.fail("Resend should not be called"))
    app.config.update(SMTP_USER="helper@gmail.com", SMTP_PASSWORD="abcdefghijklmnop")
    with app.app_context():
        assert mailer.mail_provider().startswith("Gmail")
        real_send_email("student@example.com", "Hello", "<p>Hi there</p>", "Hi there")
    host, port, login, message = FakeMailbox.sent[0]
    assert (host, port) == ("smtp.gmail.com", 465) and login == ("helper@gmail.com", "abcdefghijklmnop")
    assert message["To"] == "student@example.com" and message["From"] == "Math Homework Helper <helper@gmail.com>"
    assert message.get_body(("html",)).get_content().strip() == "<p>Hi there</p>"
    assert message.get_body(("plain",)).get_content().strip() == "Hi there"


def test_gmail_login_failure_becomes_a_mail_error(app, monkeypatch):
    monkeypatch.setattr(mailer.smtplib, "SMTP_SSL", FakeMailbox)
    app.config.update(SMTP_USER="helper@gmail.com", SMTP_PASSWORD="wrongpassword")
    with app.app_context(), pytest.raises(mailer.MailError):
        real_send_email("student@example.com", "Hello", "<p>Hi</p>", "Hi")


def test_app_password_spaces_are_removed(monkeypatch):
    from mathhelper.config import load_settings
    monkeypatch.setenv("SMTP_PASSWORD", "abcd efgh ijkl mnop")
    assert load_settings()["SMTP_PASSWORD"] == "abcdefghijklmnop"


def test_gmail_messages_carry_standard_headers(app, monkeypatch):
    FakeMailbox.sent = []
    monkeypatch.setattr(mailer.smtplib, "SMTP_SSL", FakeMailbox)
    app.config.update(SMTP_USER="helper@gmail.com", SMTP_PASSWORD="abcdefghijklmnop", SUPPORT_EMAIL="help@example.com")
    with app.app_context():
        real_send_email("student@example.com", "Hello", "<p>Hi</p>", "Hi")
    message = FakeMailbox.sent[0][3]
    assert message["Date"] and message["Message-ID"].endswith("@gmail.com>") and message["Reply-To"] == "help@example.com"
