from datetime import datetime

from apis import api
from apis.option import option_fields
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

api = Namespace("Questions", description="Collection of question endpoints", path="/")

question_fields = api.model(
    "Question",
    {
        "id": fields.Integer,
        "text": fields.String,
        "is_msq": fields.Boolean,
        "assignment_id": fields.Integer,
    },
)

question_parser = reqparse.RequestParser()
question_parser.add_argument(
    "text", type=str, required=True, help="Text of the question"
)
question_parser.add_argument(
    "is_msq", type=bool, required=True, help="Is the question multiple select?"
)


@api.route("/assignment/<int:assignment_id>/questions")
class AssignmentQuestionAPI(Resource):
    @jwt_required()
    @api.doc(
        description="Get all the questions in assignment with specified assignment ID."
    )
    def get(self, assignment_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 401
        assignment = Assignment.query.get(assignment_id)
        if not assignment:
            return {"message": "Assignment not found"}, 401
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
        questions = assignment.questions
        return marshal(questions, question_fields)

    @jwt_required()
    @api.expect(question_parser)
    @api.doc(
        description="Add questions to the assignment with specified assignment ID."
    )
    def post(self, assignment_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 401
        if not user.admin and not user.instructor:
            return {"message": "User is not an admin or instructor"}, 401
        assignment = Assignment.query.get(assignment_id)
        if not assignment:
            return {"message": "Assignment not found"}, 401
        week = assignment.week
        if not week:
            return {"message": "Week not found"}, 401
        course = week.course
        if not course:
            return {"message": "Course not found"}, 401
        if user.instructor and course not in user.instructor.courses:
            return {"message": "User is not an instructor of the course"}, 401
        args = question_parser.parse_args()
        text = args["text"]
        is_msq = bool(args["is_msq"])
        question = Question(text=text, is_msq=is_msq, assignment=assignment)
        db.session.add(question)
        db.session.commit()
        return marshal(question, question_fields)


@api.route("/question/<int:question_id>")
class QuestionAPI(Resource):
    @jwt_required()
    @api.doc(description="Return the details of question with specified question ID.")
    def get(self, question_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 401
        question = Question.query.get(question_id)
        if not question:
            return {"message": "Question not found"}, 401
        assignment = question.assignment
        if not assignment:
            return {"message": "Assignment not found"}, 401
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
        return marshal(question, question_fields)

    @jwt_required()
    @api.expect(question_parser)
    @api.doc(
        description="Modify the parameters of question with specified question ID."
    )
    def put(self, question_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 401
        if not user.admin and not user.instructor:
            return {"message": "User is not an admin or instructor"}, 401
        question = Question.query.get(question_id)
        if not question:
            return {"message": "Question not found"}, 401
        assignment = question.assignment
        if not assignment:
            return {"message": "Assignment not found"}, 401
        week = assignment.week
        if not week:
            return {"message": "Week not found"}, 401
        course = week.course
        if not course:
            return {"message": "Course not found"}, 401
        if user.instructor and course not in user.instructor.courses:
            return {"message": "User is not an instructor of the course"}, 401
        args = question_parser.parse_args()
        text = args["text"]
        is_msq = bool(args["is_msq"])
        question.text = text
        question.is_msq = is_msq
        db.session.commit()
        return marshal(question, question_fields)

    @jwt_required()
    @api.doc(description="Delete the details of question with specified question ID.")
    def delete(self, question_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 401
        if not user.admin and not user.instructor:
            return {"message": "User is not an admin or instructor"}, 401
        question = Question.query.get(question_id)
        if not question:
            return {"message": "Question not found"}, 401
        assignment = question.assignment
        if not assignment:
            return {"message": "Assignment not found"}, 401
        week = assignment.week
        if not week:
            return {"message": "Week not found"}, 401
        course = week.course
        if not course:
            return {"message": "Course not found"}, 401
        if user.instructor and course not in user.instructor.courses:
            return {"message": "User is not an instructor of the course"}, 401
        db.session.delete(question)
        db.session.commit()
        return {"message": "Question deleted"}, 200


@api.route("/question/<int:question_id>/marked")
class QuestionMarkedAPI(Resource):
    @jwt_required()
    @api.doc(
        description="Returns options marked by current student for question with specified question ID."
    )
    def get(self, question_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 401
        if not user.student:
            return {"message": "User is not a student"}, 401
        question = Question.query.get(question_id)
        if not question:
            return {"message": "Question not found"}, 401
        assignment = question.assignment
        if not assignment:
            return {"message": "Assignment not found"}, 401
        week = assignment.week
        if not week:
            return {"message": "Week not found"}, 401
        course = week.course
        if not course:
            return {"message": "Course not found"}, 401
        if user.student and course not in user.student.courses:
            return {"message": "User not enrolled in course"}, 401
        options = question.options
        marked = []
        for option in options:
            submission = Submission.query.filter_by(user=user, option=option).first()
            if submission:
                marked.append(option)
        return marshal(marked, option_fields)
