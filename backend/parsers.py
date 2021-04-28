import re
import json
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
import string
from datetime import datetime as dt

DATE_FORMAT = '%d/%m/%Y'

# regex_kode_matkul = "[A-Z]{2}[0-9]{4}"
# regex_tanggal = "([0-9]{2}[/-][0-9]{2}[/-][0-9]{4})|([0-9]{2}\s*(Januari|Februari|Maret|April|Mei|Juni|Juli|Agustus|September|Oktober|November|Desember)\s*[0-9]{4})"
# regex_jenis_task = "([Tt]ubes|[Tt]ucil|[Tt]ugas|[Pp]raktikum|[Uu]jian|[Kk]uis)"
# regex_topik = "^[A-Z]"

def regex_cleaning(string_kotor):
	'''
	membersihkan string_kotor dengan regex
	'''
	# Hilangkan Unicode
	string_bersih = re.sub(r'[^\x00-\x7F]+', ' ', string_kotor)
	# Hilangkan Mentions
	string_bersih = re.sub(r'@\w+', '', string_bersih)
	#Ubah jadi Lowercase
	string_bersih = string_bersih.lower()
	#Hilangkan punctuations
	string_bersih = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', string_bersih)
	#Lowercase numbers
	string_bersih = re.sub(r'[0-9]', '', string_bersih)
	#Hilangkan double space
	string_bersih = re.sub(r'\s{2,}', ' ', string_bersih)

	return string_bersih

def string_to_list(s):
	'''
	mengembalikan list of string hasil tokenize string s
	'''
	return word_tokenize(s)

def stem_words(list_of_words):
	'''
	mengembalikan hasil stemming terhadap list_of_words
	'''
	porter = PorterStemmer()
	ret = []

	for word in list_of_words: 
		ret.append(porter.stem(word))
	return ret

def remove_stop_words(list_of_words):
	'''
	menghapus stop word dari list_of_words dan mengembalikan hasilnya
	'''
	stop_words = set(stopwords.words('indonesian')) 
	ret = []

	for word in list_of_words:
		if word not in stop_words:
			ret.append(word)
	return ret

def list_to_string(list_of_words):
	'''
	mengembalikan string hasil konkatenasi list of words, dipisahkan spasi
	'''
	ret = ''
	for word in list_of_words:
		ret = ret + (word + ' ')
	if len(ret) > 0:
		ret = ret[:-1]
	return ret

def clean_string(s):
	'''
	melakukan stemming terhadap s dan menghilangkan stop word dari s
	'''
	return list_to_string(remove_stop_words(stem_words(string_to_list(regex_cleaning(s)))))

def get_lps(s):
	'''
	mengembalikan array prefix function dari string s

	deskripsi args
	-- s: string
	'''
	ret = [0]
	for i in range(1, len(s)):
		j = ret[i-1]
		while j > 0 and s[i] != s[j]:
			j = ret[j-1]
		if s[i] == s[j]:
			j += 1
		ret.append(j)
	return ret


def has_pattern(s, p):
	'''
	mengembalikan True apabila pattern p terdapat pada string s
	dilakukan menggunakan algoritme KMP
	hanya dapat mencari exact match p di s

	deskripsi args
	-- s: string
	-- p: pattern yang ingin dicari kemunculannya di s
	'''
	lps = get_lps(s)
	i = 0
	j = 0
	found = False
	while not(found) and i < len(s):
		if s[i] == p[j]:
			# karakter sama, majukan index kedua string
			i += 1
			j += 1
		if j == len(p):
			# karakter p sudah habis
			found = True
		elif i < len(s) and s[i] != p[j]:
			# karakter berbeda, pindahkan index p dengan prefix function
			if j > 0:
				j = lps[j-1]
			else:
				i += 1
	return found

def count_candidate_score(candidate, user_input):
	'''
	mengembalikan skor candidate
	skor = (banyak keyword yang cocok + banyak param yang cocok) / (banyak keyword + banyak param)
	diasumsikan penyebut > 0

	deskripsi args
	-- candidate: dict {id fitur, list of keyword fitur, list of regex param fitur}
	-- user_input: string input user
	'''
	# hitung valid keyword
	cnt_valid_keyword = 0
	cnt_keyword = len(candidate['keywords'])
	for keyword in candidate['keywords']:
		# cek ada pattern keyword apa enggak di user input pakai KMP
		if has_pattern(user_input, keyword):
			cnt_valid_keyword += 1

	# hitung valid param
	cnt_valid_param = 0
	cnt_param = len(candidate['params'])
	for param in candidate['params']:
		# cek regex param match/enggak di user input pakai library regex
		if re.search(candidate['params'][param], user_input):
			cnt_valid_param += 1

	return (cnt_valid_keyword+cnt_valid_param)/(cnt_keyword+cnt_param)

def get_date(s_date):
	'''
	mengembalikan string date dalam format dd/mm/yyyy

	deskripsi args
	-- s_date: string date berformat dd/mm/yyyy atau %d %B %Y
	'''
	date_patterns = ['%d/%m/%Y', '%d/%m/%y', '%d %B %Y', '%d %B %y', '%d-%m-%Y', '%d-%m-%y']
	for pattern in date_patterns:
		try:
			return dt.strftime(dt.strptime(s_date, pattern), DATE_FORMAT)
		except:
			pass

