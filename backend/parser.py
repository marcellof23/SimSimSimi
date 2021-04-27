import re

regex_kode_matkul = "[A-Z]{2}[0-9]{4}"
regex_tanggal = "([0-9]{2}[/-][0-9]{2}[/-][0-9]{4})|([0-9]{2}\s*(Januari|Februari|Maret|April|Mei|Juni|Juli|Agustus|September|Oktober|November|Desember)\s*[0-9{4}])"
regex_jenis_task = "([Tt]ubes|[Tt]ucil|[Tt]ugas|[Pp]raktikum|[Uu]jian|[Kk]uis)"
regex_topik = "^[A-Z]"


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
			i += 1
			j += 1
		if j == len(p):
			found = True
		elif i < len(s) and s[i] != p[j]:
			if j > 0:
				j = lps[j-1]
			else:
				i += 1
	return found

test_candidates = [
	{
		"id": 1,
		"keywords": [],
		"params": {
			"jenis_task": regex_jenis_task,
			"kode_matkul": regex_kode_matkul,
			"tanggal": regex_tanggal,
			"topik": regex_topik
		}
	}
]

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
	chosen_candidate_feature_id = list_of_candidates[chosen_candidate_params]["id"]

	# cari argumen-argumen untuk fitur
	args = []
	for param in chosen_candidate_params:
		args.append(re.findall(chosen_candidate_params[param], user_input)[0])

	return {"id": chosen_candidate_feature_id, "args": args}
