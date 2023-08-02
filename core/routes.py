from flask import render_template, request
from . import app


app.route("/", methods=["GET", ])
def index_page():

    return render_template("main/index.html")
