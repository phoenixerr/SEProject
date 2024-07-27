from flask_restx import Api, Resource, marshal_with, fields, reqparse, marshal
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from main import app
from models import db, Course, User, Student, Instructor, Admin, Week, Lecture, Assignment, Question, Option, Submission, Chat, Event
from apis import api
from datetime import datetime

event_fields = api.model('Event', {
    'id': fields.Integer,
    'title': fields.String,
    'start': fields.DateTime,
    'end': fields.DateTime,
    'course_id': fields.Integer,
    'user_id': fields.Integer,
})

event_parser = reqparse.RequestParser()
event_parser.add_argument('title', type=str, required=True, help='Title of the event')
event_parser.add_argument('start', type=str, required=True, help='Start date of the event')
event_parser.add_argument('end', type=str, required=True, help='End date of the event')

@api.route('/course/<int:course_id>/events')
class CourseEventAPI(Resource):
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
        events = Event.query.filter_by(course=course, user=user).order_by(Event.start).all()
        return marshal(events, event_fields)

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
        args = event_parser.parse_args()
        title = args['title']
        try:
            start = datetime.strptime(args['start'], '%Y-%m-%d %H:%M:%S')
            end = datetime.strptime(args['end'], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return {'message': 'Start and end must be in the format YYYY-MM-DD HH:MM:SS'}, 400
        event = Event(title=title, start=start, end=end, course=course, user=user)
        db.session.add(event)
        db.session.commit()
        return marshal(event, event_fields)

@api.route('/event/<int:event_id>')
class EventAPI(Resource):
    @jwt_required()
    def get(self, event_id):
        event = Event.query.get(event_id)
        if not event:
            return {'message': 'Event not found'}, 401
        if event.user.id != get_jwt_identity():
            return {'message': 'Unauthorized'}, 401
        return marshal(event, event_fields)

    @jwt_required()
    def put(self, event_id):
        event = Event.query.get(event_id)
        if not event:
            return {'message': 'Event not found'}, 401
        if event.user.id != get_jwt_identity():
            return {'message': 'Unauthorized'}, 401
        args = event_parser.parse_args()
        event.title = args['title']
        try:
            event.start = datetime.strptime(args['start'], '%Y-%m-%d %H:%M:%S')
            event.end = datetime.strptime(args['end'], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return {'message': 'Start and end must be in the format YYYY-MM-DD HH:MM:SS'}, 400
        db.session.commit()
        return marshal(event, event_fields)

    @jwt_required()
    def delete(self, event_id):
        event = Event.query.get(event_id)
        if not event:
            return {'message': 'Event not found'}, 401
        if event.user.id != get_jwt_identity():
            return {'message': 'Unauthorized'}, 401
        db.session.delete(event)
        db.session.commit()
        return {'message': 'Event deleted'}, 200
