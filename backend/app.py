from flask import Flask, request
import time
import pymongo
from flask_cors import CORS
import os
import json
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)
DATABASE = os.getenv('DATABASE')
client = pymongo.MongoClient(DATABASE)

# Database
Database = client.get_database('tasks')
users  = Database.user

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "tes.db")

def dir():
    files = os.listdir("./static")
    for elem in files:
        print(elem)
    return "Files printed on console"

@app.route("/", methods=["GET"])
def what_ismy_basedir():
    return basedir

@app.route("/view", methods=["GET"])
def user_profile():
    todos = users.find({}, {'_id': False})
    return json.dumps([todo for todo in todos])


@app.route("/api", methods=["GET"])
def test_hello():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype for testing API .</p>"

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1")
