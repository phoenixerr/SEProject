from apis import api
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required,
)
from flask_restx import (
    Api,
    Namespace,
    Resource,
    fields,
    marshal,
    marshal_with,
    reqparse,
)
from main import app
from models import Admin, Course, Instructor, Student, User, db

api = Namespace(
    "Authosization", description="Collection of authorization endpoints", path="/"
)

auth_parser = reqparse.RequestParser()
auth_parser.add_argument("username", type=str, required=True, help="Username")
auth_parser.add_argument("password", type=str, required=True, help="Password")


@api.route("/login")
class LoginAPI(Resource):
    @api.expect(auth_parser)
    @api.doc(description="This is the login endpoint")
    def post(self):
        username = api.payload.get("username")
        password = api.payload.get("password")
        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(password):
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token}
        else:
            return {"message": "Invalid credentials"}, 401
