from flask_restx import Api, Resource, marshal_with, fields, reqparse, marshal
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from main import app
from models import db, Course, User, Student, Instructor, Admin, Week, Lecture, Assignment, Question, Option, Submission
from apis import api
import random
import string

week_fields = api.model('Week', {
    'id': fields.Integer,
    'number': fields.Integer,
    'course_id': fields.Integer,
    'summary': fields.String,
})

week_parser = reqparse.RequestParser()
week_parser.add_argument('number', type=int, required=True, help='Number of the week')
week_parser.add_argument('course_id', type=int, required=True, help='Course ID')
week_parser.add_argument('summary', type=str, required=False, help='Summary of the week')

@api.route('/course/<int:course_id>/weeks')
class CourseWeekAPI(Resource):
    @jwt_required()
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
            return {'message': 'User not found'}, 401
        course = Course.query.get(course_id)
        if not course:
            return {'message': 'Course not found'}, 401
        if course not in courses:
            return {'message': 'User not enrolled in course'}, 401
        weeks = course.weeks
        return marshal(weeks, week_fields)

    @jwt_required()
    def post(self, course_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 401
        if not user.admin and not user.instructor:
            return {'message': 'User is not an admin or instructor'}, 401
        course = Course.query.get(course_id)
        if not course:
            return {'message': 'Course not found'}, 401
        if user.instructor and course not in user.instructor.courses:
            return {'message': 'User is not an instructor of the course'}, 401
        args = week_parser.parse_args()
        number = args['number']
        summary = args['summary']
        try:
            number = int(number)
        except ValueError:
            return {'message': 'Number must be an integer'}, 400
        already_exists = Week.query.filter_by(number=number, course_id=course_id).first()
        if already_exists:
            return {'message': f'Week {week} already exists for this course'}, 400
        week = Week(number=number, course=course, summary=summary)
        db.session.add(week)
        db.session.commit()
        return marshal(week, week_fields)

@api.route('/week/<int:week_id>')
class WeekAPI(Resource):
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
            return {'message': 'User not an instructor of the course'}, 401
        return marshal(week, week_fields)

    @jwt_required()
    def put(self, week_id):
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
        if not user.admin and not user.instructor:
            return {'message': 'User is not an admin or instructor'}, 401
        if user.instructor and course not in user.instructor.courses:
            return {'message': 'User not an instructor of the course'}, 401
        args = week_parser.parse_args()
        number = args['number']
        summary = args['summary']
        try:
            number = int(number)
        except ValueError:
            return {'message': 'Number must be an integer'}, 400
        already_exists = Week.query.filter_by(number=number, course_id=course.id).first()
        if already_exists and already_exists.id != week_id:
            return {'message': f'Week {week} already exists for this course'}, 400
        week.number = number
        week.summary = summary
        db.session.commit()
        return marshal(week, week_fields)

    @jwt_required()
    def delete(self, week_id):
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
        if not user.admin and not user.instructor:
            return {'message': 'User is not an admin or instructor'}, 401
        if user.instructor and course not in user.instructor.courses:
            return {'message': 'User not an instructor of the course'}, 401
        db.session.delete(week)
        db.session.commit()
        return {'message': 'Week deleted'}

@api.route('/week/<int:week_id>/summarize')
class WeekSummaryAPI(Resource):
    @jwt_required()
    def put(self, week_id):
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
        if not user.admin and not user.instructor:
            return {'message': 'User is not an admin or instructor'}, 401
        if user.instructor and course not in user.instructor.courses:
            return {'message': 'User not an instructor of the course'}, 401
        summary = "summary fetched from GENAI" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        week.summary = summary
        db.session.commit()
        return marshal(week, week_fields)
