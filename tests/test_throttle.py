"""Limits on failed logins."""
from datetime import timedelta

from mathhelper.extensions import db
from mathhelper.models import LoginAttempt, utcnow

GOOD = {"email": "ama@example.com", "password": "secret123"}
BAD = {"email": "ama@example.com", "password": "wrong"}
ELSEWHERE = {"REMOTE_ADDR": "203.0.113.9"}


def fail(client, times, data=BAD, **kwargs):
    return [client.post("/login", data=data, **kwargs) for _ in range(times)][-1]


def test_five_wrong_passwords_lock_the_login(client, make_user):
    make_user()
    assert fail(client, 4).status_code == 200
    fifth = fail(client, 1)
    assert fifth.status_code == 200 and "Too many attempts" in fifth.get_data(as_text=True)
    blocked = client.post("/login", data=GOOD)
    assert blocked.status_code == 429 and "Please wait 15 minutes" in blocked.get_data(as_text=True)
    assert client.get("/home").status_code == 302


def test_lock_is_per_visitor_so_the_owner_can_still_log_in(client, make_user):
    make_user()
    fail(client, 5)
    assert client.post("/login", data=GOOD, environ_base=ELSEWHERE).location.endswith("/home")


def test_lock_ends_after_the_window(app, client, make_user):
    make_user()
    fail(client, 5)
    with app.app_context():
        for attempt in db.session.scalars(db.select(LoginAttempt)):
            attempt.created_at = utcnow() - timedelta(minutes=16)
        db.session.commit()
    assert client.post("/login", data=GOOD).location.endswith("/home")


def test_success_clears_earlier_failures(app, client, make_user):
    make_user()
    fail(client, 3)
    client.post("/login", data=GOOD)
    client.post("/logout")
    with app.app_context():
        assert db.session.scalar(db.select(db.func.count()).select_from(LoginAttempt)) == 0
    assert fail(client, 4).status_code == 200


def test_many_visitors_guessing_one_account_lock_it_everywhere(client, make_user):
    make_user()
    for visitor in range(4):
        fail(client, 4, environ_base={"REMOTE_ADDR": f"198.51.100.{visitor}"})
    assert client.post("/login", data=GOOD, environ_base=ELSEWHERE).status_code == 429


def test_one_visitor_guessing_many_accounts_is_blocked(client, make_user):
    make_user()
    for number in range(30):
        client.post("/login", data={"email": f"user{number}@example.com", "password": "guess"})
    assert client.post("/login", data=GOOD).status_code == 429


def test_password_reset_unlocks_the_account(client, make_user, outbox):
    import re
    make_user()
    fail(client, 5)
    client.post("/forgot-password", data={"email": "ama@example.com"})
    link = re.search(r"http://localhost(/reset-password/\S+)", outbox[-1]["text"])[1]
    assert client.post(link, data={"password": "brandnew99", "confirm": "brandnew99"}).location.endswith("/home")
    client.post("/logout")
    assert client.post("/login", data={"email": "ama@example.com", "password": "brandnew99"}).location.endswith("/home")


def test_network_address_is_not_stored_in_plain_text(app, client, make_user):
    make_user()
    fail(client, 1, environ_base=ELSEWHERE)
    with app.app_context():
        stored = db.session.scalar(db.select(LoginAttempt.network))
    assert "203.0.113.9" not in stored and len(stored) == 32


def test_lock_message_is_translated(client, make_user):
    make_user()
    client.get("/language/fr")
    assert "Trop de tentatives" in fail(client, 5).get_data(as_text=True)
