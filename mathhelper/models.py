"""Database tables for users, solutions, chats, practice and lessons."""
from datetime import datetime, timezone

from flask_login import UserMixin
from sqlalchemy import JSON, ForeignKey, LargeBinary, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db

LEVELS = ["Elementary", "Middle School", "High School", "College"]
THEMES = ["system", "light", "dark"]


def utcnow():
    """Return the current UTC time without tzinfo, which is how rows store it."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


class User(UserMixin, db.Model):
    """A student account, or the admin account when is_admin is set."""

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str | None] = mapped_column(String(255))
    google_id: Mapped[str | None] = mapped_column(String(64), unique=True)
    level: Mapped[str] = mapped_column(String(20), default="High School")
    theme: Mapped[str] = mapped_column(String(10), default="system")
    expand_steps: Mapped[bool] = mapped_column(default=True)
    sounds: Mapped[bool] = mapped_column(default=True)
    timezone: Mapped[str] = mapped_column(String(64), default="UTC")
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    is_admin: Mapped[bool] = mapped_column(default=False)
    suspended_at: Mapped[datetime | None] = mapped_column()

    solutions: Mapped[list["Solution"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    attempts: Mapped[list["PracticeAttempt"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    completions: Mapped[list["LessonCompletion"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    @property
    def is_active(self):
        """Return False while the account is suspended, which blocks signing in."""
        return self.suspended_at is None

    def set_password(self, password):
        """Store a salted hash of the password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Return True when the password matches the stored hash."""
        return bool(self.password_hash) and check_password_hash(self.password_hash, password)

    @property
    def first_name(self):
        """Return the first word of the name for friendly greetings."""
        return self.name.split()[0] if self.name.strip() else "there"

    @property
    def initials(self):
        """Return up to two initials for the avatar."""
        parts = self.name.split()
        return "".join(p[0] for p in parts[:2]).upper() or self.email[0].upper()


class Solution(db.Model):
    """One solved photo or typed question, holding one or more problems."""

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), index=True)
    source: Mapped[str] = mapped_column(String(10))
    prompt: Mapped[str | None] = mapped_column(Text)
    image_name: Mapped[str | None] = mapped_column(String(64))
    problems: Mapped[list] = mapped_column(JSON, default=list)
    topic: Mapped[str] = mapped_column(String(40), default="Math", index=True)
    note: Mapped[str | None] = mapped_column(Text)
    starred: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=utcnow, index=True)

    user: Mapped[User] = relationship(back_populates="solutions")
    messages: Mapped[list["Message"]] = relationship(
        back_populates="solution", cascade="all, delete-orphan", order_by="Message.id"
    )

    @property
    def title(self):
        """Return the first problem statement, or the typed prompt as a fallback."""
        if self.problems:
            return self.problems[0].get("problem") or "Untitled problem"
        return self.prompt or "Photo with no readable problem"

    @property
    def topics(self):
        """Return every distinct topic in this solution."""
        return list(dict.fromkeys(p.get("topic", "Math") for p in self.problems))


class Photo(db.Model):
    """A homework photo kept in the database so it survives on any host."""

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    data: Mapped[bytes] = mapped_column(LargeBinary)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)


class EmailLog(db.Model):
    """A record of each email sent, used to limit how many go out."""

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), index=True)
    kind: Mapped[str] = mapped_column(String(20))
    created_at: Mapped[datetime] = mapped_column(default=utcnow, index=True)


class LoginAttempt(db.Model):
    """A failed login, kept briefly to limit password guessing."""

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), index=True)
    network: Mapped[str] = mapped_column(String(32), index=True)
    created_at: Mapped[datetime] = mapped_column(default=utcnow, index=True)


class Message(db.Model):
    """A single turn in the tutor chat under a solution."""

    id: Mapped[int] = mapped_column(primary_key=True)
    solution_id: Mapped[int] = mapped_column(ForeignKey("solution.id"), index=True)
    role: Mapped[str] = mapped_column(String(10))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)

    solution: Mapped[Solution] = relationship(back_populates="messages")


class PracticeAttempt(db.Model):
    """A finished practice round, stored with its seed so it can be reviewed later."""

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), index=True)
    skill_id: Mapped[str] = mapped_column(String(40), index=True)
    seed: Mapped[str] = mapped_column(String(32))
    answers: Mapped[list] = mapped_column(JSON, default=list)
    correct: Mapped[int] = mapped_column(default=0)
    total: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(default=utcnow, index=True)

    user: Mapped[User] = relationship(back_populates="attempts")

    @property
    def percent(self):
        """Return the score as a whole number percentage."""
        return round(100 * self.correct / self.total) if self.total else 0


class LessonCompletion(db.Model):
    """Marks a lesson as finished by a user."""

    __table_args__ = (UniqueConstraint("user_id", "lesson_key"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), index=True)
    lesson_key: Mapped[str] = mapped_column(String(80))
    created_at: Mapped[datetime] = mapped_column(default=utcnow)

    user: Mapped[User] = relationship(back_populates="completions")


class SavedLesson(db.Model):
    """A lesson written or changed by the admin, which replaces the built in lesson with the same key."""

    __table_args__ = (UniqueConstraint("course_id", "slug"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[str] = mapped_column(String(40), index=True)
    slug: Mapped[str] = mapped_column(String(60))
    minutes: Mapped[int] = mapped_column(default=5)
    skill: Mapped[str] = mapped_column(String(40))
    content: Mapped[dict] = mapped_column(JSON, default=dict)
    published: Mapped[bool] = mapped_column(default=True)
    deleted: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)

    @property
    def visible(self):
        """Return True when students can see this lesson."""
        return self.published and not self.deleted


class SavedPractice(db.Model):
    """A practice set written or changed by the admin, which replaces the built in skill with the same id."""

    id: Mapped[int] = mapped_column(primary_key=True)
    skill_id: Mapped[str] = mapped_column(String(60), unique=True)
    level: Mapped[str] = mapped_column(String(20))
    topic: Mapped[str] = mapped_column(String(40))
    content: Mapped[dict] = mapped_column(JSON, default=dict)
    questions: Mapped[list] = mapped_column(JSON, default=list)
    published: Mapped[bool] = mapped_column(default=True)
    deleted: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=utcnow, onupdate=utcnow)

    @property
    def visible(self):
        """Return True when students can see this practice set."""
        return self.published and not self.deleted


class Setting(db.Model):
    """A small named value the app keeps for itself, such as which admin password was last applied."""

    key: Mapped[str] = mapped_column(String(40), primary_key=True)
    value: Mapped[str] = mapped_column(String(255))
