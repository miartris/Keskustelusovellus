from db import db
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash

def check_user_data(name: str, password: str):
    query = text("SELECT username, user_id, password, is_admin FROM users WHERE username=:username")
    result = db.session.execute(query, {"username":name})
    user = result.fetchone()
    user_object = {"is_user": False, "username": name, "error": None, "admin": False}
    if not user:
        user_object["error"] = "No such user"        
    else:
        hashval = user.password
        if check_password_hash(hashval, password):
            user_object["is_user"] = True
        else:
            user_object["error"] = "Wrong password"
        if user.is_admin == True:
            user_object["admin"] = True
    
    return user_object


def create_new_user(name: str, password: str, as_admin: bool):
    hashed_password = generate_password_hash(password, "sha256")
    query = text("INSERT INTO users (username, password, is_admin) VALUES (:username, :password, :as_admin) ON CONFLICT DO NOTHING")
    db.session.execute(query, {"username":name, "password":hashed_password, "as_admin":as_admin})
    db.session.commit()

def get_user_id(name: str):
    query = text("SELECT user_id FROM users WHERE username = :name")
    res = db.session.execute(query, {"name":name}).fetchone()
    val = res[0] if res else None
    return val
    
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

def update_user_description(user_id: int, description: str):
    query = text("UPDATE users SET description = :description WHERE user_id = :id")
    db.session.execute(query, {"description":description, "id":user_id})
    db.session.commit()

def upload_profile_image(data: bytearray, id: int, filename:str):
    query = text("INSERT into images (data, filename) VALUES(:data, :filename)")
    db.session.execute(query, {"data":data, "filename":filename})
    db.session.commit()
    query2 = text("INSERT INTO user_images (user_id, image_id) SELECT :uid, image_id " \
                 "FROM images ORDER BY image_id DESC LIMIT 1")
    db.session.execute(query2, {"uid":id})
    db.session.commit()

def associate_img_to_user(id: int):
    pass

def get_profile_data(id: int):
    query = text("SELECT username, description, COUNT(post_id), SUM(upvotes) FROM users LEFT JOIN " \
                 "posts ON users.user_id = posts.creator_id WHERE users.user_id = :id GROUP BY users.user_id")
    res = db.session.execute(query, {"id":id})
    return res.fetchone()

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

def add_upvote(id: int, increment: int):
    query = text("UPDATE posts SET upvotes = upvotes + 1 where post_id = :id")
    db.session.execute(query, {"id":id})
    db.session.commit()

def get_total_statistics():
    query = text("SELECT COUNT(DISTINCT user_id), COUNT(DISTINCT T.thread_id), COUNT(DISTINCT post_id) " \
                 "FROM users U, THREADS T, posts P")
    res = db.session.execute(query)
    return res.fetchone()

def get_image(id: int):
    query = text("SELECT image_id, data FROM images where image_id = :id ORDER BY image_id DESC LIMIT 1")
    res = db.session.execute(query, {"id":id})
    return res.fetchone()

def get_image_by_user(id: int):
    query = text("SELECT data from images I LEFT JOIN user_images U on I.image_id = U.image_id WHERE U.user_id = :id " \
                 "ORDER BY I.image_id DESC LIMIT 1")
    res = db.session.execute(query, {"id":id})
    return res.fetchone()

