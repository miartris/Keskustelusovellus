from app import app
from flask import Flask, render_template, redirect, url_for, request
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash
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
        hashed_pw = generate_password_hash(password)
        models.create_new_user(name, hashed_pw)
        # ToDo: Handle error from duplicate usernames
        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["login_name"]
        password = request.form["login_password"]
        models.fetch_user_data(name)
        
    else:
        return render_template("login.html")
