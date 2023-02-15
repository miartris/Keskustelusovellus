from app import app
from flask_sqlalchemy import SQLAlchemy
import os

dbURI = os.getenv("DATABASE_URI")
app.config["SQLALCHEMY_DATABASE_URI"] = dbURI
# For debugging/development
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)


