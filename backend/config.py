from main import app
from dotenv import load_dotenv
from os import getenv

load_dotenv()
app.config["SQLALCHEMY_DATABASE_URI"] = getenv(
    "SQLALCHEMY_DATABASE_URI", "sqlite:///db.sqlite"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = getenv(
    "SQLALCHEMY_TRACK_MODIFICATIONS", False
)
app.config["SECRET_KEY"] = getenv("SECRET_KEY", "secret")
app.config["JWT_SECRET_KEY"] = getenv("JWT_SECRET_KEY", "jwt_secret")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = getenv("JWT_ACCESS_TOKEN_EXPIRES", 3600)
app.config["JWT_TOKEN_LOCATION"] = getenv("JWT_TOKEN_LOCATION", ["headers"])
