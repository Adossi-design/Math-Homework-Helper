"""Helpers for showing stored UTC times in the student's own time zone."""
from datetime import datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from flask_login import current_user

from .i18n import format_date
from .i18n import gettext as _
from .i18n import ngettext


def zone_for(user=None):
    """Return the time zone of the given or current user, falling back to UTC."""
    user = user or (current_user if current_user and current_user.is_authenticated else None)
    try:
        return ZoneInfo(user.timezone) if user and user.timezone else ZoneInfo("UTC")
    except (ZoneInfoNotFoundError, ValueError):
        return ZoneInfo("UTC")


def is_valid_zone(name):
    """Return True when the name is a real IANA time zone."""
    try:
        ZoneInfo(name)
        return True
    except (ZoneInfoNotFoundError, ValueError):
        return False


def to_local(moment, user=None):
    """Convert a naive UTC datetime into the user's local time."""
    return moment.replace(tzinfo=timezone.utc).astimezone(zone_for(user))


def local_now(user=None):
    """Return the current time in the user's time zone."""
    return datetime.now(zone_for(user))


def time_ago(moment):
    """Describe a past UTC datetime in friendly words like 5 minutes ago."""
    seconds = int((datetime.now(timezone.utc).replace(tzinfo=None) - moment).total_seconds())
    for size, unit in ((86400 * 7, "week"), (86400, "day"), (3600, "hour"), (60, "minute")):
        if seconds >= size:
            count = seconds // size
            if unit == "week" and count > 4:
                return format_date(to_local(moment))
            if unit == "day" and count == 1:
                return _("yesterday")
            return ngettext(f"{{n}} {unit} ago", f"{{n}} {unit}s ago", count)
    return _("just now")


def greeting(user=None):
    """Return a greeting that matches the time of day."""
    hour = local_now(user).hour
    if hour < 12:
        return _("Good morning")
    if hour < 18:
        return _("Good afternoon")
    return _("Good evening")
