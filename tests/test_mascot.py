"""The mascot: assets, messages, the real events that trigger it and the 3D Beral setup."""
import json
import re
from pathlib import Path

from PIL import Image

from mathhelper import create_app
from mathhelper.mascot import MESSAGES, POSES
from mathhelper.practice import build_round

STATIC = Path(__file__).resolve().parent.parent / "public" / "static"
ASSETS = STATIC / "mascot"
ANIMATIONS = STATIC / "js" / "beral" / "animations.js"


def mascot(response):
    """Read the mascot data embedded in a page."""
    match = re.search(r'<script type="application/json" id="mascot-data">(.*?)</script>', response.get_data(as_text=True), re.S)
    return json.loads(match[1])


def test_every_state_has_a_transparent_image():
    for state in POSES:
        image = Image.open(ASSETS / f"mascot_{state}.png")
        assert image.mode == "RGBA"
        corners = [(0, 0), (image.width - 1, 0), (0, image.height - 1), (image.width - 1, image.height - 1)]
        assert all(image.getpixel(corner)[3] == 0 for corner in corners)
        assert (ASSETS / f"mascot_{state}.png").stat().st_size < 250 * 1024


def test_every_message_has_both_languages_a_known_pose_and_a_known_animation():
    states = set(re.findall(r"^  (\w+): \{ ", ANIMATIONS.read_text(encoding="utf-8"), re.M))
    assert {"idle", "welcome", "thinking", "success", "celebrate", "encourage"} <= states
    for key, (pose, animation, texts) in MESSAGES.items():
        assert pose in POSES and animation in states, key
        assert texts["en"] and texts["fr"] and len(texts["en"]) < 70 and len(texts["fr"]) < 70, key


def test_welcome_is_only_for_signed_in_users(client, logged_in):
    data = mascot(logged_in.get("/home"))
    assert data["welcome"] is True and data["event"] is None and data["duration"] == 4000
    assert data["messages"]["welcome"] == {"state": "welcome", "animation": "welcome", "text": "Welcome! Ready for some maths?"}
    assert data["messages"]["completed"]["animation"] == "success" and data["messages"]["milestone"]["animation"] == "celebrate"
    assert data["images"]["thinking"].endswith("/static/mascot/mascot_thinking.png")
    logged_in.post("/logout")
    assert mascot(logged_in.get("/"))["welcome"] is False


def test_mascot_speaks_french_when_the_app_is_in_french(logged_in):
    logged_in.get("/language/fr")
    messages = mascot(logged_in.get("/home"))["messages"]
    assert messages["welcome"]["text"].startswith("Bienvenue") and messages["correct"]["text"].startswith("Bravo")
    assert messages["saved"]["text"].startswith("Enregistré")


def test_solving_a_problem_makes_mascot_celebrate_once(logged_in):
    response = logged_in.post("/solve", data={"mode": "type", "problem": "2x + 3 = 11"}, follow_redirects=True)
    assert mascot(response)["event"] == "completed"
    assert mascot(logged_in.get("/solutions/1"))["event"] is None


def test_completing_a_lesson_makes_mascot_celebrate_and_undoing_does_not(logged_in):
    done = logged_in.post("/learn/algebra-1/solving-equations/complete", follow_redirects=True)
    assert mascot(done)["event"] == "completed"
    undone = logged_in.post("/learn/algebra-1/solving-equations/complete", follow_redirects=True)
    assert mascot(undone)["event"] is None


def test_practice_results_choose_the_big_celebration_or_encouragement(logged_in):
    seed = "0123456789abcdef"
    perfect = ",".join(str(q.answer) for q in build_round("slope", seed))
    great = logged_in.post("/practice/slope/finish", data={"seed": seed, "answers": perfect}, follow_redirects=True)
    assert mascot(great)["event"] == "milestone"
    low = logged_in.post("/practice/slope/finish", data={"seed": seed, "answers": ""}, follow_redirects=True)
    assert mascot(low)["event"] == "encourage"
    assert mascot(logged_in.get("/practice/results/1"))["event"] is None


def test_a_waiting_message_survives_background_requests(logged_in):
    logged_in.post("/solve", data={"mode": "type", "problem": "2x + 3 = 11"})
    logged_in.post("/solutions/1/ask", json={"question": "Why?"}, headers={"Accept": "application/json"})
    assert mascot(logged_in.get("/solutions/1"))["event"] == "completed"


