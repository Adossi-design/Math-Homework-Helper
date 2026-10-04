"""Shared Flask extensions created once and bound in the app factory."""
from authlib.integrations.flask_client import OAuth
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for every database model."""


db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
csrf = CSRFProtect()
oauth = OAuth()
