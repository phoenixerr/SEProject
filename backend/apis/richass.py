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

api = Namespace(
    "RichAssignments", description="Collection of assignments endpoints that have questinos and options in it", path="/"
)

'''
This is similar to assignemnts endpoint but this also returns the questions and options in the assignment.
The original endpoint is kept for legacy.
'''

option_fields = api.model(  # for adding an option
    "Option",
    {
        "id": fields.Integer(required=True, description="ID of the option", example=1),
        "text": fields.String(
            required=True, description="Text of the option", example="Abc Abc"
        ),
        "is_correct": fields.Boolean(
            required=True,
            description="Boolean, is the current option correct?",
            example=True,
        ),
    },
)

question_fields = api.model(
    "Question",
    {
        "id": fields.Integer,
        "text": fields.String,
        "is_msq": fields.Boolean,
        "assignment_id": fields.Integer,
        "options": fields.List(fields.Nested(option_fields)),
    },
)
assignment_fields = api.model(
    "Assignment",
    {
        "id": fields.Integer(required=True, description='The assignment ID', example=1),
        "title": fields.String(required=True, description='The title of the assignment', example="GA1"),
        "is_graded": fields.Boolean(required=True, description='Is the assignment graded?', example=True),
        "due_date": fields.DateTime(required=True, description='The duedate of the assignment', example="2024-08-1 23:59:59"),
        "week_id": fields.Integer(required=True, description='The Week ID', example=1),
        "questions": fields.List(fields.Nested(question_fields)),
    },
)

@api.route("/week/<int:week_id>/richassignments")
class WeekAssignmentAPI(Resource):
    @jwt_required()
    @api.doc(
        description="Returns all the assignments in the week with the specified week ID of current course",
        params={'week_id':'ID of the user'},
        security = 'jsonWebToken'
    )
    #@api.param('week_id','ID of the user')
    def get(self, week_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 401
        week = Week.query.get(week_id)
        if not week:
            return {"message": "Week not found"}, 401
        course = week.course
        if not course:
            return {"message": "Course not found"}, 401
        if user.student and course not in user.student.courses:
            return {"message": "User not enrolled in course"}, 401
        if user.instructor and course not in user.instructor.courses:
            return {"message": "User is not an instructor of the course"}, 401
        assignments = week.assignments
        return marshal(assignments, assignment_fields)

@api.route("/richassignment/<int:assignment_id>")
class AssignmentAPI(Resource):
    @jwt_required()
    @api.doc(description="Get rich assignment with specified assignment ID",
             security = 'jsonWebToken')
    def get(self, assignment_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 401
        assignment = Assignment.query.get(assignment_id)
        if not assignment:
            return {"message": "Assignment not found"}, 400
        week = assignment.week
        if not week:
            return {"message": "Week not found"}, 401
        course = week.course
        if not course:
            return {"message": "Course not found"}, 401
        if user.student and course not in user.student.courses:
            return {"message": "User not enrolled in course"}, 401
        if user.instructor and course not in user.instructor.courses:
            return {"message": "User is not an instructor of the course"}, 401
        return marshal(assignment, assignment_fields)