def test_mascot_is_named_and_stands_on_the_public_screens_and_the_dashboard(client, logged_in):
    home = logged_in.get("/home").get_data(as_text=True)
    assert '<strong class="mascot-name">Beral</strong>' in home and "mascot/mascot_thinking_large.webp" in home
    logged_in.post("/logout")
    landing = client.get("/").get_data(as_text=True)
    assert 'class="demo-mascot"' in landing and landing.count("mascot/mascot_welcome_large.webp") == 2
    assert client.get("/login").get_data(as_text=True).count("mascot/mascot_welcome_large.webp") == 2
    assert client.get("/forgot-password").get_data(as_text=True).count("mascot/mascot_thinking_large.webp") == 2
    for state in ["welcome", "thinking"]:
        assert (ASSETS / f"mascot_{state}_large.webp").stat().st_size < 150 * 1024


def test_without_a_model_beral_stays_a_picture_and_three_js_is_not_loaded(logged_in):
    page = logged_in.get("/home").get_data(as_text=True)
    assert mascot(logged_in.get("/home"))["three"] is None
    assert "importmap" not in page and "three.module" not in page and "data-mascot-stage" in page


def test_with_a_model_students_get_the_3d_beral_and_the_admin_preview_reports_it(tmp_path):
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": f"sqlite:///{tmp_path / 'm.db'}", "WTF_CSRF_ENABLED": False,
                      "BERAL_MODEL_URL": "/static/mascot/beral.glb", "ADMIN_EMAIL": "boss@example.com", "ADMIN_PASSWORD": "correct-horse-battery"})
    student = app.test_client()
    student.post("/signup", data={"name": "Ama", "email": "ama@example.com", "password": "secret123"})
    page = student.get("/home").get_data(as_text=True)
    three = mascot(student.get("/home"))["three"]
    assert three == {"model": "/static/mascot/beral.glb", "module": "/static/js/beral/beral3d.js",
                     "decoders": "/static/vendor/three/addons/libs/draco/gltf/"}
    assert '<script type="importmap">' in page and "/static/vendor/three/three.module.min.js" in page
    assert student.get("/admin/beral").status_code == 403
    visitor = app.test_client()
    assert mascot(visitor.get("/"))["three"] is None
    admin = app.test_client()
    admin.post("/login", data={"email": "boss@example.com", "password": "correct-horse-battery"})
    preview = admin.get("/admin/beral").get_data(as_text=True)
    assert "createBeral" in preview and "data-play=\"celebrate\"" in preview and mascot(admin.get("/admin/"))["three"] is None


def test_the_admin_preview_explains_where_the_model_goes_while_it_is_missing(app):
    from mathhelper import schema
    with app.app_context():
        schema.ensure_admin("boss@example.com", "correct-horse-battery")
    admin = app.test_client()
    admin.post("/login", data={"email": "boss@example.com", "password": "correct-horse-battery"})
    preview = admin.get("/admin/beral").get_data(as_text=True)
    assert "No 3D model is installed yet" in preview and "public/static/mascot/beral.glb" in preview and "createBeral" not in preview


def test_three_js_and_the_beral_modules_ship_with_the_app():
    for name in ["vendor/three/three.module.min.js", "vendor/three/addons/loaders/GLTFLoader.js", "vendor/three/addons/loaders/DRACOLoader.js",
                 "vendor/three/addons/utils/BufferGeometryUtils.js", "vendor/three/addons/libs/meshopt_decoder.module.js",
                 "vendor/three/addons/libs/draco/gltf/draco_decoder.wasm", "vendor/three/addons/libs/draco/gltf/draco_wasm_wrapper.js",
                 "vendor/three/LICENSE", "js/beral/beral3d.js", "js/beral/animations.js"]:
        assert (STATIC / name).is_file(), name
    engine = (STATIC / "js/beral/beral3d.js").read_text(encoding="utf-8")
    for needed in ["AnimationMixer", "crossFadeFrom", "LoopOnce", "isSkinnedMesh", "visibilitychange", "dispose()"]:
        assert needed in engine, needed
