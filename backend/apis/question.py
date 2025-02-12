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
from genaifuncs import generate_summary_from_transcript, get_transcript
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

question_input_fields = api.model(
    "Question",
    {
        "text": fields.String(
            required=True,
            description="The text of the question",
            example="What are examples of lists ih python?",
        ),
        "is_msq": fields.Boolean(
            required=True, description="Is the question multiple select?", example=False
        ),
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
        description="Get all the questions in assignment with specified assignment ID.",
        security="jsonWebToken",
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
    @api.expect(question_input_fields)
    @api.doc(
        description="Add questions to the assignment with specified assignment ID.",
        security="jsonWebToken",
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
    @api.doc(
        description="Return the details of question with specified question ID.",
        security="jsonWebToken",
    )
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
    @api.expect(question_input_fields)
    @api.doc(
        description="Modify the parameters of question with specified question ID.",
        security="jsonWebToken",
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
    @api.doc(
        description="Delete the details of question with specified question ID.",
        security="jsonWebToken",
    )
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
        description="Returns options marked by current student for question with specified question ID.",
        security="jsonWebToken",
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


@api.route("/question/generate/<int:week_id>")
class QuestionGenerateAPI(Resource):
    @jwt_required()
    @api.doc(
        description="Generate questions for the week with specified week ID.",
        security="jsonWebToken",
    )
    def get(self, week_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 401
        if not user.admin and not user.instructor:
            return {"message": "User is not an admin or instructor"}, 401
        week = Week.query.get(week_id)
        if not week:
            return {"message": "Week not found"}, 401
        course = week.course
        if not course:
            return {"message": "Course not found"}, 401
        if user.instructor and course not in user.instructor.courses:
            return {"message": "User is not an instructor of the course"}, 401

        # generate questions from genai

        lecture_data = []
        lectures = week.lectures
        for lecture in lectures:
            current_lecture = []
            current_lecture.append(lecture.title)
            current_lecture.append("https://youtu.be/" + lecture.url)
            lecture_data.append(current_lecture)

        lecture_string = ""
        print(lecture_data)
        for lecture in lecture_data:
            lecture_string += f"## {lecture[0]}\n{lecture[1]}\n\n"

        prompt = f"You are an instructor for a course in python. You have been asked to create a quiz for the students. The quiz should contain questions based on the following lecture links. Do the following for each lecture: The questions should be multiple choice questions. The correct answer should be the one that is most relevant to the lecture content. The other options should be incorrect. The questions should be clear and concise. For each lecture, generated 5 or 6 questions and the corresponding options. Make it markdown formatted. The h1 title should be week number, which is {week_id}.\n\n"

        questions = generate_summary_from_transcript(lecture_string, prompt)

        return {"questions_answers": questions}
