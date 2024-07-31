from datetime import datetime

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
from models import (
    Admin,
    Assignment,
    Course,
    Instructor,
    Lecture,
    Option,
    Question,
    Student,
    Submission,
    User,
    Week,
    db,
)

api = Namespace(
    "Instructor", description="Collection of instructor endpoints", path="/"
)

instructor_fields = api.model(
    "Instructor",
    {
        "id": fields.Integer,
    },
)


@api.route("/instructors")
class InstructorsAPI(Resource):
    @jwt_required()
    @api.doc(description="Returns all the instructors.",
             security = 'jsonWebToken')
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 401
        if not user.admin:
            return {"message": "User is not an admin"}, 401
        instructors = Instructor.query.all()
        return marshal(instructors, instructor_fields)

    @jwt_required()
    @api.doc(description="Add new users as the instructors.",
             security = 'jsonWebToken')
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 401
        if user.student:
            return {"message": "User is a student"}, 401
        if user.instructor:
            return {"message": "User is already an instructor"}, 401
        if user.admin:
            return {"message": "User is an admin"}, 401
        instructor = Instructor(user=user)
        db.session.add(instructor)
        db.session.commit()
        return marshal(instructor, instructor_fields)


@api.route("/instructor/<int:instructor_id>")
class InstructorAPI(Resource):
    @jwt_required()
    @api.doc(description="Returns the instructor with specified instructor ID.",
             security = 'jsonWebToken')
    def get(self, instructor_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 401
        instructor = Instructor.query.get(instructor_id)
        if not instructor:
            return {"message": "Instructor not found"}, 401
        if user.student:
            return {"message": "Unauthorized access"}, 401
        if user.instructor and instructor != user.instructor:
            return {"message": "Unauthorized access"}, 401
        return marshal(instructor, instructor_fields)

    @jwt_required()
    @api.doc(description="Delete the instructor with specified instructor ID.",
             security = 'jsonWebToken')
    def delete(self, instructor_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 401
        instructor = Instructor.query.get(instructor_id)
        if not instructor:
            return {"message": "Instructor not found"}, 401
        if user.student:
            return {"message": "Unauthorized access"}, 401
        if user.instructor and instructor != user.instructor:
            return {"message": "Unauthorized access"}, 401
        db.session.delete(instructor)
        db.session.commit()
        return {"message": "Instructor deleted"}
