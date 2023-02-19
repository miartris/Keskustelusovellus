CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
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
    content TEXT CHECK (length(content) <= 500)
    );