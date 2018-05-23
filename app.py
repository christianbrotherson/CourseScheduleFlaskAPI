from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=False)
    description = db.Column(db.Text, unique=False)

    def __init__(self, title, description):
        self.title = title
        self.description = description


class CourseSchema(ma.Schema):
    class Meta:
        fields = ('title', 'description')


course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)

# Endpoint to create a new course
@app.route('/course', methods=["POST"])
def add_course():
    title = request.json['title']
    description = request.json['description']

    new_course = Course(title, description)

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

    course.title = title
    course.description = description

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