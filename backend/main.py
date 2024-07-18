from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api, Resource

app = Flask(__name__)

import config
import models
import api