def get_args(params, user_input):
	'''
	mencari argumen-argumen untuk suatu fitur dari user_input
	lalu mengembalikannya dalam bentuk dict {"nama_arg": arg}

	deskripsi args
	-- params: dict berisi {"nama_arg": regex_untuk_arg}
	-- user_input: string input user
	'''
	args = {}
	for param in params:
		if param == 'topik':
			# handle topik secara khusus
			# bagian ini rawan bug kayaknya
			# harusnya yang masuk sini cuma fitur 1: add task
			topik = user_input
			# hapus substring sebelum jenis task
			match = re.search(params['jenis_task'], topik)
			if match is not None:
				topik = topik[match.start():]
			# hapus jenis task
			topik = re.sub(params['jenis_task'], '', topik)
			# hapus tanggal
			topik = re.sub(params['tanggal'], '', topik)
			# hapus kode matkul
			topik = re.sub(params['kode_matkul'], '', topik)
			# bersihin pake stemming, stop word removal, regex
			topik = clean_string(topik)
			# semoga udah jadi topik task
			args[param] = topik

		elif param == 'tanggal_awal':
			# handle tanggal awal
			# hapus tanggal_awal dari input
			args[param] = re.findall(params[param], user_input)[0]
			user_input = re.sub(params[param], '', user_input, 1)

		else:
			regex_res = re.findall(params[param], user_input)
			if len(regex_res) > 0:
				# hapus bagian string dari argumen numerik
				if param == 'n_hari' or param == 'n_minggu' or param == 'id_task':
					args[param] = int(re.findall('[0-9]+', regex_res[0])[0])
				else:
					args[param] = regex_res[0]
	# print('args sebelum normalize: ', args)

	# pastikan semua tanggal berformat dd/mm/yyyy
	if 'tanggal' in args:
		args['tanggal'] = get_date(args['tanggal'])

	if 'tanggal_awal' in args:
		args['tanggal_awal'] = get_date(args['tanggal_awal'])

	if 'tanggal_akhir' in args:
		args['tanggal_akhir'] = get_date(args['tanggal_akhir'])

	# pastikan tanggal awal sebelum tanggal akhir
	if 'tanggal_awal' in args and 'tanggal_akhir' in args:
		if dt.strptime(args['tanggal_awal'], DATE_FORMAT) > dt.strptime(args['tanggal_akhir'], DATE_FORMAT):
			args['tanggal_awal'], args['tanggal_akhir'] = args['tanggal_akhir'], args['tanggal_awal']

	# pastikan semua jenis task diawali huruf kapital
	if 'jenis_task' in args:
		args['jenis_task'] = args['jenis_task'].capitalize()

	return args

def resolve_feature(list_of_candidates, user_input):
	'''
	mengembalikan dict berisi id dan parameter-parameter fitur
	apabila tidak terdapat fitur yang cocok, mengembalikan id fitur -1

	deskripsi args
	-- list_of_candidates: list of dict {id_fitur, list_of_keyword_fitur, list_of_regex_param_fitur}
	-- user_input: string input user 
	'''
	# hitung skor tiap kandidat
	candidate_scores = []
	for i, candidate in enumerate(list_of_candidates):
		candidate_scores.append((count_candidate_score(candidate, user_input), i))

	# ambil kandidat dengan skor terbesar
	# kalau seri, ambil kandidat dengan id fitur terbesar
	candidate_scores.sort(reverse=True)
	chosen_candidate_score = candidate_scores[0][0]

	# kembalikan id -1 apabila skor kandidat < 0.5
	if chosen_candidate_score <= 0.5:
		return {'id': -1, 'score': chosen_candidate_score}

	chosen_candidate_idx = candidate_scores[0][1]
	chosen_candidate_params = list_of_candidates[chosen_candidate_idx]['params']
	chosen_candidate_feature_id = list_of_candidates[chosen_candidate_idx]['id']

	# cari argumen-argumen untuk fitur
	args = get_args(chosen_candidate_params, user_input)
	
	return {'id': chosen_candidate_feature_id, 'score': chosen_candidate_score, 'args': args}

# testing
# nltk.download('stopwords')
# fopen = open('database/dictionary.json')
# test_candidates = json.load(fopen)
# print(test_candidates)
# test_input = [
# 	'Apakah mayones sebuah instrumen?',
# 	'Tubes IF2211 String Matching pada 14 April 2021',
# 	'Tubes IF2211 String Matching pada 14 April 21',
# 	'Tubes IF2211 String Matching pada 14/04/2021',
# 	'Tubes IF2211 String Matching pada 14/04/21',
# 	'Tubes IF2211 String Matching pada 14-04-21',
# 	'tubes IF2211 String Matching',
# 	'tubes String Matching pada 14 April 2021',
# 	'ada kuis IF3110 Bab 2 sampai 3 pada 22/04/2021',
# 	'Apa saja deadline yang dimiliki sejauh ini?',
# 	'Deadline 10 minggu ke depan apa saja?',
# 	'Selesai task 1',
# 	'Apa saja deadline hari ini?',
# 	'Antara 03/04/2021 dan 15/04/2021 ada deadline apa saja ya',
# 	'Deadline tugas IF2211 itu kapan?',
# 	'Deadline task 69 diundur menjadi 28/04/2021',
# 	'Saya sudah selesai mengerjakan task 69',
# 	'Help',
# 	'help',
# 	'lihat',
# 	'Lihat',
# 	'selesai task 3'
# ]
# for test in test_input:
# 	print(test, ':\n', resolve_feature(test_candidates['dictionary'], test))