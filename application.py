from flask import render_template, Flask, request,\
    flash, abort, url_for, redirect
from elevation import getElevation
import secrets
import csv
import math
from flask_login import LoginManager,\
 login_required, login_user, UserMixin
from urllib.parse import urlparse, urljoin


app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_urlsafe(16)
app.config['SESSION_PERMANENT'] = True
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


class User(UserMixin):
    pass


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


@login_manager.user_loader
def load_user(user_id):
    user = User()
    user.id = user_id
    return user


@app.route("/")
@login_required
def index():
    return render_template('main.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        if request.form.get('password') == '0380':
            # Login and validate the user.
            user = User()
            user.id = 'admin'
            login_user(user, True)
            flash('登入成功')

            next = request.args.get('next')
            if not is_safe_url(next):
                return abort(400)
            return redirect(next or url_for('index'))
        else:
            flash('密碼錯誤')
            return render_template('login.html')


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
