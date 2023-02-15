from db import db
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash

def check_user_data(name: str, password: str):
    query = text("SELECT username, id, password FROM users WHERE username=:username")
    result = db.session.execute(query, {"username":name})
    user = result.fetchone()
    user_object = {"is_user": False, "username": name, "error": None}
    if not user:
        user_object["error"] = "No such user"        
    else:
        hashval = user.password
        if check_password_hash(hashval, password):
            user_object["is_user"] = True
        else:
            user_object["error"] = "Wrong password"
    return user_object


def create_new_user(name: str, password: str):
    hashed_password = generate_password_hash(password, "sha256")
    query = text("INSERT INTO users (username, password) VALUES (:username, :password) ON CONFLICT DO NOTHING")
    db.session.execute(query, {"username":name, "password":hashed_password})
    db.session.commit()
    

