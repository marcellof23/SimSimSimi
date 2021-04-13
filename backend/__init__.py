from . import db
from backend.db import get_db
from flask import current_app, g
import sqlite3
import os
from flask_cors import CORS
from flask import Flask
import json
basedir = os.path.abspath(os.path.dirname(__file__))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "tes.db")


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'tes.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/", methods=["GET"])
    def what_ismy_basedir():
        return basedir

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/demo', methods=['GET'])
    def demos():
        response = dict()
        response['a'] = 'A'
        response['b'] = 'B'
        response['c'] = 'C'
        return json.dumps(response)

    @app.route('/view', methods=['GET'])
    def view():
        with sqlite3.connect(db_path) as db:
            db.row_factory = sqlite3.Row
            cur = db.cursor()
            cur.execute("select * from user")
            rows = cur.fetchall()
        res = []
        for row in rows:
            response = {}
            response["id"] = row["id"]
            response["text"] = row["text"]
            response["day"] = row["days"]
            response["reminder"] = row["reminder"]
            res.append(response)
        return json.dumps(res)

    db.init_app(app)

    return app
