from main import app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy(app)
migrate = Migrate(app, db)

instructor_course = db.Table('instructor_course',
                             db.Column('instructor_id', db.Integer, db.ForeignKey('instructor.id'), primary_key=True),
                             db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)
                             )

student_course = db.Table('student_course',
                          db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True),
                          db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)
                          )

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), unique=True, nullable=False)
  username = db.Column(db.String(80), unique=True, nullable=False)
  passhash = db.Column(db.String(80), nullable=False)

  @property
  def password(self):
    raise AttributeError('password is not a readable attribute')
  
  @password.setter
  def password(self, password):
    self.passhash = generate_password_hash(password)
  
  def verify_password(self, password):
    return check_password_hash(self.passhash, password)

class Student(db.Model):
  id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)
  user = db.relationship('User', backref=db.backref('student', lazy=True))

  cgpa = db.Column(db.Float, nullable=False)


  courses = db.relationship('Course', secondary=student_course, backref=db.backref('students', lazy=True))

class Instructor(db.Model):
  id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)
  user = db.relationship('User', backref=db.backref('instructor', lazy=True))

  courses = db.relationship('Course', secondary=instructor_course, backref=db.backref('instructors', lazy=True))

class Admin(db.Model):
  id = db.Column(db.Integer, primary_key=True)

  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  user = db.relationship('User', backref=db.backref('admin', lazy=True))

class Course(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), nullable=False)
  level = db.Column(db.Integer, nullable=False, default=1)
  summary = db.Column(db.String(80), nullable=True)


class Week(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  number = db.Column(db.Integer, nullable=False)
  summary = db.Column(db.String(80), nullable=True)

  course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
  course = db.relationship('Course', backref=db.backref('weeks', lazy=True))


class Lecture(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(80), nullable=False)
  url = db.Column(db.String(80), nullable=False)
  summary = db.Column(db.String(80), nullable=True)

  week_id = db.Column(db.Integer, db.ForeignKey('week.id'), nullable=False)
  week = db.relationship('Week', backref=db.backref('lectures', lazy=True))


class Assignment(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(80), nullable=False)
  is_graded = db.Column(db.Boolean, nullable=False)
  due_date = db.Column(db.DateTime, nullable=False)

  week_id = db.Column(db.Integer, db.ForeignKey('week.id'), nullable=False)
  week = db.relationship('Week', backref=db.backref('assignments', lazy=True))

class Question(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  text = db.Column(db.String(80), nullable=False)
  is_msq = db.Column(db.Boolean, nullable=False)

  assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'), nullable=False)
  assignment = db.relationship('Assignment', backref=db.backref('questions', lazy=True))

class Option(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  text = db.Column(db.String(80), nullable=False)
  is_correct = db.Column(db.Boolean, nullable=False)

  question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
  question = db.relationship('Question', backref=db.backref('options', lazy=True))

class Submission(db.Model):
  id = db.Column(db.Integer, primary_key=True)

  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  user = db.relationship('User', backref=db.backref('submissions', lazy=True))

  option_id = db.Column(db.Integer, db.ForeignKey('option.id'), nullable=False)
  option = db.relationship('Option', backref=db.backref('submissions', lazy=True))

class Chat(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  prompt = db.Column(db.String(80), nullable=False)
  response = db.Column(db.String(80), nullable=True)
  datetime = db.Column(db.DateTime, nullable=False)

  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  user = db.relationship('User', backref=db.backref('chats', lazy=True))

  course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=True)
  course = db.relationship('Course', backref=db.backref('chats', lazy=True))


class Event(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(80), nullable=False)
  start = db.Column(db.DateTime, nullable=False)
  end = db.Column(db.DateTime, nullable=False)

  course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=True)
  course = db.relationship('Course', backref=db.backref('planners', lazy=True))

  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  user = db.relationship('User', backref=db.backref('planners', lazy=True))

with app.app_context():
  db.create_all()
  admins = Admin.query.all()
  if not admins:
    user = User(name='admin', username='admin', password='admin')
    admin = Admin(user=user)
    db.session.add(user)
    db.session.add(admin)
  db.session.commit()
