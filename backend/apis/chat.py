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
from genaifuncs import generate_summary_from_transcript
from main import app
from models import (
    Admin,
    Assignment,
    Chat,
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

api = Namespace("Chats", description="Collection of chat endpoints", path="/")

chat_fields = api.model(
    "Chat",
    {
        "id": fields.Integer,
        "prompt": fields.String,
        "response": fields.String,
        "datetime": fields.DateTime,
        "user_id": fields.Integer,
        "course_id": fields.Integer,
    },
)

chat_input_fields = api.model(
    "Chat",
    {
        "prompt": fields.String(
            required=True,
            description="The prompt",
            example="How do I make lists in python?",
        ),
    },
)

chat_parser = reqparse.RequestParser()
chat_parser.add_argument("prompt", type=str, required=True, help="Prompt of the chat")


@api.route("/course/<int:course_id>/chats")
class CourseChatAPI(Resource):
    @jwt_required()
    @api.doc(
        description="Retrieves the chat history of the current user for specified course ID.\nUses Calude LLM",
        security="jsonWebToken",
    )
    def get(self, course_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 401
        course = Course.query.get(course_id)
        if not course:
            return {"message": "Course not found"}, 401
        if user.student and course not in user.student.courses:
            return {"message": "User not enrolled in course"}, 401
        if user.instructor and course not in user.instructor.courses:
            return {"message": "User is not an instructor of the course"}, 401
        # only get the chats for the current user
        chats = Chat.query.filter_by(user=user, course=course).all()
        return marshal(chats, chat_fields)

    @jwt_required()
    @api.expect(chat_input_fields)
    @api.doc(
        description="Add new message in the chat and its response from the LLM for specified course ID.\nUses Claude LLM",
        security="jsonWebToken",
    )
    def post(self, course_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 401
        course = Course.query.get(course_id)
        if not course:
            return {"message": "Course not found"}, 401
        if user.student and course not in user.student.courses:
            return {"message": "User not enrolled in course"}, 401
        if user.instructor and course not in user.instructor.courses:
            return {"message": "User is not an instructor of the course"}, 401
        args = chat_parser.parse_args()
        response = None
        # simluated response
        
        prompt = f"Imageine you are an academic instructor and a student asks you a question, Given below is the history of the conversation between the student and the instructor (you). Give a satisfactory answer. If any non academic answer is asked, tell that you are not allowed to be answering such questions.\n"
        chats = Chat.query.filter_by(user=user, course=course).all()
        chat_history = marshal(chats, chat_fields)
        chat_history = "\n".join(
            [f"{chat['prompt']}\n{chat['response']}" for chat in chat_history]
        )
        chat_history += f"\nStudent: {args['prompt']}"
        print(chat_history)
        response = generate_summary_from_transcript(chat_history, prompt)
        # response = "This is a simulated response"
        chat = Chat(
            prompt=args['prompt'],
            response=response,
            user=user,
            course=course,
        )
        db.session.add(chat)
        db.session.commit()
        return marshal(chat, chat_fields)

    @jwt_required()
    @api.doc(
        description="Delete the chat history of the current user for specified course ID.",
        security="jsonWebToken",
    )
    def delete(self, course_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 401
        course = Course.query.get(course_id)
        if not course:
            return {"message": "Course not found"}, 401
        if user.student and course not in user.student.courses:
            return {"message": "User not enrolled in course"}, 401
        if user.instructor and course not in user.instructor.courses:
            return {"message": "User is not an instructor of the course"}, 401
        chats = course.chats
        for chat in chats:
            db.session.delete(chat)
        db.session.commit()
        return {"message": "Chats deleted"}


# uncoursed chats
@api.route("/chats")
class ChatAPI(Resource):
    @jwt_required()
    @api.doc(
        description="Retrieves the general chat history of the current user.",
        security="jsonWebToken",
    )
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 401
        chats = Chat.query.filter_by(user=user, course=None).all()
        return marshal(chats, chat_fields)

    @jwt_required()
    @api.expect(chat_input_fields)
    @api.doc(
        description="Add new message in the general chat and its response from the LLM.\nUses Calude LLM",
        security="jsonWebToken",
    )
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 401
        args = chat_parser.parse_args()
        response = None
        # simluated response

        prompt = f"Imageine you are an academic instructor and a student asks you a question, Given below is the history of the conversation between the student and the instructor (you). Give a satisfactory answer. If any non academic answer is asked, tell that you are not allowed to be answering such questions.\n"
        chats = Chat.query.filter_by(user=user, course=None).all()
        chat_history = marshal(chats, chat_fields)
        chat_history = "\n".join(
            [f"{chat['prompt']}\n{chat['response']}" for chat in chat_history]
        )
        chat_history += f"\nStudent: {args['prompt']}"
        # print(chat_history)
        response = generate_summary_from_transcript(chat_history, prompt)

        chat = Chat(prompt=args['prompt'], response=response, user=user)
        db.session.add(chat)
        db.session.commit()
        return marshal(chat, chat_fields)

    @jwt_required()
    @api.doc(
        description="Delete the chat history of the current user.",
        security="jsonWebToken",
    )
    def delete(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 401
        chats = Chat.query.filter_by(user=user, course=None).all()
        for chat in chats:
            db.session.delete(chat)
        db.session.commit()
        return {"message": "Chats deleted"}
