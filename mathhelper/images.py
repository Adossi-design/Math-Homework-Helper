"""Validation and storage for uploaded homework photos."""
import uuid
from io import BytesIO

from PIL import Image, ImageOps, UnidentifiedImageError
from sqlalchemy import delete, select

from .extensions import db
from .i18n import gettext as _
from .models import Photo

MAX_SIDE = 1600


class ImageError(Exception):
    """Raised when an upload is not a usable picture."""


def prepare_image(stream):
    """Check the upload and return it as a compact, upright JPEG."""
    try:
        image = Image.open(stream)
        image.load()
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as exc:
        raise ImageError(_("That file does not look like a photo. Please use a JPG, PNG or WebP image.")) from exc

    # Rotate phone photos upright and flatten transparency onto white.
    image = ImageOps.exif_transpose(image)
    if image.mode in ("RGBA", "LA", "P"):
        image = image.convert("RGBA")
        background = Image.new("RGB", image.size, "white")
        background.paste(image, mask=image.getchannel("A"))
        image = background
    image = image.convert("RGB")
    image.thumbnail((MAX_SIDE, MAX_SIDE))

    buffer = BytesIO()
    image.save(buffer, "JPEG", quality=85, optimize=True)
    return buffer.getvalue()


def save_image(data):
    """Queue JPEG bytes for storage and return the new photo name."""
    name = f"{uuid.uuid4().hex}.jpg"
    db.session.add(Photo(name=name, data=data))
    return name


def load_image(name):
    """Return the stored bytes for a photo, or None."""
    return db.session.scalar(select(Photo.data).where(Photo.name == name))


def delete_image(name):
    """Queue a stored photo for removal."""
    if name:
        db.session.execute(delete(Photo).where(Photo.name == name))
