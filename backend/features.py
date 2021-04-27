# from app import users,app
# import json

# @app.route("/views", methods=["GET"])
# def user_profile():
#     todos = users.find({}, {'_id': False})
#     return json.dumps([todo for todo in todos])

# def add_task(args):

# 	'''
# 	fitur 1
# 	menambahkan task ke database
# 	menampilkan pesan feedback ke interface juga
# 	ngehandle argumen kurang juga, kayak kurang tanggal (?)

# 	deskripsi argumen
# 	-- args: 
# 	dict yang isinya bisa {tanggal, nama matkul, jenis task, topik}
	
# 	'''

# def show_tasks(args):
# 	'''
# 	fitur 2
# 	menampilkan daftar task ke interface
	
# 	deskripsi argumen
# 	-- args: 
# 	dict yang isinya bisa {date_awal, date_akhir, n_minggu, n_hari}
# 	kalo n_hari = 0, berarti hari ini
# 	'''

# def show_deadline(args):
# 	'''
# 	fitur 3
# 	menampilkan deadline task

# 	deskripsi argumen
# 	-- args:
# 	dict yang isinya bisa {nama matkul, jenis task}
# 	'''

# def update_task_deadline(args):
# 	'''
# 	fitur 4
# 	meng-update tanggal task
# 	menampilkan pesan feedback ke interface juga

# 	deskripsi argumen
# 	-- args:
# 	dict yang isinya bisa {id task, tanggal baru}
# 	id task sesuai tampilan fitur 2
# 	'''

# def remove_task(id):
# 	'''
# 	fitur 5
# 	menghapus task dengan id tertentu
# 	menampilkan pesan feedback ke interface juga

# 	deskripsi argumen
# 	-- id:
# 	id task sesuai tampilan fitur 2
# 	'''

# def show_help():
# 	'''
# 	fitur 6
# 	menampilkan daftar fitur & keyword
# 	'''