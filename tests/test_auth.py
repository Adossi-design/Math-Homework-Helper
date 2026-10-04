"""Sign up, log in, log out and access control."""
from mathhelper import create_app


def test_landing_is_public_and_app_pages_need_login(client):
    assert client.get("/").status_code == 200
    for path in ["/home", "/solve", "/library", "/learn/", "/practice/", "/settings/"]:
        response = client.get(path)
        assert response.status_code == 302
        assert "/login" in response.location


def test_signup_validates_input(client):
    response = client.post("/signup", data={"name": "", "email": "bad", "password": "short"})
    html = response.get_data(as_text=True)
    assert "Please tell us your name." in html
    assert "Enter a valid email address." in html
    assert "Use at least 8 characters." in html


def test_signup_logs_in_and_blocks_duplicates(client):
    data = {"name": "Kofi", "email": "Kofi@Example.com", "password": "longpassword", "timezone": "Africa/Kigali"}
    response = client.post("/signup", data=data)
    assert response.status_code == 302 and response.location.endswith("/home")
    assert "Kofi" in client.get("/home").get_data(as_text=True)
    client.post("/logout")
    again = client.post("/signup", data=data).get_data(as_text=True)
    assert "already exists" in again


def test_login_rejects_wrong_password(client, make_user):
    make_user()
    response = client.post("/login", data={"email": "ama@example.com", "password": "nope"})
    assert "do not match" in response.get_data(as_text=True)


def test_login_follows_only_safe_next_links(client, make_user):
    make_user()
    good = client.post("/login?next=/library", data={"email": "ama@example.com", "password": "secret123"})
    assert good.location.endswith("/library")
    client.post("/logout")
    bad = client.post("/login?next=https://evil.example", data={"email": "ama@example.com", "password": "secret123"})
    assert bad.location.endswith("/home")


def test_logout_ends_the_session(logged_in):
    assert logged_in.post("/logout").status_code == 302
    assert logged_in.get("/home").status_code == 302


def test_login_page_says_welcome_back_only_after_a_first_sign_in(client, make_user):
    make_user()
    first = client.get("/login").get_data(as_text=True)
    assert "<h1>Welcome</h1>" in first and "Welcome back" not in first
    client.post("/login", data={"email": "ama@example.com", "password": "nope"})
    assert "Welcome back" not in client.get("/login").get_data(as_text=True)
    client.post("/login", data={"email": "ama@example.com", "password": "secret123"})
    client.post("/logout")
    assert "<h1>Welcome back</h1>" in client.get("/login").get_data(as_text=True)


def test_phones_and_tablets_can_log_out_from_the_top_bar_and_settings(logged_in):
    home = logged_in.get("/home").get_data(as_text=True)
    assert 'class="account-menu"' in home and home.count('action="/logout"') == 2
    assert 'class="settings-logout touch-only"' in logged_in.get("/settings/").get_data(as_text=True)


def test_google_routes_hidden_without_keys(client):
    assert client.get("/login/google").status_code == 404
    assert "Continue with Google" not in client.get("/login").get_data(as_text=True)


def test_csrf_protects_forms(tmp_path):
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": f"sqlite:///{tmp_path / 'csrf.db'}",
                      "GOOGLE_CLIENT_ID": "", "GOOGLE_CLIENT_SECRET": "",
                      "SMTP_USER": "", "SMTP_PASSWORD": ""})
    response = app.test_client().post("/login", data={"email": "a@b.co", "password": "x"})
    assert response.status_code == 400
