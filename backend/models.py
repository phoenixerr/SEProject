from datetime import datetime

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from main import app
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy(app)
migrate = Migrate(app, db)

instructor_course = db.Table(
    "instructor_course",
    db.Column(
        "instructor_id", db.Integer, db.ForeignKey("instructor.id"), primary_key=True
    ),
    db.Column("course_id", db.Integer, db.ForeignKey("course.id"), primary_key=True),
)

student_course = db.Table(
    "student_course",
    db.Column("student_id", db.Integer, db.ForeignKey("student.id"), primary_key=True),
    db.Column("course_id", db.Integer, db.ForeignKey("course.id"), primary_key=True),
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    passhash = db.Column(db.String(80), nullable=False)

    chats = db.relationship(
        "Chat", backref=db.backref("user", lazy=True), cascade="all, delete-orphan"
    )

    events = db.relationship(
        "Event", backref=db.backref("user", lazy=True), cascade="all, delete-orphan"
    )

    student = db.relationship(
        "Student",
        backref=db.backref("user", lazy=True),
        single_parent=True,
        uselist=False,
    )

    instructor = db.relationship(
        "Instructor",
        backref=db.backref("user", lazy=True),
        single_parent=True,
        uselist=False,
    )

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.passhash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.passhash, password)


class Student(db.Model):
    id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False, primary_key=True
    )

    cgpa = db.Column(db.Float, nullable=False)

    courses = db.relationship(
        "Course",
        secondary=student_course,
        backref=db.backref("students", lazy=True),
    )


class Instructor(db.Model):
    id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False, primary_key=True
    )
    courses = db.relationship(
        "Course",
        secondary=instructor_course,
        backref=db.backref("instructors", lazy=True),
    )


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship(
        "User",
        backref=db.backref("admin", lazy=True),
        cascade="all, delete-orphan",
        single_parent=True,
    )


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    level = db.Column(db.Integer, nullable=False, default=1)
    summary = db.Column(db.String(8000), nullable=True)

    weeks = db.relationship(
        "Week",
        backref=db.backref("course", lazy=True),
        cascade="all, delete-orphan",
    )

    chats = db.relationship(
        "Chat",
        backref=db.backref("course", lazy=True),
        cascade="all, delete-orphan",
    )

    events = db.relationship(
        "Event",
        backref=db.backref("course", lazy=True),
        cascade="all, delete-orphan",
    )


class Week(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    summary = db.Column(db.String(8000), nullable=True)

    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)

    lectures = db.relationship(
        "Lecture",
        backref=db.backref("week", lazy=True),
        cascade="all, delete-orphan",
    )

    assignments = db.relationship(
        "Assignment",
        backref=db.backref("week", lazy=True),
        cascade="all, delete-orphan",
    )


class Lecture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    url = db.Column(db.String(80), nullable=False)
    summary = db.Column(db.String(8000), nullable=True)

    week_id = db.Column(db.Integer, db.ForeignKey("week.id"), nullable=False)


class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    is_graded = db.Column(db.Boolean, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)

    week_id = db.Column(db.Integer, db.ForeignKey("week.id"), nullable=False)
    questions = db.relationship(
        "Question",
        backref=db.backref("assignment", lazy=True),
        cascade="all, delete-orphan",
    )


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(80), nullable=False)
    is_msq = db.Column(db.Boolean, nullable=False)

    assignment_id = db.Column(
        db.Integer, db.ForeignKey("assignment.id"), nullable=False
    )
    options = db.relationship(
        "Option",
        backref=db.backref("question", lazy=True),
        cascade="all, delete-orphan",
    )


class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(80), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)

    question_id = db.Column(db.Integer, db.ForeignKey("question.id"), nullable=False)

    submissions = db.relationship(
        "Submission",
        backref=db.backref("option", lazy=True),
        cascade="all, delete-orphan",
    )


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", backref=db.backref("submissions", lazy=True))

    option_id = db.Column(db.Integer, db.ForeignKey("option.id"), nullable=False)


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prompt = db.Column(db.String(80), nullable=False)
    response = db.Column(db.String(80), nullable=True)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=True)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)

    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


with app.app_context():
    db.create_all()
    admins = Admin.query.all()
    if not admins:
        user = User(name="admin", username="admin", password="admin")
        admin = Admin(user=user)
        db.session.add(user)
        db.session.add(admin)
    db.session.commit()
