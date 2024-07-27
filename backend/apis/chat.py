from flask_restx import Api, Resource, marshal_with, fields, reqparse, marshal
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from main import app
from models import db, Course, User, Student, Instructor, Admin, Week, Lecture, Assignment, Question, Option, Submission, Chat
from apis import api
from datetime import datetime

chat_fields = api.model('Chat', {
    'id': fields.Integer,
    'prompt': fields.String,
    'response': fields.String,
    'datetime': fields.DateTime,
    'user_id': fields.Integer,
    'course_id': fields.Integer,
})

chat_parser = reqparse.RequestParser()
chat_parser.add_argument('prompt', type=str, required=True, help='Prompt of the chat')

@api.route('/course/<int:course_id>/chats')
class CourseChatAPI(Resource):
    @jwt_required()
    def get(self, course_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 401
        course = Course.query.get(course_id)
        if not course:
            return {'message': 'Course not found'}, 401
        if user.student and course not in user.student.courses:
            return {'message': 'User not enrolled in course'}, 401
        if user.instructor and course not in user.instructor.courses:
            return {'message': 'User is not an instructor of the course'}, 401
        chats = course.chats
        return marshal(chats, chat_fields)

    @jwt_required()
    def post(self, course_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 401
        course = Course.query.get(course_id)
        if not course:
            return {'message': 'Course not found'}, 401
        if user.student and course not in user.student.courses:
            return {'message': 'User not enrolled in course'}, 401
        if user.instructor and course not in user.instructor.courses:
            return {'message': 'User is not an instructor of the course'}, 401
        args = chat_parser.parse_args()
        prompt = args['prompt']
        response = None
        datetime = datetime.now()
        # simluated response
        response = "Default response from GENAI"
        chat = Chat(prompt=prompt, response=response, datetime=datetime, user=user, course=course)
        db.session.add(chat)
        db.session.commit()
        return marshal(chat, chat_fields)

    @jwt_required()
    def delete(self, course_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 401
        course = Course.query.get(course_id)
        if not course:
            return {'message': 'Course not found'}, 401
        if user.student and course not in user.student.courses:
            return {'message': 'User not enrolled in course'}, 401
        if user.instructor and course not in user.instructor.courses:
            return {'message': 'User is not an instructor of the course'}, 401
        chats = course.chats
        for chat in chats:
            db.session.delete(chat)
        db.session.commit()
        return {'message': 'Chats deleted'}


# uncoursed chats
@api.route('/chats')
class ChatAPI(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 401
        chats = Chat.query.filter_by(user=user, course=None).all()
        return marshal(chats, chat_fields)

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 401
        args = chat_parser.parse_args()
        prompt = args['prompt']
        response = None
        datetime = datetime.now()
        # simluated response
        response = "Default response from GENAI"
        chat = Chat(prompt=prompt, response=response, datetime=datetime, user=user)
        db.session.add(chat)
        db.session.commit()
        return marshal(chat, chat_fields)

    @jwt_required()
    def delete(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 401
        chats = Chat.query.filter_by(user=user, course=None).all()
        for chat in chats:
            db.session.delete(chat)
        db.session.commit()
        return {'message': 'Chats deleted'}