from flask import Flask, request, redirect, url_for, Response
import time
import pymongo
from flask_cors import CORS
import os
import json
from dotenv import load_dotenv
from parsers import resolve_feature, DATE_FORMAT
from datetime import datetime as dt
from datetime import timedelta
import re

load_dotenv()

app = Flask(__name__)
CORS(app)
DATABASE = os.getenv('DATABASE')
client = pymongo.MongoClient(DATABASE)

# Database
Database = client.get_database('tasks')
users = Database.user
Dict = list(Database.dictionary.find({}))
# print(Dict[0]['dictionary'])
# print(resolve_feature(Dict[0]['dictionary'],"Selesai Task 1"))
# dictionary = [
# {
# 		"id": 1,
# 			"keywords": [],
# 			"params": {
# 				"jenis_task": "regex_jenis_task",
# 					"kode_matkul": "regex_kode_matkul",
# 					"tanggal": "regex_tanggal",
# 					"topik": "regex_topik"
# 			}
# 	}
# ]

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
	args = res['args']
	mydict = {}
	print('masuk fitur', res['id'])
	if(res['id'] == -1):
		return json.dumps({'err': 'naon'})
	if (res['id'] == 1):
		# cek komponen task lengkap apa enggak
		if 'jenis_task' not in args.keys():
			return json.dumps({'err': 'Kasih keterangan dong ini tubes, tucil, kuis, ujian, atau praktikum'})
		if 'kode_matkul' not in args:
			return json.dumps({'err': 'Tambahin kode matkul dong'})
		if 'tanggal' not in args:
			return json.dumps({'err': 'Tambahin tanggal deadline atau tanggal diadakannya dong'})
		if 'topik' not in args:
			return json.dumps({'err': 'Tambahin topik dong'})
		# tambah task ke database
		jumlah = users.find().count()
		if jumlah == 0:
			jumlah = 1
		else:
			result = list(users.find())
			ans = sorted(result, key = lambda i: i['id'],reverse=True)
			jumlah = ans[0]['id'] + 1
		mydict['id'] = jumlah
		mydict['jenis_task'] = args['jenis_task']
		mydict['kode_matkul'] = args['kode_matkul']
		mydict['tanggal'] = dt.strptime(args['tanggal'], DATE_FORMAT)
		mydict['topik'] = args['topik']
		users.insert_one(mydict)
		return Response(status=201)
	elif(res['id'] == 2):
		# bagi kasus tergantung args
		if len(args) == 0:
			# tanpa parameter
			tasks = users.find({}, {'_id': False})
			return json.dumps([task for task in tasks], default=str)
		if 'tanggal_awal' in args:
			# pake tanggal
			# cek dulu tanggalnya lengkap apa enggak
			if args['tanggal_awal'] is None:
				return json.dumps({'err': 'Kayaknya format tanggal kamu salah, coba pake dd/mm/yyyy'})
			if ('tanggal_akhir' not in args) or (args['tanggal_akhir'] is None):
				return json.dumps({'err': 'Kamu cuma masukin satu tanggal, coba masukin satu lagi'})
			tanggal_awal = dt.strptime(args['tanggal_awal'], DATE_FORMAT)
			tanggal_akhir = dt.strptime(args['tanggal_akhir'], DATE_FORMAT)
			tasks = users.find({'tanggal': {'$gte': tanggal_awal, '$lte': tanggal_akhir}}, {'_id': False})
			return json.dumps([task for task in tasks], default=str)
		if 'n_minggu' in args:
			# pake minggu
			tanggal_awal = dt.now().replace(hour=0, minute=0, second=0, microsecond=0)
			time_change = timedelta(weeks=args['n_minggu'])
			tanggal_akhir = tanggal_awal + time_change
			tasks = users.find({'tanggal': {'$gte': tanggal_awal, '$lte': tanggal_akhir}}, {'_id': False})
			return json.dumps([task for task in tasks], default=str)
		if 'n_hari' in args:
			# pake hari
			tanggal_awal = dt.now().replace(hour=0, minute=0, second=0, microsecond=0)
			time_change = timedelta(days=args['n_hari'])
			tanggal_akhir = tanggal_awal + time_change
			print('tanggal:',tanggal_awal,tanggal_akhir)
			tasks = users.find({'tanggal': {'$gte': tanggal_awal, '$lte': tanggal_akhir}}, {'_id': False})
			return json.dumps([task for task in tasks], default=str)

	elif(res['id'] == 3):
		if 'jenis_task' in args and 'kode_matkul' in args:
			tasks = users.find({"jenis_task" : args['jenis_task'], "kode_matkul" : args['kode_matkul']}, {'_id': False})
			return json.dumps([task for task in tasks], default=str)
		elif 'jenis_task' in args:
			tasks = users.find({"jenis_task" : args['jenis_task']}, {'_id': False})
			return json.dumps([task for task in tasks], default=str)
		elif 'kode_matkul' in args:
			print('masuk sini')
			tasks = users.find({"kode_matkul" : args['kode_matkul']}, {'_id': False})
			return json.dumps([task for task in tasks], default=str)

	elif(res['id'] == 4):
		if(res['args']['tanggal'] is None):
			return "TANGGAL NULL"
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
	return Response(status=201)
if(__name__ == '__main__'):
    app.run(debug=True, host='127.0.0.1')
