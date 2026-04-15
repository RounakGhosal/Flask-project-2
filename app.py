from flask import Flask, render_template, url_for, request, session, flash, redirect
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "abc"
app.permanent_session_lifetime = timedelta(minutes=3)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(100), nullable=False)

@app.route("/")
def home():
    if "user" in session:
        return render_template("index.html", username=session["user"])
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        session.permanent = True

        username = request.form["username"]
        password = generate_password_hash(request.form["password"])
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registered successfully", "success")
        return redirect(url_for("user"))   

    return render_template("register.html")  

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.permanent = True

        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password,password):
            flash("Logged in successfully", "success")
            session["user"] = username
            return redirect(url_for("user"))  
        else:
            flash("Invalid credentials","error")
            return redirect(url_for("login"))

    return render_template("login.html")   


@app.route("/link")
def link():
    if "user" not in session:
        flash("Please login first", "error")
        return redirect(url_for("login"))
    return render_template("link.html", user=session["user"])


@app.route("/user")
def user():
    if "user" in session:
        return render_template("user.html", user=session["user"])
    else:
        flash("You are not logged in", "error")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out successfully!", "success")
    return redirect(url_for("login"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
