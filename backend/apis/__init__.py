from flask_restx import Api, Resource, marshal_with, fields, reqparse, marshal
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from main import app
from models import db, Course, User, Student, Instructor, Admin

api = Api(app)
jwt = JWTManager(app)


import apis.auth
import apis.course
import apis.user
import apis.enrollment
import apis.instructor
import apis.student
import apis.week
import apis.lecture
import apis.assignment
import apis.question
import apis.option
import apis.event
import apis.chat

@api.route('/debug/db_populate')
class DebugDBPopulateAPI(Resource):
    def post(self):
        db.drop_all()
        db.create_all()
        user = User(name='admin', username='admin', password='admin')
        admin = Admin(user=user)
        db.session.add(user)
        db.session.add(admin)
        students = [
            "Sayan Ghosh",
            "Ashwin Hebbar",
            "Prabuddh Mathur",
            "Anirudh Murthy",
            "Rituparna Das",
            "Vaishnavi Dwivedi",
            "Vignesh Babu",
        ]
        for name in students:
            user = User(name=name, username=name.lower().split()[0], password='1234')
            student = Student(user=user,cgpa=8.0)
            db.session.add(user)
            db.session.add(student)
        instructors = ["Karthik Thiagarajan", "Santhana Krishnan", "Atul PS", "Adarsh Madre"]
        for name in instructors:
            user = User(name=name, username=name.lower().split()[0], password='1234')
            instructor = Instructor(user=user)
            db.session.add(user)
            db.session.add(instructor)

        courses = [
            ("Programming in Python", 1),
            ("System Commands", 2),
            ("Programming, Data Structures and Algorithms", 2),
            ("Modern Application Development I", 2),
        ]
        for name, level in courses:
            course = Course(name=name, level=level)
            db.session.add(course)
        
        db.session.commit()
        return {'message': 'Database populated'}
        
