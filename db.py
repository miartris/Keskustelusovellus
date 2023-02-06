from app import app
from flask_sqlalchemy import SQLAlchemy
import os

dbURI = os.getenv("DATABASE_URI")
app.config["SQLALCHEMY_DATABASE_URI"] = dbURI
db = SQLAlchemy(app)