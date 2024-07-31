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

api = Namespace("User", description="Collection of user endpoints", path="/")

user_fields = api.model(
    "User",
    {
        "id": fields.Integer(description="ID of the user"),
        "name": fields.String(description="Name of the user"),
        "username": fields.String(description="Username of the user"),
    },
)

user_parser = reqparse.RequestParser()
user_parser.add_argument("name", type=str, required=True, help="Name of the user")
user_parser.add_argument(
    "username", type=str, required=True, help="Username of the user"
)
user_parser.add_argument(
    "password", type=str, required=True, help="Password of the user"
)


@api.route("/user")
class UserAPI(Resource):
    @marshal_with(user_fields)
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user:
            return user
        else:
            return {"message": "User not found"}, 401

    @jwt_required()
    @api.expect(user_parser)
    def put(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 401
        args = user_parser.parse_args()
        name = args["name"]
        username = args["username"]
        password = args["password"]
        collision = User.query.filter_by(username=username).first()
        if collision and collision.id != user_id:
            return {"message": "Username already exists"}, 400
        user.name = name
        user.username = username
        user.password = password
        db.session.commit()
        return marshal(user, user_fields)

    # register
    @api.expect(user_parser)
    def post(self):
        args = user_parser.parse_args()
        name = args["name"]
        username = args["username"]
        password = args["password"]
        if User.query.filter_by(username=username).first():
            return {"message": "Username already exists"}, 400
        user = User(name=name, username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return marshal(user, user_fields)

    @jwt_required()
    def delete(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 401
        db.session.delete(user)
        return {"message": "User deleted"}


@api.route("/users")
class UsersAPI(Resource):
    @marshal_with(user_fields)
    def get(self):
        users = User.query.all()
        return users


@api.route("/user/<int:user_id>")
class UsergetAPI(Resource):
    @jwt_required()
    def get(self, user_id):
        self_id = get_jwt_identity()
        if not User.query.get(self_id).admin:
            return {"message": "Not authorized"}, 401
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 401
        return marshal(user, user_fields)

    @jwt_required()
    @api.expect(user_parser)
    def put(self, user_id):
        self_id = get_jwt_identity()
        if not User.query.get(self_id).admin:
            return {"message": "Not authorized"}, 401
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 401
        args = user_parser.parse_args()
        name = args["name"]
        username = args["username"]
        password = args["password"]
        collision = User.query.filter_by(username=username).first()
        if collision and collision.id != user_id:
            return {"message": "Username already exists"}, 400
        user.name = name
        user.username = username
        user.password = password
        db.session.commit()
        return marshal(user, user_fields)

    @jwt_required()
    def delete(self, user_id):
        self_id = get_jwt_identity()
        if not User.query.get(self_id).admin:
            return {"message": "Not authorized"}, 401
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 401
        db.session.delete(user)
        return {"message": "User deleted"}
