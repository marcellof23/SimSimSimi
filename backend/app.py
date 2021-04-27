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

@app.route('/views', methods=['GET'])

def add_task(args):

	'''
	fitur 1
	menambahkan task ke database
	menampilkan pesan feedback ke interface juga
	ngehandle argumen kurang juga, kayak kurang tanggal (?)

	deskripsi argumen
	-- args: 
	dict yang isinya bisa {tanggal, nama matkul, jenis task, topik}
	
	'''

def show_tasks(args):
	'''
	fitur 2
	menampilkan daftar task ke interface
	
	deskripsi argumen
	-- args: 
	dict yang isinya bisa {date_awal, date_akhir, n_minggu, n_hari}
	kalo n_hari = 0, berarti hari ini
	'''

def show_deadline(args):
	'''
	fitur 3
	menampilkan deadline task

	deskripsi argumen
	-- args:
	dict yang isinya bisa {nama matkul, jenis task}
	'''

def update_task_deadline(args):
	'''
	fitur 4
	meng-update tanggal task
	menampilkan pesan feedback ke interface juga

	deskripsi argumen
	-- args:
	dict yang isinya bisa {id task, tanggal baru}
	id task sesuai tampilan fitur 2
	'''

def remove_task(id):
	'''
	fitur 5
	menghapus task dengan id tertentu
	menampilkan pesan feedback ke interface juga

	deskripsi argumen
	-- id:
	id task sesuai tampilan fitur 2
	'''

def show_help():
	'''
	fitur 6
	menampilkan daftar fitur & keyword
	'''

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1")
