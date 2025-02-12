import os
import random
import string

from apis import api

# for gen ai thingies
from dotenv import load_dotenv
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
from genaifuncs import generate_summary_from_transcript, get_transcript
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

api = Namespace("Lectures", description="Collection of lecture endpoints", path="/")

lecture_fields = api.model(
    "Lecture",
    {
        "id": fields.Integer,
        "week_id": fields.Integer,
        "title": fields.String,
        "url": fields.String,
        "summary": fields.String,
    },
)


lecture_input_fields = api.model(
    "Lecture",
    {
        # "week_id": fields.Integer(required=True, description='The Week ID to which the lecture belongs', example=1),
        "title": fields.String(
            required=True,
            description="The Title of the lecture",
            example="Lists in python",
        ),
        "url": fields.String(
            required=True,
            description="The Youtube URL ID of the lecture",
            example="=LDU_Txk06tM",
        ),
        "summary": fields.String(
            required=True,
            description="The Summary of the lecture",
            example="Lists in python",
        ),
    },
)

lecture_parser = reqparse.RequestParser()
lecture_parser.add_argument(
    "title", type=str, required=True, help="Title of the lecture"
)
lecture_parser.add_argument("url", type=str, required=True, help="URL of the lecture")
lecture_parser.add_argument(
    "summary", type=str, required=False, help="Summary of the lecture"
)


@api.route("/week/<int:week_id>/lectures")
class WeekLectureAPI(Resource):
    @jwt_required()
    @api.doc(
        description="Returns the lectures present in the week with the specified week ID.",
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
            return {"message": "User is not an instructor of the course"}, 401
        lectures = week.lectures
        return marshal(lectures, lecture_fields)

    @jwt_required()
    @api.expect(lecture_input_fields)
    @api.doc(
        description="Add lectures to the week with the specified week ID.",
        security="jsonWebToken",
    )
    def post(self, week_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 401
        if not user.admin and not user.instructor:
            return {"message": "User is not an admin or instructor"}, 401
        week = Week.query.get(week_id)
        if not week:
            return {"message": "Week not found"}, 401
        course = week.course
        if not course:
            return {"message": "Course not found"}, 401
        if user.instructor and course not in user.instructor.courses:
            return {"message": "User is not an instructor of the course"}, 401
        args = lecture_parser.parse_args()
        title = args["title"]
        url = args["url"]
        summary = args["summary"]
        lecture = Lecture(week=week, title=title, url=url, summary=summary)
        db.session.add(lecture)
        db.session.commit()
        return marshal(lecture, lecture_fields)


@api.route("/lecture/<int:lecture_id>")
class LectureAPI(Resource):
    @jwt_required()
    @api.doc(
        description="Returns the lectures with the specified lecture ID.",
        security="jsonWebToken",
    )
    def get(self, lecture_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 401
        lecture = Lecture.query.get(lecture_id)
        if not lecture:
            return {"message": "Lecture not found"}, 401
        week = lecture.week
        if not week:
            return {"message": "Week not found"}, 401
        course = week.course
        if not course:
            return {"message": "Course not found"}, 401
        if user.student and course not in user.student.courses:
            return {"message": "User not enrolled in course"}, 401
        if user.instructor and course not in user.instructor.courses:
            return {"message": "User is not an instructor of the course"}, 401
        return marshal(lecture, lecture_fields)

    @jwt_required()
    @api.expect(lecture_input_fields)
    @api.doc(
        description="Modify the lectures with the specified lecture ID.",
        security="jsonWebToken",
    )
    def put(self, lecture_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 401
        if not user.admin and not user.instructor:
            return {"message": "User is not an admin or instructor"}, 401
        lecture = Lecture.query.get(lecture_id)
        if not lecture:
            return {"message": "Lecture not found"}, 401
        week = lecture.week
        if not week:
            return {"message": "Week not found"}, 401
        course = week.course
        if not course:
            return {"message": "Course not found"}, 401
        if user.instructor and course not in user.instructor.courses:
            return {"message": "User is not an instructor of the course"}, 401
        args = lecture_parser.parse_args()
        title = args["title"]
        url = args["url"]
        summary = args["summary"]
        lecture.title = title
        lecture.url = url
        lecture.summary = summary
        db.session.commit()
        return marshal(lecture, lecture_fields)

    @jwt_required()
    @api.doc(
        description="Delete the lectures with the specified lecture ID.",
        security="jsonWebToken",
    )
    def delete(self, lecture_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 401
        if not user.admin and not user.instructor:
            return {"message": "User is not an admin or instructor"}, 401
        lecture = Lecture.query.get(lecture_id)
        if not lecture:
            return {"message": "Lecture not found"}, 401
        week = lecture.week
        if not week:
            return {"message": "Week not found"}, 401
        course = week.course
        if not course:
            return {"message": "Course not found"}, 401
        if user.instructor and course not in user.instructor.courses:
            return {"message": "User is not an instructor of the course"}, 401
        db.session.delete(lecture)
        db.session.commit()
        return {"message": "Lecture deleted"}


@api.route("/lecture/<int:lecture_id>/summarize")
class LectureSummarizeAPI(Resource):
    @jwt_required()
    @api.doc(
        description="Modify the lectures summary with the specified lecture ID.\nUses Gemini LLM.",
        security="jsonWebToken",
    )
    def put(self, lecture_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 401
        lecture = Lecture.query.get(lecture_id)
        if not lecture:
            return {"message": "Lecture not found"}, 401
        week = lecture.week
        if not week:
            return {"message": "Week not found"}, 401
        course = week.course
        if not course:
            return {"message": "Course not found"}, 401
        if not user.admin and not user.instructor:
            return {"message": "User is not an admin or instructor"}, 401
        if user.instructor and course not in user.instructor.courses:
            return {"message": "User is not an instructor of the course"}, 401

        prompt = "You are an educational video summarizer. So accuracy and completeness of information is very important. Ignore any mention of a previous time (such as 2021, 2022) and replace it with the current year. You will be taking the transcript text and summarizing the entire video and providing the important summary in points in about 400 words. Please give a markdown flavoured summary: \n\n\n"

        transcript = get_transcript(lecture.url)
        summary = generate_summary_from_transcript(transcript, prompt)
        lecture.summary = summary
        db.session.commit()
        return marshal(lecture, lecture_fields)
