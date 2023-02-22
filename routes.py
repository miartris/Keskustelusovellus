from app import app
from flask import render_template, redirect, url_for, request, session, flash, abort
from os import getenv
import models
import secrets
#import requests

app.secret_key = getenv("SECRET_KEY")

@app.errorhandler(404)
def not_found(e):
    return render_template("error.html", error=404), 404 

@app.route("/")
def index():
    topics = models.get_all_topics()
    return render_template("index.html", topics=topics)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["reg_name"]
        name_stripped = name.strip()
        password = request.form["reg_password"]
        password_confirmation = request.form["reg_password_check"]
        
        if (password != password_confirmation):
            flash("Passwords don't match", "is_error")
            return redirect("/register")
        
        if (len(name) < 3 or len(name) > 25 or len(name) != len(name_stripped)):
            flash("Name must be between 3 and 25 characters long and contain no whitespace", "is_error")
            return redirect("/login")

        if (len(name) < 3 or len(name) > 25 or len(name) != len(name_stripped)):
            flash("Name must be between 3 and 25 characters long and contain no whitespace", "is_error")
            return redirect("/login")

        if (len(password) < 3 or len(password) != len(password.strip())):
            flash("Password must be longer than three characters and contain no whitespace", "is_error")
            return redirect("/login")

        models.create_new_user(name, password)
        flash("Registered successfully", "is_success")
        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["login_name"]
        password = request.form["login_password"]
        user = models.check_user_data(name, password)
        if session.get("username"):
            flash("already logged in", "is_error")
            return redirect(url_for("login"))
  
        if user["is_user"]:
            session["username"] = name
            session["user_id"] = models.get_user_id()
            session["csrf_token"] = secrets.token_hex(16)
            flash("Login successful", "is_success")
            return redirect("/")
        else:
            flash(user["error"])
            return redirect("/login")

    else:
        return render_template("login.html")

@app.route("/logout", methods=["GET"])
def logout():
    del session["username"]
    del session["csrf_token"]
    flash("Logout successful", "is_success")
    return redirect(url_for("index"))

@app.route("/<string:name>", methods=["GET", "POST"])
def topic(name):
    if request.method == "GET":
        if models.get_topic(name):
            threads = models.get_all_threads(name)
            return render_template("topic.html", topic=name, threads=threads)
        else:
            abort(404)
    if request.method == "POST":
        print(request)
        thread_title = request.form["title"]
        thread_content = request.form["content"]
        request_csrf = request.form["csrf_token"]
        if request_csrf != session.get("csrf_token"):
            abort(403)
        models.create_new_thread(thread_title, name, session.get("username"))
        id = models.get_thread_id(thread_title)

        return(redirect(f"/{name}/{id}"))
    
@app.route("/<string:topic>/<int:id>", methods=["GET", "POST"])
def thread(topic, id):
    if request.method == "GET":
        posts = models.get_all_posts(id)
        return render_template("thread.html", topic=topic, posts=posts)
    if request.method == "POST":
        models.create_new_post()
    
    