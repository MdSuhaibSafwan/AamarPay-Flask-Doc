import secrets
from flask import Flask
from flask import (
    render_template, url_for, flash, redirect
)
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_hex()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///aamarpay.db"

db = SQLAlchemy(app=app)

from . import routes
