from flask_restx import Api, Resource, marshal_with, fields, reqparse, marshal
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from main import app
from models import db, Course, User, Student, Instructor, Admin, Week, Lecture, Assignment, Question, Option, Submission
from apis import api
from datetime import datetime

student_fields = api.model('Student', {
    'id': fields.Integer,
    'cgpa': fields.Float,
})

student_parser = reqparse.RequestParser()
student_parser.add_argument('cgpa', type=float, required=True, help='CGPA of the student')

@api.route('/students')
class StudentsAPI(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 401
        if not user.admin:
            return {'message': 'User is not an admin'}, 401
        students = Student.query.all()
        return marshal(students, student_fields)

    # make self as student
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 401
        if user.student:
            return {'message': 'User is already a student'}, 401
        if user.instuctor:
            return {'message': 'User is an instructor'}, 401
        if user.admin:
            return {'message': 'User is an admin'}, 401
        student = Student(cgpa=0, user=user)
        db.session.add(student)
        db.session.commit()
        return marshal(student, student_fields)

@api.route('/student/<int:student_id>')
class StudentAPI(Resource):
    @jwt_required()
    def get(self, student_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 401
        student = Student.query.get(student_id)
        if not student:
            return {'message': 'Student not found'}, 401
        if user.student and student != user.student:
            return {'message': 'Unauthorized access'}, 401
        if user.instructor and student not in user.instructor.courses.students:
            return {'message': 'Unauthorized access'}, 401
        return marshal(student, student_fields)

    @jwt_required()
    def put(self, student_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 401
        if not user.admin:
            return {'message': 'User is not an admin'}, 401
        student = Student.query.get(student_id)
        if not student:
            return {'message': 'Student not found'}, 401
        args = student_parser.parse_args()
        cgpa = args['cgpa']
        student.cgpa = cgpa
        db.session.commit()
        return marshal(student, student_fields)

    @jwt_required()
    def delete(self, student_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 401
        student = Student.query.get(student_id)
        if not student:
            return {'message': 'Student not found'}, 401
        if user.student and student != user.student:
            return {'message': 'Unauthorized access'}, 401
        if user.instructor:
            return {'message': 'Unauthorized access'}, 401
        db.session.delete(student)
        db.session.commit()
        return {'message': 'Student deleted'}

@api.route('/course/<int:course_id>/students')
class CourseStudentsAPI(Resource):
    @jwt_required()
    def get(self, course_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 401
        course = Course.query.get(course_id)
        if not course:
            return {'message': 'Course not found'}, 401
        if user.student :
            return {'message': 'Unauthorized access'}, 401
        if user.instructor and course not in user.instructor.courses:
            return {'message': 'User is not an instructor of the course'}, 401
        students = course.students
        return marshal(students, student_fields)