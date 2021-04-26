from flask import Flask, request
import pymongo
from flask_cors import CORS
import sqlite3
import os
import json
from os import environ 
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)
connection_url = 'mongodb+srv://dbUsers:bodoamatwoi@cluster0.wuqpo.mongodb.net/test'
client = pymongo.MongoClient(connection_url)

# Database
Database = client.get_database('tasks')
users  = Database.user

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "tes.db")

with sqlite3.connect(db_path) as data:
    data.row_factory = sqlite3.Row
    cur = data.cursor()
    cur.execute("select * from user")
    rows = cur.fetchall()

def dir():
    files = os.listdir("./static")
    for elem in files:
        print(elem)
    return "Files printed on console"


@app.route("/", methods=["GET"])
def what_ismy_basedir():
    return basedir

@app.route("/testing", methods=["GET"])
def user_profile():
    todos = users.find({}, {'_id': False})
    return json.dumps([todo for todo in todos])

@app.route("/api", methods=["GET"])
def test_hello():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype for testing API .</p>"

@app.route('/view', methods=['GET'])
def view():
    res = []
    for row in rows:
        response = {}
        response["id"] = row["id"]
        response["text"] = row["text"]
        response["day"] = row["days"]
        response["reminder"] = row["reminder"]
        res.append(response)
    return json.dumps(res)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1")
