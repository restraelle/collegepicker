from flask import Flask, render_template, app, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///collegeproject.db"
db = SQLAlchemy(app)


class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    token = db.Column(db.String(100))


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    userid = db.Column(db.Integer, ForeignKey(User.uid), primary_key=True)
    firstname = db.Column(db.String(40))
    middlename = db.Column(db.String(40))
    lastname = db.Column(db.String(40))
    user = relationship('User', foreign_keys='Student.userid')
    sat_math_score = db.Column(db.Integer)
    sat_readwrite_score = db.Column(db.Integer)
    act_read_score = db.Column(db.Integer)
    act_write_score = db.Column(db.Integer)
    act_math_score = db.Column(db.Integer)
    act_science_score = db.Column(db.Integer)
    act_english_score = db.Column(db.Integer)
    act_total_score = db.Column(db.Integer)


class School(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(200))
    location_city = db.Column(db.String(50))
    location_region = db.Column(db.String(50))
    established_year = db.Column(db.String(4))
    type = db.Column(db.String(30))
    image_url = db.Column(db.String(200))
    acceptance_rate = db.Column(db.Integer)
    minimum_gpa = db.Column(db.Integer)
    minimum_sat_math = db.Column(db.Integer)
    minimum_sat_readwrite = db.Column(db.Integer)
    minimum_sat_total = db.Column(db.Integer)
    minimum_act_total = db.Column(db.Integer)

@app.route('/')
def viewIndex():
    return render_template("index.html")

@app.route('/colleges', methods=['GET'])
def viewColleges():
    query = School.query.all()
    for row in query:
        row.minimum_gpa = row.minimum_gpa * 0.01
    return render_template("colleges.html", colleges=query)

@app.route('/compare', methods=['GET'])
def viewCompare():
    query = School.query.all()
    return render_template("compare.html", colleges=query)

def createCollegeData():
    colleges = []
    colleges.append(School(name="Harvard University",
                           location_city="Cambridge",
                           location_region="Massachusetts",
                           established_year="1636",
                           type="College",
                           image_url="/static/images/harvard.jpg",
                           acceptance_rate=5,
                           minimum_gpa=404,
                           minimum_sat_total=1550
                           ))
    colleges.append(School(name="University of Central Florida",
                           location_city="Orlando",
                           location_region="Florida",
                           established_year="1963",
                           type="College",
                           image_url="/static/images/ucf.jpg",
                           acceptance_rate=50,
                           minimum_gpa=392,
                           minimum_sat_total=1320
                           ))
    colleges.append(School(name="Florida Southern College",
                           location_city="Lakeland",
                           location_region="Florida",
                           established_year="1883",
                           type="College",
                           image_url="/static/images/fsc.jpg",
                           acceptance_rate=51,
                           minimum_gpa=370,
                           minimum_sat_total=1195
                           ))
    colleges.append(School(name="Florida Institute of Technology",
                           location_city="Melbourne",
                           location_region="Florida",
                           established_year="1958",
                           type="College",
                           image_url="/static/images/fit.jpg",
                           acceptance_rate=63,
                           minimum_gpa=358,
                           minimum_sat_total=1290
                           ))
    colleges.append(School(name="University of South Florida",
                           location_city="Tampa",
                           location_region="Florida",
                           established_year="1956",
                           type="College",
                           image_url="/static/images/usf.jpg",
                           acceptance_rate=45,
                           minimum_gpa=394,
                           minimum_sat_total=1230
                           ))
    colleges.append(School(name="Florida State University",
                           location_city="Tallahassee",
                           location_region="Florida",
                           established_year="1851",
                           type="College",
                           image_url="/static/images/fsu.jpg",
                           acceptance_rate=56,
                           minimum_gpa=391,
                           minimum_sat_total=1290
                           ))
    colleges.append(School(name="Florida Polytechnic University",
                           location_city="Lakeland",
                           location_region="Florida",
                           established_year="2012",
                           type="College",
                           image_url="/static/images/fpu.jpg",
                           acceptance_rate=55,
                           minimum_gpa=352,
                           minimum_sat_total=1269
                           ))
    colleges.append(School(name="Florida Agricultural and Mechanical University",
                           location_city="Tallahassee",
                           location_region="Florida",
                           established_year="1887",
                           type="College",
                           image_url="/static/images/famu.jpg",
                           acceptance_rate=46,
                           minimum_gpa=336,
                           minimum_sat_total=1077
                           ))
    colleges.append(School(name="University of North Florida",
                           location_city="Jacksonville",
                           location_region="Florida",
                           established_year="1972",
                           type="College",
                           image_url="/static/images/unf.jpg",
                           acceptance_rate=59,
                           minimum_gpa=373,
                           minimum_sat_total=640
                           ))
    colleges.append(School(name="University of Florida",
                           location_city="Gainesville",
                           location_region="Florida",
                           established_year="1905",
                           type="College",
                           image_url="/static/images/uf.jpg",
                           acceptance_rate=38,
                           minimum_gpa=376,
                           minimum_sat_total=1240
                           ))

    db.session.add_all(colleges)
    db.session.commit()

if(__name__ == "__main__"):
    app.run(debug=True)
