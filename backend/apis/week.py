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

api = Namespace("Weeks", description="Collection of week endpoints", path="/")

week_fields = api.model(
    "Week",
    {
        "id": fields.Integer(required=True, description="ID of the week", example=1),
        "number": fields.Integer(
            required=True, description="Number of the week", example=1
        ),
        "course_id": fields.Integer(
            required=True, description="ID of the Course", example=1
        ),
        "summary": fields.String(
            required=False,
            description="A quick summary",
            example="In this week we do bla bla and bla",
        ),
    },
)

week_input_fields = api.model(
    "WeekInput",
    {
        # "id": fields.Integer(description="ID of the week", example=1),
        "number": fields.Integer(
            required=True, description="Number of the week", example=1
        ),
        "summary": fields.String(
            required=False,
            description="A quick summary",
            example="In this week we do bla bla and bla",
        ),
        "course_id": fields.Integer(
            required=True, description="ID of the Course", example=1
        ),
    },
)

week_update_fields = api.model(
    "WeekUpdate",
    {
        # "id": fields.Integer(description="ID of the week", example=1),
        "number": fields.Integer(
            required=True, description="Number of the week", example=1
        ),
        "course_id": fields.Integer(
            required=True, description="ID of the Course", example=1
        ),
        "summary": fields.String(
            required=False,
            description="A quick summary",
            example="In this week we do bla bla and bla",
        ),
    },
)


week_parser = reqparse.RequestParser()
week_parser.add_argument("number", type=int, required=True, help="Number of the week")
week_parser.add_argument("course_id", type=int, required=True, help="Course ID")
week_parser.add_argument(
    "summary", type=str, required=False, help="Summary of the week"
)


@api.route("/course/<int:course_id>/weeks")
class CourseWeekAPI(Resource):
    @jwt_required()
    @api.doc(
        description="Returns the summary of all the weeks of the course with specified course ID.",
        security="jsonWebToken",
    )
    def get(self, course_id):
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
        course = Course.query.get(course_id)
        if not course:
            return {"message": "Course not found"}, 401
        if course not in courses:
            return {"message": "User not enrolled in course"}, 401
        weeks = course.weeks
        return marshal(weeks, week_fields)

    @jwt_required()
    @api.expect(week_input_fields)
    @api.doc(
        description="Add summary of new week to the course with specified course ID.",
        security="jsonWebToken",
    )
    def post(self, course_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 401
        if not user.admin and not user.instructor:
            return {"message": "User is not an admin or instructor"}, 401
        course = Course.query.get(course_id)
        if not course:
            return {"message": "Course not found"}, 401
        if user.instructor and course not in user.instructor.courses:
            return {"message": "User is not an instructor of the course"}, 401
        args = week_parser.parse_args()
        number = args["number"]
        summary = args["summary"]
        try:
            number = int(number)
        except ValueError:
            return {"message": "Number must be an integer"}, 400
        already_exists = Week.query.filter_by(
            number=number, course_id=course_id
        ).first()
        if already_exists:
            return {"message": f"Week {week} already exists for this course"}, 400
        week = Week(number=number, course=course, summary=summary)
        db.session.add(week)
        db.session.commit()
        return marshal(week, week_fields)


@api.route("/week/<int:week_id>")
class WeekAPI(Resource):
    @jwt_required()
    @api.doc(
        description="Returns the details of the week with specified week ID.",
        security="jsonWebToken",
    )
    def get(self, week_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 401
        week = Week.query.get(week_id)
        if not week:
            return {"message": "Week not found"}, 401
        course = week.course
        if not course:
            return {"message": "Course not found"}, 401
        if user.student and course not in user.student.courses:
            return {"message": "User not enrolled in course"}, 401
        if user.instructor and course not in user.instructor.courses:
            return {"message": "User not an instructor of the course"}, 401
        return marshal(week, week_fields)

    @jwt_required()
    @api.expect(week_update_fields)
    @api.doc(
        description="Modify the details of the week with specified week ID.",
        security="jsonWebToken",
    )
    def put(self, week_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 401
        week = Week.query.get(week_id)
        if not week:
            return {"message": "Week not found"}, 401
        course = week.course
        if not course:
            return {"message": "Course not found"}, 401
        if not user.admin and not user.instructor:
            return {"message": "User is not an admin or instructor"}, 401
        if user.instructor and course not in user.instructor.courses:
            return {"message": "User not an instructor of the course"}, 401
        args = week_parser.parse_args()
        number = args["number"]
        summary = args["summary"]
        try:
            number = int(number)
        except ValueError:
            return {"message": "Number must be an integer"}, 400
        already_exists = Week.query.filter_by(
            number=number, course_id=course.id
        ).first()
        if already_exists and already_exists.id != week_id:
            return {"message": f"Week {week} already exists for this course"}, 400
        week.number = number
        week.summary = summary
        db.session.commit()
        return marshal(week, week_fields)

    @jwt_required()
    @api.doc(
        description="Delete the details of the week with specified week ID.",
        security="jsonWebToken",
    )
    def delete(self, week_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 401
        week = Week.query.get(week_id)
        if not week:
            return {"message": "Week not found"}, 401
        course = week.course
        if not course:
            return {"message": "Course not found"}, 401
        if not user.admin and not user.instructor:
            return {"message": "User is not an admin or instructor"}, 401
        if user.instructor and course not in user.instructor.courses:
            return {"message": "User not an instructor of the course"}, 401
        db.session.delete(week)
        db.session.commit()
        return {"message": "Week deleted"}


@api.route("/week/<int:week_id>/summarize")
class WeekSummaryAPI(Resource):
    @jwt_required()
    @api.doc(
        description="Modify the summary of the week with specified week ID.\nGenerated by Gemini LLM",
        security="jsonWebToken",
    )
    def put(self, week_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 401
        week = Week.query.get(week_id)
        if not week:
            return {"message": "Week not found"}, 401
        course = week.course
        if not course:
            return {"message": "Course not found"}, 401
        if not user.admin and not user.instructor:
            return {"message": "User is not an admin or instructor"}, 401
        if user.instructor and course not in user.instructor.courses:
            return {"message": "User not an instructor of the course"}, 401
        summary = "summary fetched from GENAI" + "".join(
            random.choices(string.ascii_uppercase + string.digits, k=10)
        )
        week.summary = summary
        db.session.commit()
        return marshal(week, week_fields)
