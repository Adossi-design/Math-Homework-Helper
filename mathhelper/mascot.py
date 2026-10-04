"""Beral, the small mascot who greets, celebrates and encourages, as a 3D character or a picture."""
from flask import current_app, session, url_for

from .config import STATIC_DIR
from .i18n import language, polish

NAME = "Beral"
DURATION_MS = 4000
POSES = ["welcome", "celebrate", "encourage", "thinking"]
MODEL_FILE = "mascot/beral.glb"

# Each message names the picture pose, the 3D animation and the text in every language. Edit the text here.
MESSAGES = {
    "welcome": ("welcome", "welcome", {
        "en": "Welcome! Ready for some maths?",
        "fr": "Bienvenue ! Prêt pour un peu de maths ?",
    }),
    "welcome_back": ("welcome", "welcome", {
        "en": "Good to see you. Let's make progress today.",
        "fr": "Quel plaisir de te revoir. Faisons des progrès aujourd'hui.",
    }),
    "correct": ("celebrate", "success", {
        "en": "Nice work! You got it.",
        "fr": "Bravo ! Tu as réussi.",
    }),
    "completed": ("celebrate", "success", {
        "en": "Great job. That's another step forward.",
        "fr": "Excellent travail. Encore un pas en avant.",
    }),
    "milestone": ("celebrate", "celebrate", {
        "en": "Brilliant round! You really know this.",
        "fr": "Superbe partie ! Tu maîtrises le sujet.",
    }),
    "encourage": ("encourage", "encourage", {
        "en": "Keep going. You're making progress.",
        "fr": "Continue. Tu progresses.",
    }),
    "saved": ("encourage", "encourage", {
        "en": "Saved! You can come back to it anytime.",
        "fr": "Enregistré ! Tu pourras y revenir quand tu veux.",
    }),
    "wrong": ("thinking", "encourage", {
        "en": "Almost there. Check your steps and try again.",
        "fr": "Presque ! Vérifie tes étapes et réessaie.",
    }),
    "reminder": ("thinking", "encourage", {
        "en": "Take your time. Accuracy matters more than speed.",
        "fr": "Prends ton temps. La précision compte plus que la vitesse.",
    }),
}


def model_found():
    """Return True when the rigged Beral model file is in the static folder."""
    return (STATIC_DIR / MODEL_FILE).is_file()


def model_url():
    """Return the address of the 3D Beral model, or None while there is no model."""
    configured = current_app.config.get("BERAL_MODEL_URL")
    if configured:
        return configured
    return url_for("static", filename=MODEL_FILE) if current_app.config.get("BERAL_MODEL_FOUND") else None


def three_d():
    """Return what the browser needs to load the 3D Beral, or None while there is no model."""
    url = model_url()
    if url is None:
        return None
    return {
        "model": url,
        "module": url_for("static", filename="js/beral/beral3d.js"),
        "decoders": url_for("static", filename="vendor/three/addons/libs/draco/gltf/"),
    }


def queue(key):
    """Ask the mascot to speak on the next page the user sees."""
    session["mascot"] = key


def payload(enabled):
    """Return what the page needs to show the mascot, and clear any message that was waiting."""
    lang = language()
    return {
        "lang": lang,
        "duration": DURATION_MS,
        "welcome": bool(enabled),
        "event": session.pop("mascot", None),
        "images": {pose: url_for("static", filename=f"mascot/mascot_{pose}.png") for pose in POSES},
        "three": three_d() if enabled else None,
        "messages": {
            key: {"state": pose, "animation": animation, "text": polish(texts.get(lang, texts["en"]), lang)}
            for key, (pose, animation, texts) in MESSAGES.items()
        },
    }
