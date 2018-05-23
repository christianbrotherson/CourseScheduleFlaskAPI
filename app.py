from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

from flask_cors import CORS

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=False)
    description = db.Column(db.Text, unique=False)
    enrolled = db.Column(db.Boolean, unique=False)
    open = db.Column(db.Boolean, unique=False)

    def __init__(self, title, description, enrolled, open):
        self.title = title
        self.description = description
        self.enrolled = enrolled
        self.open = open


class CourseSchema(ma.Schema):
    class Meta:
        fields = ('title', 'description', 'enrolled', 'open')


course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)

# Endpoint to create a new course
@app.route('/course', methods=["POST"])
def add_course():
    title = request.json['title']
    description = request.json['description']
    enrolled = False
    open = False

    new_course = Course(title, description, enrolled, open)

    db.session.add(new_course)
    db.session.commit()

    course = Course.query.get(new_course.id)

    return course_schema.jsonify(course)


# Endpoint to query a single course
@app.route('/course/<id>', methods=["GET"])
def get_course(id):
    course = Course.query.get(id)
    return course_schema.jsonify(course)


# Endpoint to query all courses
@app.route('/courses', methods=["GET"])
def get_courses():
    all_courses = Course.query.all()
    result = courses_schema.dump(all_courses)

    return jsonify(result.data)


# Endpoint to update a course
@app.route('/course/<id>', methods=["PUT"])
def update_course(id):
    course = Course.query.get(id)
    title = request.json['title']
    description = request.json['description']
    enrolled = False

    course.title = title
    course.description = description
    course.enrolled = enrolled

    db.session.commit()
    return course_schema.jsonify(course)


# Endpoint to delete a course
@app.route('/course/<id>', methods=["DELETE"])
def delete_course(id):
    course = Course.query.get(id)
    db.session.delete(course)
    db.session.commit()

    return course_schema.jsonify(course)


if __name__ == '__main__':
    app.run(debug=True)