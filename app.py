from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)
from flask import session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

import numpy as np
import pickle


# APP

app = Flask(__name__)

app.secret_key = "supersecretkey"

# DATABASE

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)



# LOGIN MANAGER


login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"



# LOAD MODEL

model = pickle.load(open("breast_model.pkl", "rb"))



# USER TABLE


class UserModel(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(300),
        nullable=False
    )

# PREDICTION TABLE


class Prediction(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    mean_radius = db.Column(db.Float)

    mean_texture = db.Column(db.Float)

    mean_perimeter = db.Column(db.Float)

    mean_area = db.Column(db.Float)

    mean_smoothness = db.Column(db.Float)

    worst_radius = db.Column(db.Float)

    result = db.Column(db.String(50))

    confidence = db.Column(db.Float)



# USER CLASS


class User(UserMixin):

    def __init__(self, username):

        self.id = username


@login_manager.user_loader
def load_user(user_id):

    return User(user_id)



# REGISTER


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        existing_user = UserModel.query.filter_by(
            username=username
        ).first()

        if existing_user:

            return render_template(
                "register.html",
                error="Username Already Exists"
            )

        hashed_password = generate_password_hash(password)

        new_user = UserModel(
            username=username,
            password=hashed_password
        )

        db.session.add(new_user)

        db.session.commit()

        flash("Registration Successful")

        return redirect(url_for("login"))

    return render_template("register.html")



# LOGIN


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        user = UserModel.query.filter_by(
            username=username
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):

            login_user(User(user.username))

            return redirect(url_for("home"))

        return render_template(
            "login.html",
            error="Invalid Username or Password"
        )

    return render_template("login.html")



# FORGOT PASSWORD


@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():

    if request.method == "POST":

        username = request.form["username"]

        new_password = request.form["new_password"]

        user = UserModel.query.filter_by(
            username=username
        ).first()

        if not user:

            return render_template(
                "forgot_password.html",
                error="User Not Found"
            )

        user.password = generate_password_hash(
            new_password
        )

        db.session.commit()

        flash("Password Updated Successfully")

        return redirect(url_for("login"))

    return render_template("forget_password.html")



# LOGOUT


@app.route('/logout')
def logout():
    session.clear()   # removes all session data (user login info)
    return redirect(url_for('login'))



# HOME


@app.route("/")
@login_required
def home():

    return render_template(
        "index.html",
        prediction_text=None
    )



# PREDICT


@app.route("/predict", methods=["POST"])
@login_required
def predict():

    try:

        features = [
            float(x)
            for x in request.form.values()
        ]

        np_features = np.array(
            features
        ).reshape(1, -1)

        prediction = model.predict(
            np_features
        )

        probability = model.predict_proba(
            np_features
        )

        confidence = round(
            np.max(probability) * 100,
            2
        )

        output = (
            "Not Cancerous"
            if prediction[0] == 1
            else "Cancerous"
        )

        new_prediction = Prediction(

            mean_radius=features[0],

            mean_texture=features[1],

            mean_perimeter=features[2],

            mean_area=features[3],

            mean_smoothness=features[4],

            worst_radius=features[5],

            result=output,

            confidence=confidence
        )

        db.session.add(new_prediction)

        db.session.commit()

        return render_template(

            "index.html",

            prediction_text=output,

            confidence=confidence
        )

    except Exception as e:

        return render_template(

            "index.html",

            prediction_text=f"Error: {e}"
        )


# CREATE DATABASE

with app.app_context():

    db.create_all()


# RUN APP

if __name__ == "__main__":
    app.run(debug=True)