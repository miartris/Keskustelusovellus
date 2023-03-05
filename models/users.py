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
    query = text("INSERT INTO users (username, password, is_admin) VALUES (:username, :password, :as_admin)")
    try:
        db.session.execute(query, {"username":name, "password":hashed_password, "as_admin":as_admin})
        db.session.commit()
        return True
    except:
        return False

def get_user_id(name: str):
    query = text("SELECT user_id FROM users WHERE username = :name")
    res = db.session.execute(query, {"name":name}).fetchone()
    val = res[0] if res else None
    return val

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

def get_image_by_user(id: int):
    query = text("SELECT data from images I LEFT JOIN user_images U on I.image_id = U.image_id WHERE U.user_id = :id " \
                 "ORDER BY I.image_id DESC LIMIT 1")
    res = db.session.execute(query, {"id":id})
    return res.fetchone()
