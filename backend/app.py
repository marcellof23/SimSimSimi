from flask import Flask, request, redirect, url_for, Response
import time
import pymongo
from flask_cors import CORS
import os
import json
from dotenv import load_dotenv
from parsers import resolve_feature

load_dotenv()

app = Flask(__name__)
CORS(app)
DATABASE = os.getenv('DATABASE')
client = pymongo.MongoClient(DATABASE)

# Database
Database = client.get_database('tasks')
users = Database.user
Dict = list(Database.dictionary.find({}))
print(Dict[0]['dictionary'])
print(resolve_feature(Dict[0]['dictionary'],"Selesai Task 1"))
dictionary = [
{
		"id": 1,
			"keywords": [],
			"params": {
				"jenis_task": "regex_jenis_task",
					"kode_matkul": "regex_kode_matkul",
					"tanggal": "regex_tanggal",
					"topik": "regex_topik"
			}
	}
]


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


@app.route('/api/data', methods=['GET', 'POST'])
def HandleTasks():
	query = request.form['user_input']
	res = resolve_feature(Dict[0]['dictionary'], query)
	mydict = {}
	print(res)
	if (res['id'] == 1):
		jumlah = users.find().count()
		if jumlah == 0:
			jumlah = 1
		else:
			result = list(users.find())
			ans = sorted(result, key = lambda i: i['id'],reverse=True)
			jumlah = ans[0]['id'] + 1
		mydict['id'] = jumlah
		mydict['jenis_task'] = res['args']['jenis_task']
		mydict['kode_matkul'] = res['args']['kode_matkul']
		mydict['tanggal'] = res['args']['tanggal']
		mydict['topik'] = res['args']['topik']
		users.insert_one(mydict)
		return Response(status=201)
	elif(res['id'] == 2):
		tasks = users.find({}, {'_id': False})
		return json.dumps([task for task in tasks])
	elif(res['id'] == 3):
		tanggal_deadline = users.find_one({"jenis_task" : res['args']['jenis_task'], "kode_matkul" : res['args']['kode_matkul']})
		return json.dumps(tanggal_deadline['tanggal'])
	elif(res['id'] == 4):
		lama = users.find_one({"id" : res['args']['id_task']})
		baru = lama
		baru['tanggal'] = res['args']['tanggal']
		users.update_one(lama, baru)
	elif(res['id'] == 5):
		items = res['args']['id_task']
		myquery = {'id' : items} 
		users.delete_one(myquery)
	elif(res['id'] == 6):	
		return Response(status=201)
if(__name__ == '__main__'):
    app.run(debug=True, host='127.0.0.1')
