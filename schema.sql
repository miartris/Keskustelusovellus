CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
);

CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    topic REFERENCES topics(name) NOT NULL,
    creator_id REFERENCES users(id),
    date_created TIMESTAMP
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    creator_id REFERENCES users(id),
    content CHECK (length(content) <= 500)
)