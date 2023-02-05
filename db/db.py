from app import app
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv 

load_dotenv("../")
dbURI = os.getenv("DATABASE_URI")
app.config["SQLALCHEMY_DATABASE_URI"] = dbURI
db = SQLAlchemy(app)