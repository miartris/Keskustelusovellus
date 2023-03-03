from db import db
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash

def check_user_data(name: str, password: str):
    query = text("SELECT username, user_id, password FROM users WHERE username=:username")
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

def get_user_id(name: str):
    query = text("SELECT user_id FROM users WHERE username = :name")
    res = db.session.execute(query, {"name":name}).fetchone()
    val = res[0] if res else None
    return val
    
def create_new_topic(name: str):
    query = text("INSERT INTO topics (name) VALUES (:name) ON CONFLICT DO NOTHING")
    db.session.exeute(query, {"name":name})
    db.session.commit()

def get_topic(name: str):
    query = text("SELECT name FROM topics WHERE name = :name")
    res = db.session.execute(query, {"name":name})
    return res.fetchone()[0]

def get_all_topics():
    query = text("SELECT name FROM topics")
    result = db.session.execute(query)
    result_as_list = [name[0] for name in result]
    return result_as_list

def create_new_thread(name: str, topic: str, creator_name: str):
    query = text("INSERT INTO threads (name, creator_id, topic_id, date_created)" \
    "select :name, u.user_id, t.topic_id, NOW() from users u, topics t where " \
    "u.username = :creator_name and t.name = :topic")
    db.session.execute(query, {"name":name, "topic":topic, "creator_name":creator_name})
    db.session.commit()

def get_all_threads(topic: str):
    query = text("SELECT thread_id, T.name, date_created FROM threads T INNER JOIN topics D ON T.topic_id = D.topic_id " \
    "WHERE D.name = :name ORDER by date_created DESC")
    res = db.session.execute(query, {"name":topic})
    return res.fetchall()

def get_all_posts(thread_id: int):
    query = text("SELECT username, content, name FROM posts P, threads T, users U " \
    "WHERE P.creator_id = U.user_id AND P.thread_id = :thread_id AND T.thread_id = :thread_id")
    res = db.session.execute(query, {"thread_id":thread_id})
    return res.fetchall() 

def get_thread_id(name:str):
    query = text("SELECT thread_id FROM threads WHERE name = :name")
    res = db.session.execute(query, {"name":name})
    return res.fetchone()[0]

def create_new_post(content: str, user_id: int, thread_id: int):
    query = text("INSERT INTO posts (creator_id, thread_id, content)" \
    "SELECT :user_id, thread_id, :content FROM threads T where T.thread_id = :thread_id")
    db.session.execute(query, {"user_id":user_id, "content":content, "thread_id":thread_id})
    db.session.commit()
