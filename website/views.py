from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import ContactUs
from . import db
import json

# from my_module import my_function
import sys
from pathlib import Path

# Add the current directory to the Python import paths
current_directory = Path(__file__).resolve().parent
sys.path.append(str(current_directory))

# Import your function
from my_module import my_function

views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html", user=current_user)


@views.route("/graph", methods=["GET", "POST"])
@login_required
def graph():
    return render_template("graph.html", user=current_user)


@views.route("/equifolio.ai", methods=["GET", "POST"])
def home():
    return render_template("index.html", user=current_user)


@views.route("/portfolio", methods=["GET", "POST"])
def portfolio():
    return render_template("portfolio.html", user=current_user)


@views.route("/boxes", methods=["GET", "POST"])
def boxes():
    return render_template("boxes.html", user=current_user)


@views.route("/investopedia", methods=["GET", "POST"])
def investopedia():
    result = None
    if request.method == "POST":
        data = request.form["data"]
        result = my_function(data)
    return render_template("investopedia.html", result=result, user=current_user)


@views.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        ContactUs = request.form.get("ContactUs")  # Gets the ContactUs from the HTML

        if len(ContactUs) < 1:
            flash("ContactUs is too short!", category="error")
        else:
            new_ContactUs = ContactUs(
                data=ContactUs, user_id=current_user.id
            )  # providing the schema for the ContactUs
            db.session.add(new_ContactUs)  # adding the ContactUs to the database
            db.session.commit()
            flash("ContactUs added!", category="success")

    return render_template("contact.html", user=current_user)


@views.route("/about", methods=["GET", "POST"])
def about():
    return render_template("AboutUs.html", user=current_user)


# @views.route("/manam")
# def manam():
#     return render_template("manam.html")


# @views.route("/process", methods=["POST"])
# def process():
#     data = request.form["data"]
#     result = my_function(data)
#     return render_template("result.html", result=result)


@views.route("/manam", methods=["GET", "POST"])
def manam():
    result = None
    if request.method == "POST":
        data = request.form["data"]
        result = my_function(data)
    return render_template("manam.html", result=result)
