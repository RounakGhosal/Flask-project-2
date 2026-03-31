from flask import Flask, render_template, url_for, request, session
app = Flask(__name__)
app.secret_key = "abc"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/link")
def link():
    return render_template("link.html")

@app.route("/submit", methods=["POST"])
def submit():
    username = request.form["username"]
    password = request.form["password"]
    session["user"] = username
    session["pass"] = password
    return render_template("index.html", username=username, password=password)

if __name__ == "__main__":
    app.run(debug=True)