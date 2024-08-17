from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required,
)
from flask_restx import Api, Resource, fields, marshal, marshal_with, reqparse
from main import app
from models import (
    Admin,
    Course,
    Instructor,
    Student,
    User,
    Week,
    Lecture,
    Assignment,
    Question,
    Option,
    Submission,
    Chat,
    Event,
    instructor_course,
    student_course,
    db,
)
from datetime import datetime


bearer_authorizations = {
    "jsonWebToken": {"type": "apiKey", "in": "header", "name": "Authorization"}
}

api = Api(
    app,
    title="SE Project Team 7",
    description="This document outlines the collection of all the endpoints used in the project",
    authorizations=bearer_authorizations,
    default="DB Populate and Testing",
    default_label="DB Populate and Testing",
)

jwt = JWTManager(app)

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


@api.route("/debug/db_populate")
class DebugDBPopulateAPI(Resource):
    @api.doc(
        description="Used for debugging.\nAllows us to quickly drop all entried and repopulate the table."
    )
    def post(self):
        db.drop_all()
        db.create_all()
        user = User(name="admin", username="admin", password="admin")
        admin = Admin(user=user)
        db.session.add(user)
        db.session.add(admin)

        # add students
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
            user = User(name=name, username=name.lower().split()[0], password="1234")
            student = Student(user=user, cgpa=8.5)
            db.session.add(user)
            db.session.add(student)

        # add instructors
        instructors = [
            "Karthik Thiagarajan",
            "Santhana Krishnan",
            "Atul PS",
            "Adarsh Madre",
        ]
        for name in instructors:
            user = User(name=name, username=name.lower().split()[0], password="1234")
            instructor = Instructor(user=user)
            db.session.add(user)
            db.session.add(instructor)

        # add courses
        courses = [
            ("Programming in Python", 1),
            ("System Commands", 2),
            ("Programming, Data Structures and Algorithms", 2),
            ("Modern Application Development I", 2),
        ]
        for name, level in courses:
            course = Course(name=name, level=level)
            db.session.add(course)

        # add instructors to teach courses
        instructor_course_entries = [(9, 1), (10, 1)]
        for instructorid, courseid in instructor_course_entries:
            instructor=Instructor.query.get(instructorid)
            course=Course.query.get(courseid)
            instructor.courses.append(course)

        # add students to teach courses
        student_course_entries = [(2, 1), (3, 1), (4, 1), (5, 1)]
        for studentid, courseid in student_course_entries:
            student=Student.query.get(studentid)
            course=Course.query.get(courseid)
            student.courses.append(course)

        # add weeks
        weeks = [
            (1, "Basics of python", 1),
            (2, "Using Replit", 1),
            (3, "Datatypes in python", 1),
        ]
        for week_number, week_summary, courseid in weeks:
            week_entry = Week(
                number=week_number, summary=week_summary, course_id=courseid
            )
            db.session.add(week_entry)

        # add lectures
        lectures = [
            (
                "Introduction to python",
                "8ndsDXohLMQ",
                "Summary of the lecture 'Intro to python'",
                1,
            ),
            (
                "How to install python",
                "8ndsDXohLMQ",
                "Summary of the lecture 'How to install python'",
                1,
            ),
            (
                "First programs",
                "8ndsDXohLMQ",
                "Summary of the lecture 'First programs'",
                1,
            ),
            (
                "Introduction to Replit",
                "8ndsDXohLMQ",
                "Summary of the lecture 'Intro to Replit'",
                2,
            ),
            (
                "Using Replit",
                "8ndsDXohLMQ",
                "Summary of the lecture 'Using Replit'",
                2,
            ),
            (
                "Introduction to Dictioanries",
                "8ndsDXohLMQ",
                "Summary of the lecture 'Intro to Dictionaries'",
                3,
            ),
            (
                "Introduction to Lists",
                "8ndsDXohLMQ",
                "Summary of the lecture 'Intro to Lists'",
                3,
            ),
        ]
        for title,url,summary,weekid in lectures:
            lecture_entry=Lecture(title=title,url=url,summary=summary,week_id=weekid)
            db.session.add(lecture_entry)

        # add assignments
        assignments = [
            ("GA1", True, datetime(2024,8,1,23,59,59), 1),
            ("GA2", True, datetime(2024,8,8,23,59,59), 2),
            ("GA3", True, datetime(2024,8,15,23,59,59), 3),
        ]
        for title,graded,duedate,weekid in assignments:
            assignment_entry=Assignment(title=title,is_graded=graded,due_date=duedate,week_id=weekid)
            db.session.add(assignment_entry)

        # add questions
        questions = [
            (
                'What is the data type of the following variable in Python?\nmy_var = "Hello, World!"',
                False,
                1,
            ),
            (
                "Which of the following is used to define a multi-line comment in Python?",
                False,
                1,
            ),
            ("What is Replit primarily used for?", False, 2),
            ("Which of the following is NOT a core feature of Replit?", False, 2),
            ("What are examples of lists ih python?", True, 3),
            ("What are examples of dictionaries ih python?", True, 3),
        ]
        for q_text,msq,assignmentid in questions:
            question_entry=Question(text=q_text,is_msq=msq,assignment_id=assignmentid)
            db.session.add(question_entry)


        # add options to questions
        options = [
            ("IntegerFloatStringBoolean", False, 1),
            ("Float", False, 1),
            ("String", True, 1),
            ("Boolean", False, 1),
            ("\/* */", False, 1),
            ("//", False, 1),
            ("#", False, 1),
            ("Triple quotes (''' or \"\"\")", True, 1),
            ("Creating and sharing static websites", False, 2),
            ("Developing and running code in various programming languages", True, 2),
            ("Managing large-scale database systems", False, 2),
            ("Designing complex graphical user interfaces", False, 2),
            ("Real-time collaboration", False, 2),
            ("Built-in terminal", False, 2),
            ("Code versioning", True, 2),
            ("Deployment options", False, 2),
            ('[1, 2, 3, "hello"]', True, 3),
            ('["abc", "def", "ijk"]', True, 3),
            ('{"name": "Alice", "age": 30}', False, 3),
            ("12345", False, 3),
            ('[1, 2, 3, "hello"]', False, 3),
            ('["abc", "def", "ijk"]', False, 3),
            ('{"name": "Alice", "age": 30}', True, 3),
            ("12345", False, 3),
        ]
        for op_text,correct,quesid in options:
            option_entry=Option(text=op_text,is_correct=correct,question_id=quesid)
            db.session.add(option_entry)

        # add submissions
        submissions = [(2, 3), (2, 8), (2, 17), (2, 18)]
        for userid,optionid in submissions:
            submission_entry=Submission(user_id=userid,option_id=optionid)
            db.session.add(submission_entry)

        # add events
        events = [
            ("OPPE Due", datetime(2024,8,1,23,59,59), datetime(2024,8,8,23,59,59), 1, 2),
            ("Hall Ticket issued", datetime(2024,8,1,23,59,59), datetime(2024,8,8,23,59,59), 1, 2),
            ("Hall Ticket issued", datetime(2024,8,1,23,59,59), datetime(2024,8,8,23,59,59), 1, 3),
            ("OPPE Due", datetime(2024,8,1,23,59,59), datetime(2024,8,8,23,59,59), 1, 3),
        ]
        for event_title,startdate,enddate,courseid,userid in events:
            event_entry=Event(title=event_title,start=startdate,end=enddate,course_id=courseid,user_id=userid)
            db.session.add(event_entry)

        # add chats
        chats = [
            (
                "How do you swap the values of two variables in Python without using a temporary variable?",
                "Use tuple unpacking: a, b = b, a",
                datetime(2024,7,28,20,50,59),
                2,
                1,
            ),
            (
                "What is the difference between a list and a tuple in Python?",
                "Lists are mutable (can be changed), while tuples are immutable (cannot be changed).",
                datetime(2024,7,28,20,52,59),
                2,
                1,
            ),
            (
                "How do you check if a string is a palindrome in Python?",
                "Reverse the string and compare it to the original string. If they are equal, it's a palindrome.",
                datetime(2024,7,28,20,51,59),
                3,
                1,
            ),
            (
                "Explain the use of the enumerate() function in Python.",
                "enumerate() adds a counter to an iterable and returns it as an enumerate object.",
                datetime(2024,7,28,20,53,59),
                3,
                1,
            ),
        ]
        for chat_prompt,resp,time,userid,courseid in chats:
            chat_entry=Chat(prompt=chat_prompt,response=resp,datetime=time,user_id=userid,course_id=courseid)
            db.session.add(chat_entry)

        db.session.commit()
        return {"message": "Database populated"}
