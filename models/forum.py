from db import db
from sqlalchemy.sql import text

def create_new_topic(name: str):
    query = text("INSERT INTO topics (name) VALUES (:name) ON CONFLICT DO NOTHING")
    db.session.execute(query, {"name":name})
    db.session.commit()

def get_topic(name: str):
    query = text("SELECT name FROM topics WHERE name = :name")
    res = db.session.execute(query, {"name":name})
    return res

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
    query = text("SELECT username, content, name, P.date_created, upvotes, P.post_id FROM posts P, threads T, users U " \
    "WHERE P.creator_id = U.user_id AND P.thread_id = :thread_id AND T.thread_id = :thread_id " \
    "ORDER BY P.date_created ASC")
    res = db.session.execute(query, {"thread_id":thread_id})
    return res.fetchall() 

def get_thread_id(name:str):
    query = text("SELECT thread_id FROM threads WHERE name = :name")
    res = db.session.execute(query, {"name":name})
    return res.fetchone()[0]

def create_new_post(content: str, user_id: int, thread_id: int):
    query = text("INSERT INTO posts (creator_id, thread_id, content, date_created, upvotes)" \
    "SELECT :user_id, thread_id, :content, NOW(), 0 FROM threads T where T.thread_id = :thread_id")
    db.session.execute(query, {"user_id":user_id, "content":content, "thread_id":thread_id})
    db.session.commit()

def increment_upvote(id: int, increment: int):
    query = text("UPDATE posts SET upvotes = upvotes + 1 where post_id = :id")
    db.session.execute(query, {"id":id})
    db.session.commit()