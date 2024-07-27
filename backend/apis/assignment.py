from flask_restx import Api, Resource, marshal_with, fields, reqparse, marshal
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from main import app
from models import db, Course, User, Student, Instructor, Admin, Week, Lecture, Assignment, Question, Option, Submission
from apis import api
from datetime import datetime

assignment_fields = api.model('Assignment', {
    'id': fields.Integer,
    'title': fields.String,
    'is_graded': fields.Boolean,
    'due_date': fields.DateTime,
    'week_id': fields.Integer,
})

assignment_parser = reqparse.RequestParser()
assignment_parser.add_argument('title', type=str, required=True, help='Title of the assignment')
assignment_parser.add_argument('is_graded', type=bool, required=True, help='Is the assignment graded?')
assignment_parser.add_argument('due_date', type=str, required=True, help='Due date of the assignment')

@api.route('/week/<int:week_id>/assignments')
class WeekAssignmentAPI(Resource):
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
        assignments = week.assignments
        return marshal(assignments, assignment_fields)

    @jwt_required()
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
        args = assignment_parser.parse_args()
        title = args['title']
        is_graded = args['is_graded']
        due_date = args['due_date']
        try:
            due_date = datetime.strptime(due_date, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return {'message': 'Invalid due date format. Please use YYYY-MM-DD HH:MM:SS'}, 400
        assignment = Assignment(title=title, is_graded=is_graded, due_date=due_date, week=week)
        db.session.add(assignment)
        db.session.commit()
        return marshal(assignment, assignment_fields)

@api.route('/assignment/<int:assignment_id>')
class AssignmentAPI(Resource):
    @jwt_required()
    def get(self, assignment_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 401
        assignment = Assignment.query.get(assignment_id)
        if not assignment:
            return {'message': 'Assignment not found'}, 400
        week = assignment.week
        if not week:
            return {'message': 'Week not found'}, 401
        course = week.course
        if not course:
            return {'message': 'Course not found'}, 401
        if user.student and course not in user.student.courses:
            return {'message': 'User not enrolled in course'}, 401
        if user.instructor and course not in user.instructor.courses:
            return {'message': 'User is not an instructor of the course'}, 401
        return marshal(assignment, assignment_fields)

    @jwt_required()
    def put(self, assignment_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return {'message': 'User not found'}, 401

        if not user.admin and not user.instructor:
            return {'message': 'User is not an admin or instructor'}, 401

        assignment = Assignment.query.get(assignment_id)
        if not assignment:
            return {'message': 'Assignment not found'}, 400
        week = assignment.week
        if not week:
            return {'message': 'Week not found'}, 401
        course = week.course
        if not course:
            return {'message': 'Course not found'}, 401
        if user.instructor and course not in user.instructor.courses:
            return {'message': 'User is not an instructor of the course'}, 401
        args = assignment_parser.parse_args()
        title = args['title']
        is_graded = args['is_graded']
        due_date = args['due_date']
        try:
            due_date = datetime.strptime(due_date, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return {'message': 'Invalid due date format. Please use YYYY-MM-DD HH:MM:SS'}, 400
        assignment.title = title
        assignment.is_graded = is_graded
        assignment.due_date = due_date
        db.session.commit()
        return marshal(assignment, assignment_fields)

    @jwt_required()
    def delete(self, assignment_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 401
        if not user.admin and not user.instructor:
            return {'message': 'User is not an admin or instructor'}, 401
        assignment = Assignment.query.get(assignment_id)
        if not assignment:
            return {'message': 'Assignment not found'}, 400
        week = assignment.week
        if not week:
            return {'message': 'Week not found'}, 401
        course = week.course
        if not course:
            return {'message': 'Course not found'}, 401
        if user.instructor and course not in user.instructor.courses:
            return {'message': 'User is not an instructor of the course'}, 401
        db.session.delete(assignment)
        db.session.commit()
        return {'message': 'Assignment deleted successfully'}, 200