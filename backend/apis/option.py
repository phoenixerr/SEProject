from flask_restx import Api, Resource, marshal_with, fields, reqparse, marshal
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from main import app
from models import db, Course, User, Student, Instructor, Admin, Week, Lecture, Assignment, Question, Option, Submission
from apis import api
from datetime import datetime


option_fields = api.model('Option', {
    'id': fields.Integer,
    'text': fields.String,
    'is_correct': fields.Boolean,
    'question_id': fields.Integer,
})

option_parser = reqparse.RequestParser()
option_parser.add_argument('text', type=str, required=True, help='Text of the option')
option_parser.add_argument('is_correct', type=bool, required=True, help='Is the option correct?')

@api.route('/question/<int:question_id>/options')
class QuestionOptionAPI(Resource):
    @jwt_required()
    def get(self, question_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 401
        question = Question.query.get(question_id)
        if not question:
            return {'message': 'Question not found'}, 401
        assignment = question.assignment
        if not assignment:
            return {'message': 'Assignment not found'}, 401
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
        options = question.options
        return marshal(options, option_fields)

    @jwt_required()
    def post(self, question_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 401
        if not user.admin and not user.instructor:
            return {'message': 'User is not an admin or instructor'}, 401
        question = Question.query.get(question_id)
        if not question:
            return {'message': 'Question not found'}, 401
        assignment = question.assignment
        if not assignment:
            return {'message': 'Assignment not found'}, 401
        week = assignment.week
        if not week:
            return {'message': 'Week not found'}, 401
        course = week.course
        if not course:
            return {'message': 'Course not found'}, 401
        if user.instructor and course not in user.instructor.courses:
            return {'message': 'User is not an instructor of the course'}, 401
        args = option_parser.parse_args()
        text = args['text']
        is_correct = bool(args['is_correct'])
        option = Option(text=text, is_correct=is_correct, question=question)
        db.session.add(option)
        db.session.commit()
        return marshal(option, option_fields)

@api.route('/option/<int:option_id>')
class OptionAPI(Resource):
    @jwt_required()
    def get(self, option_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 401
        option = Option.query.get(option_id)
        if not option:
            return {'message': 'Option not found'}, 401
        question = option.question
        if not question:
            return {'message': 'Question not found'}, 401
        assignment = question.assignment
        if not assignment:
            return {'message': 'Assignment not found'}, 401
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
        return marshal(option, option_fields)

    @jwt_required()
    def put(self, option_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return {'message': 'User not found'}, 401

        if not user.admin and not user.instructor:
            return {'message': 'User is not an admin or instructor'}, 401

        option = Option.query.get(option_id)
        if not option:
            return {'message': 'Option not found'}, 401
        question = option.question
        if not question:
            return {'message': 'Question not found'}, 401
        assignment = question.assignment
        if not assignment:
            return {'message': 'Assignment not found'}, 401
        week = assignment.week
        if not week:
            return {'message': 'Week not found'}, 401
        course = week.course
        if not course:
            return {'message': 'Course not found'}, 401
        if user.instructor and course not in user.instructor.courses:
            return {'message': 'User is not an instructor of the course'}, 401
        args = option_parser.parse_args()
        text = args['text']
        is_correct = bool(args['is_correct'])
        option.text = text
        option.is_correct = is_correct
        db.session.commit()
        return marshal(option, option_fields)

    @jwt_required()
    def delete(self, option_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return {'message': 'User not found'}, 401

        if not user.admin and not user.instructor:
            return {'message': 'User is not an admin or instructor'}, 401

        option = Option.query.get(option_id)
        if not option:
            return {'message': 'Option not found'}, 401
        question = option.question
        if not question:
            return {'message': 'Question not found'}, 401
        assignment = question.assignment
        if not assignment:
            return {'message': 'Assignment not found'}, 401
        week = assignment.week
        if not week:
            return {'message': 'Week not found'}, 401
        course = week.course
        if not course:
            return {'message': 'Course not found'}, 401
        if user.instructor and course not in user.instructor.courses:
            return {'message': 'User is not an instructor of the course'}, 401
        db.session.delete(option)
        db.session.commit()
        return {'message': 'Option deleted successfully'}, 200


@api.route('/option/<int:option_id>/submit')
class OptionSubmitAPI(Resource):
    @jwt_required()
    def post(self, option_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 401
        option = Option.query.get(option_id)
        if not option:
            return {'message': 'Option not found'}, 401
        question = option.question
        if not question:
            return {'message': 'Question not found'}, 401
        assignment = question.assignment
        if not assignment:
            return {'message': 'Assignment not found'}, 401
        if assignment.due_date < datetime.now():
            return {'message': 'Assignment is already ended'}, 401
        week = assignment.week
        if not week:
            return {'message': 'Week not found'}, 401
        course = week.course
        if not course:
            return {'message': 'Course not found'}, 401
        if not user.student:
            return {'message': 'User is not a student'}, 401
        if user.student and course not in user.student.courses:
            return {'message': 'User not enrolled in course'}, 401
        already_exists = Submission.query.filter_by(user=user, option=option).first()
        if already_exists:
            return {'message': 'User has already submitted this option'}, 200
        submission = Submission(user=user, option=option)
        db.session.add(submission)
        db.session.commit()
        return {'message': 'Submission successful'}, 200

    @jwt_required()
    def delete(self, option_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 401
        option = Option.query.get(option_id)
        if not option:
            return {'message': 'Option not found'}, 401
        question = option.question
        if not question:
            return {'message': 'Question not found'}, 401
        assignment = question.assignment
        if not assignment:
            return {'message': 'Assignment not found'}, 401
        if assignment.due_date < datetime.now():
            return {'message': 'Assignment is already ended'}, 401
        week = assignment.week
        if not week:
            return {'message': 'Week not found'}, 401
        course = week.course
        if not course:
            return {'message': 'Course not found'}, 401
        if not user.student:
            return {'message': 'User is not a student'}, 401
        if user.student and course not in user.student.courses:
            return {'message': 'User not enrolled in course'}, 401
        submission = Submission.query.filter_by(user=user, option=option).first()
        if not submission:
            return {'message': 'Submission not found'}, 401
        db.session.delete(submission)
        db.session.commit()
        return {'message': 'Submission deleted successfully'}, 200