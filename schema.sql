CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    is_admin BOOLEAN, 
    description TEXT
    );

CREATE TABLE topics (
    topic_id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
    );

CREATE TABLE threads (
    thread_id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    topic_id INTEGER REFERENCES topics(topic_id) NOT NULL,
    creator_id INTEGER REFERENCES users(user_id),
    date_created TIMESTAMP
    );

CREATE TABLE posts (
    post_id SERIAL PRIMARY KEY,
    creator_id INTEGER REFERENCES users(user_id),
    thread_id INTEGER REFERENCES threads(thread_id),
    content TEXT CHECK (length(content) <= 500),
    date_created TIMESTAMP,
    upvotes INTEGER
    );

CREATE TABLE private_messages (
    message_id SERIAL PRIMARY KEY,
    sender_id INTEGER REFERENCES users(user_id),
    receiver_id INTEGER REFERENCES users(user_id),
    content TEXT CHECK (length(content) <= 200),
    date_sent TIMESTAMP
);

CREATE TABLE images (
    image_id SERIAL PRIMARY KEY, 
    data BYTEA
);

CREATE TABLE user_images (
    user_id INTEGER REFERENCES users(user_id),
    image_id INTEGER REFERENCES images(image_id),
    PRIMARY KEY (user_id, image_id)
);

CREATE TABLE post_images (
    post_id INTEGER REFERENCES posts(post_id),
    image_id INTEGER REFERENCES images(image_id),
    PRIMARY KEY (post_id, image_id)
);
