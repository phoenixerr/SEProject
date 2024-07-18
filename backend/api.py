from flask_restx import Api, Resource, marshal_with, fields
from main import app
from models import Course

api = Api(app)

course_fields = api.model('Course', {
                          'id': fields.Integer,
                          'name': fields.String,
  })


@api.route('/courses')
class CourseAPI(Resource):
    @marshal_with(course_fields)
    def get(self):
      courses = Course.query.all()
      return courses
