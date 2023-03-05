from db import db
from sqlalchemy.sql import text

def get_threads_per_topic():
    query = text("SELECT thread_id, count(thread_id) FROM threads GROUP BY topic_id")
    res = db.session.execute(query)
    return res.fetchall()

def get_total_users():
    res = db.session.execute(text("SELECT COUNT(DISTINCT user_id) from users"))
    return res.fetchone()

def get_total_posts():
    res = db.session.execute(text("SELECT COUNT(DISTINCT post_id) FROM posts"))
    return res.fetchone()

def get_topics_and_threads():
    query = text("select T.name, count(H.thread_id) as amt_of_threads " \
                "from topics T left join threads H on T.topic_id = H.topic_id " \
                "GROUP BY H.topic_id, T.name ORDER BY amt_of_threads DESC")
    res = db.session.execute(query)
    return res.fetchall()

def get_total_statistics():
    query = text("SELECT COUNT(DISTINCT user_id), COUNT(DISTINCT T.thread_id), COUNT(DISTINCT post_id) " \
                 "FROM users U, THREADS T, posts P")
    res = db.session.execute(query)
    return res.fetchone()

def get_image(id: int):
    query = text("SELECT image_id, data FROM images where image_id = :id ORDER BY image_id DESC LIMIT 1")
    res = db.session.execute(query, {"id":id})
    return res.fetchone()