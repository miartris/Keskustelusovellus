from db import db
from sqlalchemy.sql import text

def fetch_user_data(name: str):
    query = "SELECT username, id, password FROM users WHERE username=:username"
    result = db.session.execute(query, {"username":name})

def create_new_user(name: str, hashed_password: str):
    query = text("INSERT INTO users (username, password) VALUES (:username, :password)")
    db.session.execute(query, {"username":name, "password":hashed_password})
    db.session.commit()
    

