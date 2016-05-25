import pickle
import sys
import math
from common import *

config, outpath = load_config("config_999.json")

global Attrs
Attrs = load_attr_csv(config["user_limit"], first_col = config["first_col"], data_prefix = config["data_pref"])
global Users
Users = load_user_csv(config["user_limit"], first_col = config["first_col"], data_prefix = config["data_pref"])

anonsetsizes = []
ctr = 0
for uid, l in enumerate(open(outpath, "r").readlines()):
	r = [float(x) for x in l.replace('\r', '').replace('\n', '').split(';')]

	if ctr >= 0:
		s = test_fingerprint(uid, r, Users, Attrs)
		if len(s) == 0:
			print uid
			print s

		anonsetsizes.append(len(s))

	ctr += 1
pickle.dump(anonsetsizes, open(outpath.replace(".csv", ".p"), "w+"))

for anonsetsize in [0, 1, 2, 3]:
	print "[|anon_set_size| == "+str(anonsetsize)+"]:", sum(i == anonsetsize for i in anonsetsizes)
