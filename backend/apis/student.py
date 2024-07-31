from datetime import datetime

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

api = Namespace("Student", description="Collection of student endpoints",path='/')

student_fields = api.model(
    "Student",
    {
        "id": fields.Integer,
        "cgpa": fields.Float,
    },
)

student_parser = reqparse.RequestParser()
student_parser.add_argument(
    "cgpa", type=float, required=True, help="CGPA of the student"
)


@api.route("/students")
class StudentsAPI(Resource):
    @jwt_required()
    @api.doc(description="Return details of all student users.")
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 401
        if not user.admin:
            return {"message": "User is not an admin"}, 401
        students = Student.query.all()
        return marshal(students, student_fields)

    # make self as student
    @jwt_required()
    @api.doc(description="Adds current user as a student.")
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 401
        if user.student:
            return {"message": "User is already a student"}, 401
        if user.instructor:
            return {"message": "User is an instructor"}, 401
        if user.admin:
            return {"message": "User is an admin"}, 401
        student = Student(cgpa=0, user=user)
        db.session.add(student)
        db.session.commit()
        return marshal(student, student_fields)


@api.route("/student/<int:student_id>")
class StudentAPI(Resource):
    @jwt_required()
    @api.doc(description="Return details of student of specified user ID.", path="/")
    def get(self, student_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 401
        student = Student.query.get(student_id)
        if not student:
            return {"message": "Student not found"}, 401
        if user.student and student != user.student:
            return {"message": "Unauthorized access"}, 401
        if user.instructor and student not in user.instructor.courses.students:
            return {"message": "Unauthorized access"}, 401
        return marshal(student, student_fields)

    @jwt_required()
    @api.expect(student_parser)
    @api.doc(description="Modify details of student of specified user ID.")
    def put(self, student_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 401
        if not user.admin:
            return {"message": "User is not an admin"}, 401
        student = Student.query.get(student_id)
        if not student:
            return {"message": "Student not found"}, 401
        args = student_parser.parse_args()
        cgpa = args["cgpa"]
        student.cgpa = cgpa
        db.session.commit()
        return marshal(student, student_fields)

    @jwt_required()
    @api.doc(description="Delete  student of specified user ID.")
    def delete(self, student_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 401
        student = Student.query.get(student_id)
        if not student:
            return {"message": "Student not found"}, 401
        if user.student and student != user.student:
            return {"message": "Unauthorized access"}, 401
        if user.instructor:
            return {"message": "Unauthorized access"}, 401
        db.session.delete(student)
        db.session.commit()
        return {"message": "Student deleted"}


@api.route("/course/<int:course_id>/students")
class CourseStudentsAPI(Resource):
    @jwt_required()
    @api.doc(
        description="Get all the students registered for course with specified course ID."
    )
    def get(self, course_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 401
        course = Course.query.get(course_id)
        if not course:
            return {"message": "Course not found"}, 401
        if user.student:
            return {"message": "Unauthorized access"}, 401
        if user.instructor and course not in user.instructor.courses:
            return {"message": "User is not an instructor of the course"}, 401
        students = course.students
        return marshal(students, student_fields)
