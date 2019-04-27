from flask import Flask, render_template, app, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user
import pdb

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///collegeproject.db"
app.secret_key = "ABAAIIA)@@@@)@!!(@219129ja"
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def loadUser(user_id):
    return User.query.filter_by(id=user_id).first()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    token = db.Column(db.String(100))
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    city = db.Column(db.String(50))
    region = db.Column(db.String(50))

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    userid = db.Column(db.Integer, ForeignKey(User.id), primary_key=True)
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

@app.route('/about', methods=['GET'])
def viewAbout():
    return render_template("about.html")

@app.route('/signup', methods=['GET'])
def viewSignup():
    return render_template("signup.html")

@app.route('/login', methods=['GET'])
def viewLogin():
    return render_template("login.html")

@app.route('/logout')
def viewLogout():
    logout_user()
    return redirect('/')

@app.route('/api/signup', methods=['POST'])
def apiSignUp():
    try:
        data = request.get_json()
        u = User(fname=data['fname'],
                 lname=data['lname'],
                 city=data['city'],
                 region=data['region'],
                 email=data['email'],
                 password=generate_password_hash(data['password']))
        db.session.add(u)
        db.session.commit()
        ret = {"status": "success"}
        return jsonify(ret)
    except:
        ret = {"status": "failure"}
        return jsonify(ret)

@app.route('/api/login', methods=['POST'])
def apiLogin():
    try:
        data = request.get_json()
        u = User.query.filter_by(email=data['email']).first()

        if(u):
            valid = check_password_hash(str(u.password), data['password'])
            if(valid == True):
                print("User successfully validated.")
                login_user(u)
                ret = {"status": "success"}
                return jsonify(ret)
            else:
                ret = {"status": "failure - incorrect password"}
                return jsonify(ret)
        else:
            ret = {"status": "failure - email not found"}
            return jsonify(ret)
    except:
        ret = {"status": "failure - check sys log"}
        return jsonify(ret)

@app.route('/api/sync', methods=['GET'])
def apiSync():
    isLoggedIn = not current_user.is_anonymous
    ret = {
        "isLoggedIn": isLoggedIn,
    }
    if(isLoggedIn):
        ret['user_email'] = current_user.email

    return jsonify(ret)


@app.route('/profile', methods=['GET'])
@login_required
def viewProfile():
    return render_template("profile.html", user=current_user)

@app.route('/api/get/college/<int:col>', methods=['GET'])
def apiGetCollege(col):
    try:
        query = School.query.filter_by(id=col).first()
        gpaCalc = query.minimum_gpa * 0.01
        ret = {
            "status": "success",
            "id": query.id,
            "name": query.name,
            "location": query.location_city + ", " + query.location_region,
            "established_year": query.established_year,
            "image_url": query.image_url,
            "acceptance_rate": query.acceptance_rate,
            "minimum_gpa": "%.2f" % gpaCalc,
            "minimum_sat": query.minimum_sat_total,
            "minimum_act": query.minimum_act_total
        }
        return jsonify(ret)
    except:
        ret = {
            "status": "failure: check log"
        }
        return jsonify(ret)

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
                           minimum_sat_total=1550,
                           minimum_act_total=0
                           ))
    colleges.append(School(name="University of Central Florida",
                           location_city="Orlando",
                           location_region="Florida",
                           established_year="1963",
                           type="College",
                           image_url="/static/images/ucf.jpg",
                           acceptance_rate=50,
                           minimum_gpa=392,
                           minimum_sat_total=1320,
                           minimum_act_total = 28
                           ))
    colleges.append(School(name="Florida Southern College",
                           location_city="Lakeland",
                           location_region="Florida",
                           established_year="1883",
                           type="College",
                           image_url="/static/images/fsc.jpg",
                           acceptance_rate=51,
                           minimum_gpa=370,
                           minimum_sat_total=1195,
                           minimum_act_total = 26
                           ))
    colleges.append(School(name="Florida Institute of Technology",
                           location_city="Melbourne",
                           location_region="Florida",
                           established_year="1958",
                           type="College",
                           image_url="/static/images/fit.jpg",
                           acceptance_rate=63,
                           minimum_gpa=358,
                           minimum_sat_total=1290,
                           minimum_act_total=26
                           ))
    colleges.append(School(name="University of South Florida",
                           location_city="Tampa",
                           location_region="Florida",
                           established_year="1956",
                           type="College",
                           image_url="/static/images/usf.jpg",
                           acceptance_rate=45,
                           minimum_gpa=394,
                           minimum_sat_total=1230,
                           minimum_act_total=26
                           ))
    colleges.append(School(name="Florida State University",
                           location_city="Tallahassee",
                           location_region="Florida",
                           established_year="1851",
                           type="College",
                           image_url="/static/images/fsu.jpg",
                           acceptance_rate=56,
                           minimum_gpa=391,
                           minimum_sat_total=1290,
                           minimum_act_total=27

                           ))
    colleges.append(School(name="Florida Polytechnic University",
                           location_city="Lakeland",
                           location_region="Florida",
                           established_year="2012",
                           type="College",
                           image_url="/static/images/fpu.jpg",
                           acceptance_rate=55,
                           minimum_gpa=352,
                           minimum_sat_total=1269,
                           minimum_act_total=27
                           ))
    colleges.append(School(name="Florida Agricultural and Mechanical University",
                           location_city="Tallahassee",
                           location_region="Florida",
                           established_year="1887",
                           type="College",
                           image_url="/static/images/famu.jpg",
                           acceptance_rate=46,
                           minimum_gpa=336,
                           minimum_sat_total=1077,
                           minimum_act_total=22
                           ))
    colleges.append(School(name="University of North Florida",
                           location_city="Jacksonville",
                           location_region="Florida",
                           established_year="1972",
                           type="College",
                           image_url="/static/images/unf.jpg",
                           acceptance_rate=59,
                           minimum_gpa=373,
                           minimum_sat_total=640,
                           minimum_act_total=26
                           ))
    colleges.append(School(name="University of Florida",
                           location_city="Gainesville",
                           location_region="Florida",
                           established_year="1905",
                           type="College",
                           image_url="/static/images/uf.jpg",
                           acceptance_rate=38,
                           minimum_gpa=376,
                           minimum_sat_total=1240,
                           minimum_act_total=32
                           ))

    db.session.add_all(colleges)
    db.session.commit()

if(__name__ == "__main__"):
    app.run(debug=True)
