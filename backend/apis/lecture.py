from flask_restx import Api, Resource, marshal_with, fields, reqparse, marshal
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from main import app
from models import db, Course, User, Student, Instructor, Admin, Week, Lecture, Assignment, Question, Option, Submission
from apis import api
import random
import string

lecture_fields = api.model('Lecture', {
    'id': fields.Integer,
    'week_id': fields.Integer,
    'title': fields.String,
    'url': fields.String,
    'summary': fields.String,
})

lecture_parser = reqparse.RequestParser()
lecture_parser.add_argument('week_id', type=int, required=True, help='Week ID')
lecture_parser.add_argument('title', type=str, required=True, help='Title of the lecture')
lecture_parser.add_argument('url', type=str, required=True, help='URL of the lecture')
lecture_parser.add_argument('summary', type=str, required=False, help='Summary of the lecture')

@api.route('/week/<int:week_id>/lectures')
class WeekLectureAPI(Resource):
    @jwt_required()
    def get(self, week_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 401
        week = Week.query.get(week_id)
        if not week:
            return {'message': 'Week not found'}, 401
        course = week.course
        if not course:
            return {'message': 'Course not found'}, 401
        if user.student and course not in user.student.courses:
            return {'message': 'User not enrolled in course'}, 401
        if user.instructor and course not in user.instructor.courses:
            return {'message': 'User is not an instructor of the course'}, 401
        lectures = week.lectures
        return marshal(lectures, lecture_fields)

    @jwt_required()
    @api.expect(lecture_parser)
    def post(self, week_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 401
        if not user.admin and not user.instructor:
            return {'message': 'User is not an admin or instructor'}, 401
        week = Week.query.get(week_id)
        if not week:
            return {'message': 'Week not found'}, 401
        course = week.course
        if not course:
            return {'message': 'Course not found'}, 401
        if user.instructor and course not in user.instructor.courses:
            return {'message': 'User is not an instructor of the course'}, 401
        args = lecture_parser.parse_args()
        title = args['title']
        url = args['url']
        summary = args['summary']
        lecture = Lecture(week=week, title=title, url=url, summary=summary)
        db.session.add(lecture)
        db.session.commit()
        return marshal(lecture, lecture_fields)

@api.route('/lecture/<int:lecture_id>')
class LectureAPI(Resource):
    @jwt_required()
    def get(self, lecture_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 401
        lecture = Lecture.query.get(lecture_id)
        if not lecture:
            return {'message': 'Lecture not found'}, 401
        week = lecture.week
        if not week:
            return {'message': 'Week not found'}, 401
        course = week.course
        if not course:
            return {'message': 'Course not found'}, 401
        if user.student and course not in user.student.courses:
            return {'message': 'User not enrolled in course'}, 401
        if user.instructor and course not in user.instructor.courses:
            return {'message': 'User is not an instructor of the course'}, 401
        return marshal(lecture, lecture_fields)

    @jwt_required()
    @api.expect(lecture_parser)
    def put(self, lecture_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 401
        if not user.admin and not user.instructor:
            return {'message': 'User is not an admin or instructor'}, 401
        lecture = Lecture.query.get(lecture_id)
        if not lecture:
            return {'message': 'Lecture not found'}, 401
        week = lecture.week
        if not week:
            return {'message': 'Week not found'}, 401
        course = week.course
        if not course:
            return {'message': 'Course not found'}, 401
        if user.instructor and course not in user.instructor.courses:
            return {'message': 'User is not an instructor of the course'}, 401
        args = lecture_parser.parse_args()
        title = args['title']
        url = args['url']
        summary = args['summary']
        lecture.title = title
        lecture.url = url
        lecture.summary = summary
        db.session.commit()
        return marshal(lecture, lecture_fields)

    @jwt_required()
    def delete(self, lecture_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 401
        if not user.admin and not user.instructor:
            return {'message': 'User is not an admin or instructor'}, 401
        lecture = Lecture.query.get(lecture_id)
        if not lecture:
            return {'message': 'Lecture not found'}, 401
        week = lecture.week
        if not week:
            return {'message': 'Week not found'}, 401
        course = week.course
        if not course:
            return {'message': 'Course not found'}, 401
        if user.instructor and course not in user.instructor.courses:
            return {'message': 'User is not an instructor of the course'}, 401
        db.session.delete(lecture)
        db.session.commit()
        return {'message': 'Lecture deleted'}

@api.route('/lecture/<int:lecture_id>/summarize')
class LectureSummarizeAPI(Resource):
    @jwt_required()
    def put(self, lecture_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 401
        lecture = Lecture.query.get(lecture_id)
        if not lecture:
            return {'message': 'Lecture not found'}, 401
        week = lecture.week
        if not week:
            return {'message': 'Week not found'}, 401
        course = week.course
        if not course:
            return {'message': 'Course not found'}, 401
        if not user.admin and not user.instructor:
            return {'message': 'User is not an admin or instructor'}, 401
        if user.instructor and course not in user.instructor.courses:
            return {'message': 'User is not an instructor of the course'}, 401
        summary = "summary fetched from GENAI" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        lecture.summary = summary
        db.session.commit()
        return marshal(lecture, lecture_fields)