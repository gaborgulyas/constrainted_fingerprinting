import sys
from common import *


DEBUG = True
# DEBUG = False

def greedy_individual_fingerprint(uid):
	global Attrs, Users
	user_set = set(Users.keys())
	users = {}
	for a in Attrs.keys():
		if len(Attrs[a]) == 0:
			continue

		if a in Users[uid]:
			users[a] = Attrs[a]
		else:
			users[a] = user_set - Attrs[a]

	mask = []
	anon_set = set(Users.keys())
	while len(anon_set) > 1:
		avail_attrs = set(users.keys()) - set(mask)

		min_a = None
		for a in avail_attrs:
			if min_a == None:
				min_a = a
				continue

			if len(users[a] & anon_set) < len(users[min_a] & anon_set):
				min_a = a

		if len(users[min_a] & anon_set) == len(anon_set):
			break

		if min_a in Users[uid]:
			mask.append(min_a)
		else:
			if min_a == 0:
				mask.append(-0.01) # otherwise sign of 0 could not be distinguished (remained due to "historical" reasons :) )
			else:
				mask.append(-min_a)
		anon_set = anon_set & users[min_a]

	return mask

config, outpath = load_config("config_999.json")

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
	print "$", uid,
	mask = []
	mask = greedy_individual_fingerprint(uid)
	if len(mask) > config["limit"]:
		long_ctr += 1

	if DEBUG:
		print "\t==> Fingerprint (FP):", mask
		print "\t    Identified by FP:", list(test_fingerprint(uid, mask, Users, Attrs))

	fi.write(";".join([str(x) for x in mask])+"\n")
fi.close()

print "Cases when fingerprint was too long:", long_ctr
