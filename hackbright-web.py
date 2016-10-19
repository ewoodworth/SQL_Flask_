from flask import Flask, request, render_template

from flask.ext.sqlalchemy import SQLAlchemy

import hackbright

app = Flask(__name__)

db = SQLAlchemy()

# def connect_to_db(app):
#     """Connect us to HB DB"""

#     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hackbright'
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     db.app = app
#     db.init_app(app)

@app.route('/')
def show_homepage():
    """Show homepage"""

    all_students = hackbright.get_all_students() 
    all_projects = hackbright.get_all_projects() 

    return render_template('index.html', all_students=all_students, all_projects=all_projects)

@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github', 'jhacks')
    first, last, github = hackbright.get_student_by_github(github)


    grades_all = hackbright.get_grades_by_github(github)

    return render_template('student.html', first=first, last=last, github=github, grades_all=grades_all)


@app.route('/student_search')
def get_student_form():
    """Show form to allow user input of student github name."""

    return render_template('student_search.html')


@app.route("/student_add", methods=['POST'])
def add_student():
    """Add new student"""

    first = request.form.get('first') 
    last = request.form.get('last')
    github = request.form.get('github')

    hackbright.make_new_student(first, last, github)

    return render_template("confirmation.html", github=github)


@app.route('/project')
def get_project():
    """Get project details by project title. """

    title = request.args.get('title')
    title, description, max_score = hackbright.get_project_by_title(title)

    all_grades = hackbright.get_grades_by_title(title)

    return render_template('projects.html', title=title, description=description, max_score=max_score, all_grades=all_grades)

@app.route("/project_add", methods=['POST'])
def add_project():
    """Add new project"""

    title = request.form.get('title') 
    description = request.form.get('description')
    max_grade = request.form.get('max_grade')

    hackbright.make_new_project(title, description, max_grade)

    return render_template("confirm_project.html", title=title)


@app.route("/grade_add", methods=['POST'])
def add_grade():
    """Adds or updates students grade on a given project"""

    github = request.form.get('student')
    title = request.form.get('project')
    grade = request.form.get('grade')

    hackbright.assign_grade(github, title, grade)

    return render_template("confirm_grade.html", title=title, github=github, grade=grade)

@app.route("/forms")
def get_grade():
    """ Form for getting and assigning a new grade to a student on a project"""

    all_students = hackbright.get_all_students() 
    all_projects = hackbright.get_all_projects() 

    return render_template('forms.html', all_projects=all_projects, all_students=all_students)


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
