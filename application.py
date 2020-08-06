from flask import render_template, Flask, redirect, request,\
    session, flash
from elevation import getElevation
import secrets
import csv
import math
from functools import wraps


app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_urlsafe(16)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
@login_required
def index():
    return render_template('main.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        flash('Please log in')
        return render_template("login.html")
    elif request.method == "POST":
        # Get form information
        password = request.form.get("password")
        # check input is valid
        if password != "0380":
            flash("Invalid password")
            return render_template("login.html")
        session['id'] = "admin"
        return redirect('/')


def load_data(filename):
    """
    Load data from csv
    """
    paths = []
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name_a = row["name_a"]
            lat_a = row["lat_a"]
            lng_a = row["lng_a"]
            name_b = row["name_b"]
            lat_b = row["lat_b"]
            lng_b = row["lng_b"]
            path = [[name_a, lat_a, lng_a], [name_b, lat_b, lng_b]]
            paths.append(path)
    return paths


def getchart(data):
    # Mt. Whitney
    startStr = data[0][1] + "," + data[0][2]
    # "36.578581,-118.291994"
    # Death Valley
    endStr = data[1][1] + "," + data[1][2]
    # "36.23998,-116.83171"
    print(startStr, endStr)
    pathStr = startStr + "|" + endStr
    d = getDistance((data[0][1], data[0][2]), (data[1][1], data[1][2]))
    return [getElevation(pathStr), d]


def getDistance(mk1, mk2):
    R = 6371.0710
    rlat1 = float(mk1[0]) * (math.pi/180)
    rlat2 = float(mk2[0]) * (math.pi/180)
    difflat = rlat2-rlat1
    difflon = (float(mk2[1])-float(mk1[1])) * (math.pi/180)
    d = 2 * R * math.asin(math.sqrt(math.sin(difflat/2)*math.sin(difflat / 2)
                          + math.cos(rlat1)*math.cos(rlat2) *
                          math.sin(difflon/2)*math.sin(difflon/2)))
    return round(d, 2)


if __name__ == '__main__':
    app.run()
