from flask_restx import Api, Resource, marshal_with, fields, reqparse, marshal
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from main import app
from models import db, Course, User, Student, Instructor, Admin
from apis import api

enrollment_fields = api.model('Enrollment', {
    'course_id': fields.Integer,
    'user_id': fields.Integer,
})

enrollment_parser = reqparse.RequestParser()
enrollment_parser.add_argument('course_id', type=int, required=True, help='Course ID')
enrollment_parser.add_argument('user_id', type=int, required=True, help='User ID')

@api.route('/student/<int:user_id>/enroll/<int:course_id>')
class StudentEnrollmentAPI(Resource):
    @jwt_required()
    def post(self, user_id, course_id):
        self_id = get_jwt_identity()
        user = User.query.get(self_id)
        if not user:
            return {'message': 'User not found'}, 401
        if not user.admin:
            return {'message': 'User is not an admin'}, 401
        student = Student.query.get(user_id)
        if not student:
            return {'message': 'Student not found'}, 401
        course = Course.query.get(course_id)
        if not course:
            return {'message': 'Course not found'}, 401
        if course in student.courses:
            return {'message': 'Student already enrolled in course'}, 400
        student.courses.append(course)
        db.session.commit()
        response = {
            'user_id': user_id,
            'course_id': course_id,
        }
        return marshal(response, enrollment_fields)
    @jwt_required()
    def get(self, user_id, course_id):
        self_id = get_jwt_identity()
        user = User.query.get(self_id)
        if not user:
            return {'message': 'User not found'}, 401
        if not user.admin:
            return {'message': 'User is not an admin'}, 401
        student = Student.query.get(user_id)
        if not student:
            return {'message': 'Student not found'}, 401
        course = Course.query.get(course_id)
        if not course:
            return {'message': 'Course not found'}, 401
        if course not in student.courses:
            return {'message': 'Student not enrolled in course'}, 400
        response = {
            'user_id': user_id,
            'course_id': course_id,
        }
        return marshal(response, enrollment_fields)
    @jwt_required()
    def delete(self, user_id, course_id):
        self_id = get_jwt_identity()
        user = User.query.get(self_id)
        if not user:
            return {'message': 'User not found'}, 401
        if not user.admin:
            return {'message': 'User is not an admin'}, 401
        student = Student.query.get(user_id)
        if not student:
            return {'message': 'Student not found'}, 401
        course = Course.query.get(course_id)
        if not course:
            return {'message': 'Course not found'}, 401
        if course not in student.courses:
            return {'message': 'Student not enrolled in course'}, 400
        student.courses.remove(course)
        db.session.commit()
        return {'message': 'Enrollment removed'}, 200
    
@api.route('/instructor/<int:user_id>/teach/<int:course_id>')
class InstructorTeachAPI(Resource):
    @jwt_required()
    def post(self, user_id, course_id):
        self_id = get_jwt_identity()
        user = User.query.get(self_id)
        if not user:
            return {'message': 'User not found'}, 401
        if not user.admin:
            return {'message': 'User is not an admin'}, 401
        instructor = Instructor.query.get(user_id)
        if not instructor:
            return {'message': 'Instructor not found'}, 401
        course = Course.query.get(course_id)
        if not course:
            return {'message': 'Course not found'}, 401
        if course in instructor.courses:
            return {'message': 'Instructor already teaching course'}, 400
        instructor.courses.append(course)
        db.session.commit()
        response = {
            'user_id': user_id,
            'course_id': course_id,
        }
        return marshal(response, enrollment_fields)
    @jwt_required()
    def get(self, user_id, course_id):
        self_id = get_jwt_identity()
        user = User.query.get(self_id)
        if not user:
            return {'message': 'User not found'}, 401
        if not user.admin:
            return {'message': 'User is not an admin'}, 401
        instructor = Instructor.query.get(user_id)
        if not instructor:
            return {'message': 'Instructor not found'}, 401
        course = Course.query.get(course_id)
        if not course:
            return {'message': 'Course not found'}, 401
        if course not in instructor.courses:
            return {'message': 'Instructor not teaching course'}, 400
        response = {
            'user_id': user_id,
            'course_id': course_id,
        }
        return marshal(response, enrollment_fields)
    @jwt_required()
    def delete(self, user_id, course_id):
        self_id = get_jwt_identity()
        user = User.query.get(self_id)
        if not user:
            return {'message': 'User not found'}, 401
        if not user.admin:
            return {'message': 'User is not an admin'}, 401
        instructor = Instructor.query.get(user_id)
        if not instructor:
            return {'message': 'Instructor not found'}, 401
        course = Course.query.get(course_id)
        if not course:
            return {'message': 'Course not found'}, 401
        if course not in instructor.courses:
            return {'message': 'Instructor not teaching course'}, 400
        instructor.courses.remove(course)
        db.session.commit()
        return {'message': 'Teaching removed'}, 200
