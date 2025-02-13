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
    "Authorization", description="Collection of authorization endpoints", path="/"
)

auth_parser = reqparse.RequestParser()
auth_parser.add_argument("username", type=str, required=True, help="Username")
auth_parser.add_argument("password", type=str, required=True, help="Password")

login_post = api.model(
    "login",
    {
        "username": fields.String(
            required=True, description="The username", example="admin"
        ),
        "password": fields.String(
            required=True, description="The password", example="admin"
        ),
    },
)


@api.route("/login")
class LoginAPI(Resource):
    @api.expect(login_post)
    @api.doc(description="This is the login endpoint")
    def post(self):
        username = api.payload.get("username")
        password = api.payload.get("password")
        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(password):
            access_token = create_access_token(identity=user.id)
            return {
                "access_token": access_token,
                "admin": bool(user.admin),
                "instructor": bool(user.instructor),
                "student": bool(user.student),
                }
        else:
            return {"message": "Invalid credentials"}, 401
