from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import logging
import logging.handlers
import os

app = Flask(__name__)
app.config.from_object(Config)

# security configuration
CORS(app)

# database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models
