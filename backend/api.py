from flask_restx import Api, Resource, marshal_with, fields, reqparse, marshal
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from main import app
from models import db, Course, User, Student, Instructor, Admin

api = Api(app)
jwt = JWTManager(app)

course_fields = api.model('Course', {
                          'id': fields.Integer,
                          'name': fields.String,
                          'level': fields.Integer,
  })

course_parser = reqparse.RequestParser()
course_parser.add_argument('name', type=str, required=True, help='Name of the course')
course_parser.add_argument('level', type=int, required=True, help='Level of the course')



@api.route('/courses')
class CourseAPI(Resource):
    @marshal_with(course_fields)
    @jwt_required()
    def get(self):
      user_id = get_jwt_identity()
      user = User.query.get(user_id)
      if user:
        if user.student:
          courses = user.student.courses
        elif user.instructor:
          courses = user.instructor.courses
        else:
          courses = Course.query.all()
      else:
        return {'message': 'User not found'}, 401
      return courses

    @jwt_required()
    def post(self):
      user_id = get_jwt_identity()
      user = User.query.get(user_id)
      if not user:
        return {'message': 'User not found'}, 401

      if not user.admin:
          return {'message': 'User is not an admin'}, 401
      args = course_parser.parse_args()
      name = args['name']
      level = args['level']
      try:
        level = int(level)
      except ValueError:
        return {'message': 'Level must be an integer'}, 400
      course = Course(name=name, level=level)
      db.session.add(course)
      db.session.commit()
      return marshal(course, course_fields)
    
@api.route('/course/<int:course_id>')
class CourseAPI(Resource):
  def get(self, course_id):
    course = Course.query.get(course_id)
    if not course:
      return {'message': 'Course not found'}, 400
    return marshal(course, course_fields)

  @jwt_required()
  def put(self, course_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
      return {'message': 'User not found'}, 401

    if not user.admin:
      return {'message': 'User is not an admin'}, 401

    args = course_parser.parse_args()
    name = args['name']
    level = args['level']
    try:
      level = int(level)
    except ValueError:
      return {'message': 'Level must be an integer'}, 400

    course = Course.query.get(course_id)
    if not course:
      return {'message': 'Course not found'}, 400

    course.name = name
    course.level = level
    db.session.commit()
    return marshal(course, course_fields)

  @jwt_required()
  def delete(self, course_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
      return {'message': 'User not found'}, 401

    if not user.admin:
      return {'message': 'User is not an admin'}, 401
    
    course = Course.query.get(course_id)
    if not course:
      return {'message': 'Course not found'}, 400
    
    db.session.delete(course)
    db.session.commit()
    return {'message': 'Course deleted'}


@api.route('/login')
class LoginAPI(Resource):
  def post(self):
    username = api.payload.get('username')
    password = api.payload.get('password')
    user = User.query.filter_by(username=username).first()
    if user and user.verify_password(password):
      access_token = create_access_token(identity=user.id)
      return {'access_token': access_token}
    else:
      return {'message': 'Invalid credentials'}, 401


user_fields = api.model('User', {
                        'id': fields.Integer(description='ID of the user'),
                        'name': fields.String(description='Name of the user'),
                        'username': fields.String(description='Username of the user'),
                        })

user_parser = reqparse.RequestParser()
user_parser.add_argument(
    'name', type=str, required=True, help='Name of the user')
user_parser.add_argument('username', type=str,
                         required=True, help='Username of the user')
user_parser.add_argument('password', type=str,
                         required=True, help='Password of the user')


@api.route('/user')
class UserAPI(Resource):
  @marshal_with(user_fields)
  @jwt_required()
  def get(self):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if user:
      return user
    else:
      return {'message': 'User not found'}, 401

  @jwt_required()
  def put(self):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
      return {'message': 'User not found'}, 401
    args = user_parser.parse_args()
    name = args['name']
    username = args['username']
    password = args['password']
    collision = User.query.filter_by(username=username).first()
    if collision and collision.id != user_id:
      return {'message': 'Username already exists'}, 400
    user.name = name
    user.username = username
    user.password = password
    db.session.commit()
    return marshal(user, user_fields)

  def post(self):
    args = user_parser.parse_args()
    name = args['name']
    username = args['username']
    password = args['password']
    user = User(name=name, username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return marshal(user, user_fields)

  @jwt_required()
  def delete(self):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
      return {'message': 'User not found'}, 401
    db.session.delete(user)
    return {'message': 'User deleted'}


@api.route('/users')
class UsersAPI(Resource):
  @marshal_with(user_fields)
  def get(self):
    users = User.query.all()
    return users
