from flask import Flask, render_template, url_for, request, session, flash, redirect
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "abc"
app.permanent_session_lifetime = timedelta(minutes=3)

@app.route("/")
def home():
    if "user" in session:
        return render_template("index.html", username=session["user"])
    return render_template("index.html")

@app.route("/link")
def link():
    if "user" not in session:
        return "Please login first"
    return render_template("link.html", user=session["user"])

@app.route("/login", methods=["POST"])
def login():
    session.permanent = True

    username = request.form["username"]
    password = request.form["password"]

    session["user"] = username

    flash("Logged in successfully", "success")
    from flask import Flask, render_template, url_for, request, session, flash, redirect
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "abc"
app.permanent_session_lifetime = timedelta(minutes=3)


@app.route("/")
def home():
    if "user" in session:
        return render_template("index.html", username=session["user"])
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.permanent = True

        username = request.form["username"]
        password = request.form["password"]

        session["user"] = username

        flash("Logged in successfully", "success")
        return redirect(url_for("user"))   # ✅ redirect after login

    return render_template("login.html")   # ✅ show login form


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
    app.run(debug=True)