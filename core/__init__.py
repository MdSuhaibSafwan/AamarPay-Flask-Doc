import secrets
from flask import Flask
from flask import (
    render_template, url_for, flash, redirect
)
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_hex()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///aamarpay.db"

db = SQLAlchemy(app=app)

bcrypt = Bcrypt(app)

with app.app_context():
    db.create_all()
    print("Created")


from . import routes
