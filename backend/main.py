from flask import Flask
from flask_cors import CORS


app = Flask(__name__)

import config

cors = CORS(app)

import models

import apis
