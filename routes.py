from app import app
from flask import render_template, redirect, url_for, request, session, flash, abort, make_response
from os import getenv
from models.forum import *
from models.stats import *
from models.users import *
import secrets
import base64
#import requests

app.secret_key = getenv("SECRET_KEY")

@app.errorhandler(404)
def not_found(e):
    return render_template("error.html", error=404), 404 

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        topics = get_topics_and_threads()
        stats = get_total_statistics()
        return render_template("index.html", topics=topics, data=stats)
    if request.method=="POST":
        if not session["admin"]:
            abort(403)
        else:
            title = request.form["title"]
            if not validate_post_content(title, 1, 40) and validate_post_request(request.form["csrf_token"]):
                flash("min 1 max 40 letters", "alert-danger")
                return redirect("/")
            create_new_topic(title)
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
            return redirect("/register")

        if (len(password) < 3 or len(password) != len(password.strip())):
            flash("Password must be longer than three characters and contain no whitespace", "alert-danger")
            return redirect("/register")

        res = create_new_user(name, password, as_admin)
        if res:
            flash("Registered successfully", "alert-success")
            return redirect("/login")
        else:
            flash("Registration failed, name could be in use", "alert-danger")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["login_name"]
        password = request.form["login_password"]
        user = check_user_data(name, password)
        if session.get("username"):
            flash("already logged in", "is_error")
            return redirect(url_for("login"))
  
        if user["is_user"]:
            session["username"] = name
            res =  get_user_id(session.get("username"))
            session["user_id"] = res
            session["csrf_token"] = secrets.token_hex(16)
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
        if get_topic(name):
            threads = get_all_threads(name)
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
        create_new_thread(thread_title, name, session.get("username"))
        id = get_thread_id(thread_title)
        create_new_post(thread_content, session.get("user_id"), id)
        return(redirect(f"/{name}/{id}"))
    
@app.route("/<string:topic>/<int:id>", methods=["GET", "POST"])
def thread(topic, id):
    if request.method == "GET":
        posts = get_all_posts(id)
        return render_template("thread.html", topic=topic, id=id, posts=posts)
    if request.method == "POST":
        content = request.form["content"]
        req_csrf = request.form["csrf_token"]
        if validate_post_request(req_csrf):
            create_new_post(content, session.get("user_id"), id)
            return redirect(f"/{topic}/{id}")
        else:
         abort(403)

@app.route("/users/<string:username>", methods=["GET", "POST"])
def profile(username):
    if request.method == "GET":
        id = get_user_id(username)
        if id:
            data = get_profile_data(id)
            imgdata = get_image_by_user(id)
            img = convert_img_to_bas64str(imgdata)
            return render_template("profile.html", username=username, data=data, pimg=img)
        else:
            abort(404)
    if request.method == "POST":
        content = request.form["description"]
        if validate_post_request(session["csrf_token"]) \
        and validate_post_content(content, 1, 500) \
        and username == session["username"]:
            update_user_description(session["user_id"], content)
            return redirect(url_for('profile', username=username))
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
            filename = file.filename
            if not file or not filename.endswith(".jpg"):
                flash("Enter a JPG-file max 10mb", "alert-danger")
                return redirect(f"/users/{username}")
            data = file.read()
            if len(data) > 1024 * 10**5:
                flash("File larger than 10mb", "alert-danger")
            upload_profile_image(data, session["user_id"], filename)
            associate_img_to_user(session["user_id"])
            return(redirect(request.referrer))
        else:
            abort(403)

@app.route("/posts/<int:id>/upvotes", methods=["POST"])
def add_upvote(id: int):
    increment_upvote(id, 1)
    return(redirect(request.referrer))

@app.route("/users/<string:username>/description", methods=["POST"])
def description(username):
    csrf = request.form["csrf_token"]
    data = request.form["description"]
    if username != session["username"]:
        abort(403)
    if validate_post_content(data, 1, 200) and validate_post_request(csrf):
        update_user_description(session["user_id"], data)
        return redirect(request.referrer)
    else:
        flash("Description must be between 1-200 letters", "alert-danger")
        return redirect(request.referrer)

def validate_post_request(req_csrf: int):
    return session.get("username") and req_csrf == session["csrf_token"]

def validate_post_content(content: str, min_length: int, max_length: int):
    return len(content) <= max_length and len(content) >= min_length and content.rstrip != 0

def convert_img_to_bas64str(data: bytearray):
    img_in_base64 = base64.b64encode(data[0]).decode("utf-8") if data else None
    return img_in_base64

