from flask_restx import Api, Resource, marshal_with, fields, reqparse, marshal
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from main import app
from models import db, Course, User, Student, Instructor, Admin



api = Api(app,
          title='SE Project Team 7',
          description='This document outlines the collection of all the endpoints used in the project')

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

from apis.assignment import api as assignment_namespace
from apis.auth import api as auth_namespace
from apis.chat import api as chat_namespace
from apis.course import api as course_namespace
from apis.enrollment import api as enrollment_namespace
from apis.event import api as event_namespace
from apis.instructor import api as instructor_namespace
from apis.lecture import api as lecture_namespace
from apis.option import api as option_namespace
from apis.question import api as question_namespace
from apis.student import api as student_namespace
from apis.user import api as user_namespace
from apis.week import api as week_namespace

api.add_namespace(assignment_namespace)
api.add_namespace(auth_namespace)
api.add_namespace(chat_namespace)
api.add_namespace(course_namespace)
api.add_namespace(enrollment_namespace)
api.add_namespace(event_namespace)
api.add_namespace(instructor_namespace)
api.add_namespace(lecture_namespace)
api.add_namespace(option_namespace)
api.add_namespace(question_namespace)
api.add_namespace(student_namespace)
api.add_namespace(user_namespace)
api.add_namespace(week_namespace)

@api.route('/debug/db_populate')
class DebugDBPopulateAPI(Resource):
    @api.doc(description = "Used for debugging.\nAllows us to quickly drop all entried and repopulate the table.")
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
        
