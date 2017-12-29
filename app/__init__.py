from flask import Flask
from config import config
from os import path


application = Flask(__name__)
application.config.from_object(config["production"])
BASE_URL = path.abspath(path.dirname(__file__))

import app.views
