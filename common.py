import json

def load_attr_csv(user_limit = 99999, first_col = 0, data_prefix = ""):
	data_path = "data/attrs.csv"
	if data_prefix != "":
		data_path = data_path.replace(".", "_"+data_prefix+".")

	data = {}
	f = open(data_path, "r")
	for ix, line in enumerate(f.readlines()):
		r = [int(x) for x in line.replace('\n', '').split(";") if x != ""][first_col:]
		data[ix] = set([x for x in r if (int(x) <= user_limit or user_limit == -1)])
	f.close()

	return data

def load_user_csv(user_limit = 99999, first_col = 0, data_prefix = ""):
	data_path = "data/users.csv"
	if data_prefix != "":
		data_path = data_path.replace(".", "_"+data_prefix+".")

	data = {}
	f = open(data_path, "r")
	for ix, line in enumerate(f.readlines()):
		data[ix] = list(set([int(x) for x in line.replace('\n', '').split(";") if x != ""][first_col:]))
		if ix >= user_limit and user_limit != -1:
			break
	f.close()
	return data

def save_csv(path, data):
	f = open(path, "w+")
	for k in sorted(data.keys()):
		f.write(str(sorted(list(data[k]))) + "\n")
	f.close()

def test_fingerprint(uid, mask, users, attrs):
	r_user_set = set(users.keys())
	for ix, a in enumerate(mask):
		if a >= 0:
			a_ = int(a)
			r_user_set = r_user_set & attrs[a_]
		else:
			a_ = int(a)
			r_user_set = r_user_set & (set(users.keys()) - attrs[-a_])

	return r_user_set

def get_individual_fingerprint_file_path(type, user_limit, data_pref):
	if type == "paper":
		fingerprint_file = "results/individual_fingerprints.csv"
		if user_limit > -1:
			fingerprint_file = "results/individual_fingerprints_"+str(user_limit)+".csv"
	else:
		fingerprint_file = "results/individual_fingerprints_faster.csv"
		if user_limit > -1:
			fingerprint_file = "results/individual_fingerprints_faster_"+str(user_limit)+".csv"
	if data_pref != "":
		fingerprint_file = fingerprint_file.replace("/", "/"+data_pref+"_")

	return fingerprint_file

def load_config(filepath = "config.json"):
	config = json.load(open("./configs/" + filepath, 'r'))
	return config, get_individual_fingerprint_file_path(config["type"], config["user_limit"], config["data_pref"])