import random
import string

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

api = Namespace("Course", description="Collection of course endpoints", path="/")

course_fields = api.model(
    "Course",
    {
        "id": fields.Integer,
        "name": fields.String,
        "level": fields.Integer,
        "summary": fields.String,
    },
)

course_parser = reqparse.RequestParser()
course_parser.add_argument("name", type=str, required=True, help="Name of the course")
course_parser.add_argument("level", type=int, required=True, help="Level of the course")
course_parser.add_argument(
    "summary", type=str, required=False, help="Summary of the course"
)


@api.route("/courses")
@api.doc(description="Returns all the courses along with their details.")
class CourseAPI(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user:
            if user.student:
                courses = user.student.courses
            elif user.instructor:
                courses = user.instructor.courses
            else:
                courses = Course.query.all()
        else:
            return {"message": "User not found"}, 401
        return marshal(courses, course_fields)

    @jwt_required()
    @api.doc(description="Add a new course along with its details.")
    @api.expect(course_parser)
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 401

        if not user.admin:
            return {"message": "User is not an admin"}, 401
        args = course_parser.parse_args()
        name = args["name"]
        level = args["level"]
        summary = args["summary"]
        try:
            level = int(level)
        except ValueError:
            return {"message": "Level must be an integer"}, 400
        course = Course(name=name, level=level, summary=summary)
        db.session.add(course)
        db.session.commit()
        return marshal(course, course_fields)


@api.route("/course/<int:course_id>")
class CourseAPI(Resource):
    @jwt_required()
    @api.doc(
        description="Returns the course with specified course ID along with their details."
    )
    def get(self, course_id):
        course = Course.query.get(course_id)
        if not course:
            return {"message": "Course not found"}, 400
        return marshal(course, course_fields)

    @jwt_required()
    @api.expect(course_parser)
    @api.doc(
        description="Modify the course with specified course ID along with their details."
    )
    def put(self, course_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return {"message": "User not found"}, 401

        if not user.admin:
            return {"message": "User is not an admin"}, 401

        args = course_parser.parse_args()
        name = args["name"]
        level = args["level"]
        summary = args["summary"]
        try:
            level = int(level)
        except ValueError:
            return {"message": "Level must be an integer"}, 400

        course = Course.query.get(course_id)
        if not course:
            return {"message": "Course not found"}, 400

        course.name = name
        course.level = level
        course.summary = summary
        db.session.commit()
        return marshal(course, course_fields)

    @jwt_required()
    @api.doc(description="Delete the course with specified course ID.")
    def delete(self, course_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return {"message": "User not found"}, 401

        if not user.admin:
            return {"message": "User is not an admin"}, 401

        course = Course.query.get(course_id)
        if not course:
            return {"message": "Course not found"}, 400

        db.session.delete(course)
        db.session.commit()
        return {"message": "Course deleted"}


@api.route("/course/<int:course_id>/summarize")
class CourseSummaryAPI(Resource):
    @jwt_required()
    @api.doc(description="Modify the summary of the course with the specified ID.")
    def put(self, course_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 401
        course = Course.query.get(course_id)
        if not course:
            return {"message": "Course not found"}, 401
        if not user.admin and not user.instructor:
            return {"message": "User is not an admin or instructor"}, 401
        if user.instructor and course not in user.instructor.courses:
            return {"message": "User not an instructor of the course"}, 401
        summary = "summary fetched from GENAI" + "".join(
            random.choices(string.ascii_uppercase + string.digits, k=10)
        )
        course.summary = summary
        db.session.commit()
        return marshal(course, course_fields)
