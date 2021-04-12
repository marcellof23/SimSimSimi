from flask import Flask, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))


def dir():
    files = os.listdir("./static")
    for elem in files:
        print(elem)
    return "Files printed on console"


@app.route("/", methods=["GET"])
def what_ismy_basedir():
    return basedir


@app.route("/api", methods=["GET"])
def test_hello():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype for testing API .</p>"


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1")
