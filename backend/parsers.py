import re
import json
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
from datetime import datetime as dt

DATE_FORMAT = '%d/%m/%Y'

regex_kode_matkul = "[A-Z]{2}[0-9]{4}"
regex_tanggal = "([0-9]{2}[/-][0-9]{2}[/-][0-9]{4})|([0-9]{2}\s*(Januari|Februari|Maret|April|Mei|Juni|Juli|Agustus|September|Oktober|November|Desember)\s*[0-9{4}])"
regex_jenis_task = "([Tt]ubes|[Tt]ucil|[Tt]ugas|[Pp]raktikum|[Uu]jian|[Kk]uis)"
regex_topik = "^[A-Z]"

fopen = open('database/dictionary.json')
test_candidates = json.load(fopen)

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
		ret.append(word + ' ')
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
	cnt_keyword = len(candidate["keywords"])
	for keyword in candidate["keywords"]:
		# cek ada pattern keyword apa enggak di user input pakai KMP
		if has_pattern(user_input, keyword):
			cnt_valid_keyword += 1

	# hitung valid param
	cnt_valid_param = 0
	cnt_param = len(candidate["params"])
	for param in candidate["params"]:
		# cek regex param match/enggak di user input pakai library regex
		if re.search(candidate["params"][param], user_input):
			cnt_valid_param += 1

	return (cnt_valid_keyword+cnt_valid_param)/(cnt_keyword+cnt_param)


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
	chosen_candidate_idx = candidate_scores[0][1]
	chosen_candidate_params = list_of_candidates[chosen_candidate_idx]["params"]
	chosen_candidate_feature_id = list_of_candidates[chosen_candidate_idx]["id"]

	# cari argumen-argumen untuk fitur
	args = {}
	for param in chosen_candidate_params:
		if param == "topik":
			# handle topik secara khusus
			# bagian ini rawan bug kayaknya
			# harusnya yang masuk sini cuma fitur 1: add task
			topik = user_input
			# hapus substring sebelum jenis task
			match = re.search(chosen_candidate_params["jenis_task"], topik)
			if match is not None:
				topik = topik[match.start():]
			# hapus jenis task
			topik = re.sub(chosen_candidate_params["jenis_task"], '', topik)
			# hapus tanggal
			topik = re.sub(chosen_candidate_params["tanggal"], '', topik)
			# hapus kode matkul
			topik = re.sub(chosen_candidate_params["kode_matkul"], '', topik)
			# bersihin pake stemming, stop word removal, regex
			topik = clean_string(topik)
			# semoga udah jadi topik task
			args[param] = topik

		elif param == "tanggal_awal":
			# handle tanggal awal
			# hapus tanggal_awal dari input
			args[param] = re.findall(chosen_candidate_params[param], user_input)[0]
			user_input = re.sub(chosen_candidate_params[param], '', user_input, 1)

		else:
			regex_res = re.findall(chosen_candidate_params[param], user_input)
			if len(regex_res) > 0:
				if param == 'n_hari' or param == 'n_minggu' or param == 'id_task':
					args[param] = int(re.findall('[0-9]*', regex_res[0])[0])
				else:
					args[param] = regex_res[0]

	if "tanggal_awal" in args and "tanggal_akhir" in args:
		if dt.strptime(args["tanggal_awal"]) > dt.strptime(args["tanggal_akhir"]):
			swap(args["tanggal_awal"], args["tanggal_awal"])
	return {"id": chosen_candidate_feature_id, "args": args}
