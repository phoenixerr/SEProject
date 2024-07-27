from flask_restx import Api, Resource, marshal_with, fields, reqparse, marshal
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from main import app
from models import db, Course, User, Student, Instructor, Admin
from apis import api

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

