import sys
from common import *

DEBUG = True
# DEBUG = False

def get_minmax_attrs(_uid, _mask):
	global Attrs, Users

	pos_mask = set([int(x) for x in _mask if x >= 0.0 and x != -0.0])
	neg_mask = set([int(abs(x)) for x in _mask if x < 0.0 or x == -0.0])
	mask = (neg_mask | pos_mask)

	users_tmp = {}
	attrs_tmp = {}
	if _mask == []:
		users_tmp = {ix:Users[ix] for ix in range(len(Users))}
		attrs_tmp = {ix:Attrs[ix] for ix in range(len(Attrs))}
	else:
		for ix in range(len(Users)):
			if ix != _uid and pos_mask.issubset(set(Users[ix])) and len(neg_mask & set(Users[ix])) == 0:
				users_tmp[ix] = Users[ix]
				for f in users_tmp[ix]:
					if f not in attrs_tmp:
						attrs_tmp[f] = [ix]
					else:
						attrs_tmp[f].append(ix)

	min_f = None
	max_f = None
	for f in attrs_tmp.keys():
		if f not in mask:
			if f in Users[_uid]:
				if min_f == None or len(attrs_tmp[f]) < len(attrs_tmp[min_f]):
					min_f = f

			if f not in Users[_uid]:
				if max_f == None or len(attrs_tmp[f]) > len(attrs_tmp[max_f]):
					max_f = f

	min_p = 1.0
	if min_f in attrs_tmp.keys():
		min_p = float(len(attrs_tmp[min_f])) / float(len(users_tmp))
	max_p = 1.0
	if max_f in attrs_tmp.keys():
		max_p = 1.0 - float(len(attrs_tmp[max_f])) / float(len(users_tmp))

	return min_f, min_p, max_f, max_p

def cut_it(_uid, _mask):
	(min_f, min_p, max_f, max_p) = get_minmax_attrs(_uid, _mask)

	if min_f == None or max_f == None:
		return _mask

	if min_p <= max_p:
		if min_f == 0:
			_mask.append(0.01)
		else:
			_mask.append(min_f)
		return cut_it(_uid, _mask)
	else:
		if max_f == 0:
			_mask.append(-0.01)
		else:
			_mask.append(-1*max_f)
		return cut_it(_uid, _mask)

config, outpath = load_config("config_999_faster.json")

global Attrs
Attrs = load_attr_csv(config["user_limit"], first_col = config["first_col"], data_prefix = config["data_pref"])
global Users
Users = load_user_csv(config["user_limit"], first_col = config["first_col"], data_prefix = config["data_pref"])

num_users = len(Users)
print "#users:", num_users

# Calculating individual fingerprints
long_ctr = 0
fi = open(outpath, "w+")
for uid in range(num_users):
	print "$", uid
	mask = []
	mask = cut_it(uid, mask)
	if len(mask) > config["limit"]:
		long_ctr += 1

	if DEBUG:
		print "\t==> Fingerprint (FP):", mask
		print "\t    Identified by FP:", list(test_fingerprint(uid, mask, Users, Attrs))

	fi.write(";".join([str(x) for x in mask])+"\n")

fi.close()

print "Cases when fingerprint was too long:", long_ctr
