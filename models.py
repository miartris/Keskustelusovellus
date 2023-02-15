from db import db
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash

def fetch_user_data(name: str, password: str):
    query = "SELECT username, id, password FROM users WHERE username=:username"
    result = db.session.execute(query, {"username":name})
    user = result.fetchone()
    if not user:
        # case invalid        
    else:
        hashval = user.password
        if check_password_hash(hashval, password):
            pass #all good
        else:
            pass # wrong pw


def create_new_user(name: str, password: str):
    hashed_password = generate_password_hash(password, "sha256")
    query = text("INSERT INTO users (username, password) VALUES (:username, :password) ON CONFLICT DO NOTHING")
    db.session.execute(query, {"username":name, "password":hashed_password})
    db.session.commit()
    

