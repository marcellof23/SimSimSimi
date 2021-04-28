from flask import Flask, request, redirect, url_for, Response
import time
import pymongo
from flask_cors import CORS
import os
import json
from dotenv import load_dotenv
from parsers import resolve_feature, DATE_FORMAT,editDist
from datetime import datetime as dt
from datetime import timedelta
import requests
import re
import nltk

load_dotenv()

app = Flask(__name__)
#yang bawah buat build
# app = Flask(__name__, static_folder='./build', static_url_path='/')
CORS(app)
DATABASE = os.getenv('DATABASE')	
client = pymongo.MongoClient("mongodb+srv://dbUsers:bodoamatwoi@cluster0.wuqpo.mongodb.net/test")

# Database
Database = client.get_database('tasks')
users = Database.user
Dict = list(Database.dictionary.find({}))
nltk.download('punkt')
nltk.download('stopwords')
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


# @app.route("/", methods=["GET"])
# def what_ismy_basedir():
# 	return basedir
#yang bawah buat build
@app.route('/')
def index():
    return app.send_static_file('index.html')


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
	query = request.json
	print(query)
	res = resolve_feature(Dict[0]['dictionary'], query)
	if('args' in res):
		args = res['args']
	mydict = {}
	print('masuk fitur', res['id'])
	importantWords = set()
	
	if(res['id'] == -1):
		el = ""
		init = -1
		for diction in Dict[0]['dictionary']:
			for i in range(len(diction['keywords'])):	
				importantWords.add(diction['keywords'][i])
		for word in importantWords:
			print(word)
		q = query.split()
		for e in importantWords:
			for j in range(len(q)):
				scoreQ = 1 - (editDist(q[j].lower(),e.lower()))/(len(e))
				formatted_float = "{:.2f}".format(scoreQ)
				print(q[j] + " " +formatted_float)
				if(init < scoreQ):
					el = e
					init = scoreQ
		formatted_float = "{:.2f}".format(init)
		print(el + " " + formatted_float)
		if(init < 0.5):
			return json.dumps({'id':-1, 'message': 'naon'})
		else:
			return json.dumps({'id':-1, 'message': 'Mungkin maksud anda adalah ' + el})
	if (res['id'] == 1):
		# cek komponen task lengkap apa enggak
		if 'jenis_task' not in args.keys():
			return json.dumps({'id': 1, 'message': 'Kasih keterangan dong ini tubes, tucil, kuis, ujian, atau praktikum'})
		if 'kode_matkul' not in args:
			return json.dumps({'id': 1, 'message': 'Tambahin kode matkul dong'})
		if 'tanggal' not in args:
			return json.dumps({'id': 1, 'message': 'Tambahin tanggal deadline atau tanggal diadakannya dong'})
		if 'topik' not in args:
			return json.dumps({'id': 1, 'message': 'Tambahin topik dong'})
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
		# return Response(status=201)
		message = 'Task berhasil dicatat!\n' + str(mydict['id']) + '. '+ dt.strftime(mydict['tanggal'], DATE_FORMAT) + ' - ' + mydict['kode_matkul'] + ' - ' + mydict['jenis_task'] + ' - ' + mydict['topik']
		print(message)
		return json.dumps({'id': 1, 'message': message})

	elif(res['id'] == 2):
		# bagi kasus tergantung args
		if len(args) == 0:
			# tanpa parameter
			tasks = users.find({}, {'_id': False})
			return json.dumps({'id': 2, 'item': [task for task in tasks],'message': 'naon'}, default=str)
		if 'tanggal_awal' in args:
			# pake tanggal
			# cek dulu tanggalnya lengkap apa enggak
			if args['tanggal_awal'] is None:
				return json.dumps({'id': 2, 'message': 'Kayaknya format tanggal kamu salah, coba pake dd/mm/yyyy'})
			if ('tanggal_akhir' not in args) or (args['tanggal_akhir'] is None):
				return json.dumps({'id': 2, 'message': 'Kamu cuma masukin satu tanggal, coba masukin satu lagi'})
			tanggal_awal = dt.strptime(args['tanggal_awal'], DATE_FORMAT)
			tanggal_akhir = dt.strptime(args['tanggal_akhir'], DATE_FORMAT)
			tasks = users.find({'tanggal': {'$gte': tanggal_awal, '$lte': tanggal_akhir}}, {'_id': False})
			return json.dumps({'id': 2, 'item': [task for task in tasks],'message': 'naon'}, default=str)
		if 'n_minggu' in args:
			# pake minggu
			tanggal_awal = dt.now().replace(hour=0, minute=0, second=0, microsecond=0)
			time_change = timedelta(weeks=args['n_minggu'])
			tanggal_akhir = tanggal_awal + time_change
			tasks = users.find({'tanggal': {'$gte': tanggal_awal, '$lte': tanggal_akhir}}, {'_id': False})
			return json.dumps({'id': 2, 'item': [task for task in tasks],'message': 'naon'}, default=str)
		if 'n_hari' in args:
			# pake hari
			tanggal_awal = dt.now().replace(hour=0, minute=0, second=0, microsecond=0)
			time_change = timedelta(days=args['n_hari'])
			tanggal_akhir = tanggal_awal + time_change
			print('tanggal:',tanggal_awal,tanggal_akhir)
			tasks = users.find({'tanggal': {'$gte': tanggal_awal, '$lte': tanggal_akhir}}, {'_id': False})
			return json.dumps({'id': 2, 'item': [task for task in tasks],'message': 'naon'}, default=str)

	elif(res['id'] == 3):
		if 'jenis_task' in args and 'kode_matkul' in args:
			tasks = users.find({"jenis_task" : args['jenis_task'], "kode_matkul" : args['kode_matkul']}, {'_id': False})
			return json.dumps({'id': 3, 'item': [task for task in tasks]}, default=str)
		elif 'jenis_task' in args:
			tasks = users.find({"jenis_task" : args['jenis_task']}, {'_id': False})
			return json.dumps({'id': 3, 'item': [task for task in tasks]}, default=str)
		elif 'kode_matkul' in args:
			tasks = users.find({"kode_matkul" : args['kode_matkul']}, {'_id': False})
			return json.dumps({'id': 3, 'item': [task for task in tasks]}, default=str)

	elif(res['id'] == 4):
		if(args['tanggal'] is None):
			return json.dumps({'id': 4, 'message': 'Kasih tanggal barunya dong'})
		lama = users.find_one({"id" : args['id_task']})
		baru = lama
		baru['tanggal'] = args['tanggal']
		users.update_one(lama, baru)
		message = 'Tanggal task ' + str(args['id_task']) + ' berhasil diubah!'
		return json.dumps({'id': 4, 'message': message}) # pesan berhasil

	elif(res['id'] == 5):
		items = args['id_task']
		myquery = {'id' : items} 
		ret = users.delete_one(myquery)
		if ret['deletedCount'] > 0:
			# berhasil
			message = 'Task ' + str(args['id_task']) + ' berhasil dihapus!'
			return json.dumps({'id': 5, 'message': message})
		else:
			message = 'Task nomor' + str(args['id_task']) + ' tidak ada'
			return json.dumps({'id': 5, 'message': message})

	elif(res['id'] == 6):
		help_message = 	(	'[Fitur]\n'
							'1. Menambahkan task baru\n'
							'2. Melihat daftar task\n'
							'3. Menampilkan deadline suatu matkul/tugas\n'
							'4. Memperbaharui tanggal task\n'
							'5. Menandai bahwa suatu task sudah selesai\n'
							'6. Menampilkan opsi help\n'
							'\n'
							'[Kata Penting: Jenis-Jenis Task]\n'
							'1. Tubes\n'
							'2. Tucil\n'
							'3. Tugas\n'
							'4. Kuis\n'
							'5. Ujian\n'
							'6. Praktikum\n' )
		# return Response(status=201)
		return json.dumps({'id': 6, 'message': help_message})

	return Response(status=201)
@app.route('/api', methods=['POST'])
def coba():
	req = request.json
	print(req)
	return { "adsf" : "1"}

@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')

#buat deploy ambil yang atas
if(__name__ == '__main__'):
	# app.run(host='0.0.0.0', debug=False, port=os.environ.get('PORT', 80))
    app.run(debug=True, host='127.0.0.1')
