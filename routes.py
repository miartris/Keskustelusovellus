from app import app
from flask import render_template, redirect, url_for, request, session, flash
from os import getenv
import models

app.secret_key = getenv("SECRET_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["reg_name"]
        password = request.form["reg_password"]
        models.create_new_user(name, password)
        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["login_name"]
        password = request.form["login_password"]
        user = models.check_user_data(name, password)
        if user["is_user"]:
            session["username"] = name
            flash("Login successful")
            return redirect("/")
        else:
            flash(user["error"])
            return redirect("/login")

    else:
        return render_template("login.html")
