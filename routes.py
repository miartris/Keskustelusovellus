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

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        topics = models.get_topics_and_threads()
        return render_template("index.html", topics=topics)
    if request.method=="POST":
        if not session["admin"]:
            abort(403)
        else:
            title = request.form["title"]
            models.create_new_topic(title)
            flash("Success", "alert-success")
            return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["reg_name"]
        name_stripped = name.strip()
        password = request.form["reg_password"]
        password_confirmation = request.form["reg_password_check"]
        as_admin = False
        if request.form.get("admin"):
            as_admin = True
        
        if (password != password_confirmation):
            flash("Passwords don't match", "alert-danger")
            return redirect("/register")
        
        if (len(name) < 3 or len(name) > 25 or len(name) != len(name_stripped)):
            flash("Name must be between 3 and 25 characters long and contain no whitespace", "alert-danger")
            return redirect("/login")

        if (len(password) < 3 or len(password) != len(password.strip())):
            flash("Password must be longer than three characters and contain no whitespace", "alert-danger")
            return redirect("/login")

        models.create_new_user(name, password, as_admin)
        flash("Registered successfully", "alert-success")
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
            res =  models.get_user_id(session.get("username"))
            session["user_id"] = res
            session["csrf_token"] = secrets.token_hex(16)
            print(user)
            if user["admin"]:
                session["admin"] = True
            else:
                session["admin"] = False
            flash("Login successful", "alert-success")
            return redirect("/")
        else:
            flash(user["error"], "alert-danger")
            return redirect("/login")

    else:
        return render_template("login.html")

@app.route("/logout", methods=["GET"])
def logout():
    del session["username"]
    del session["csrf_token"]
    del session["user_id"]
    del session["admin"]
    flash("Logout successful", "alert-success")
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
        thread_title = request.form["title"]
        thread_content = request.form["content"]
        request_csrf = request.form["csrf_token"]
        if request_csrf != session.get("csrf_token"):
            abort(403)
        if thread_title.rstrip() == "":
            flash("Title has to contain letters", "alert-danger")
            return(redirect(f"/{name}"))
        if len(thread_title) > 50:
            flash("Title has to be smaller than 50 letters" "alert-danger")
            return(redirect(f"/{name}"))
        models.create_new_thread(thread_title, name, session.get("username"))
        id = models.get_thread_id(thread_title)
        models.create_new_post(thread_content, session.get("user_id"), id)
        return(redirect(f"/{name}/{id}"))
    
@app.route("/<string:topic>/<int:id>", methods=["GET", "POST"])
def thread(topic, id):
    if request.method == "GET":
        posts = models.get_all_posts(id)
        return render_template("thread.html", topic=topic, id=id, posts=posts)
    if request.method == "POST":
        content = request.form["content"]
        req_csrf = request.form["csrf_token"]
        if validate_post_request(req_csrf):
            models.create_new_post(content, session.get("user_id"), id)
            return redirect(f"/{topic}/{id}")
        else:
         abort(403)

@app.route("/users/<string:username>", methods=["GET", "POST"])
def profile(username):
    if request.method == "GET":
        if models.get_user_id(username):
            #models.fetch_profile_data()
            return render_template("profile.html", username=username)
        else:
            abort(404)
    if request.method == "POST":
        content = request.form["description"]
        if validate_post_request(session["csrf_token"]) \
        and validate_post_content(content, 1, 500):
            models.update_user_description(session["user_id"], content)
        else:
            flash("Description must be between 1 and 500 letters long", "alert-danger")
            return(redirect(url_for('profile', username=username)))

@app.route("/users/<string:username>/images", methods=["GET", "POST"])
def profile_image(username):
    if request.method == "GET":
        abort(404)
    if request.method == "POST":
        if username == session["username"]:
            file = request.files["file"]
            print("name", file.filename)
            print("length", len(file.read()), "bytes")
            data = file.read()
            models.upload_image(data, file.filename)
        else:
            abort(403)

def validate_post_request(req_csrf: int):
    return session.get("username") and req_csrf == session["csrf_token"]

def validate_post_content(content: str, min_length: int, max_length: int):
    return len(content) <= max_length and len(content) >= min_length and content