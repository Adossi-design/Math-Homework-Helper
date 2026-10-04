"""WSGI entry point used by Vercel and other hosts."""
from flask import Flask

from mathhelper import create_app

app: Flask = create_app()
