from flask import Flask, render_template, url_for, request, session, flash
app = Flask(__name__)
app.secret_key = "abc"

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

@app.route("/submit", methods=["POST"])
def submit():
    username = request.form["username"]
    password = request.form["password"]
    session["user"] = username
    flash("Logged in succesfully","success")
    return render_template("index.html", username=username)

if __name__ == "__main__":
    app.run(debug=True)