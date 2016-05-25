import pickle
import os
import urllib2
import math

# Build environment
if not os.path.exists("data"):
	os.mkdir("data")
if not os.path.exists("results"):
	os.mkdir("results")

# Obtaining data
if not os.path.exists("adult.data"):
	print "obtaining dataset...",
	response = urllib2.urlopen('http://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data')
	f = open("data/adult.data", "w+")
	f.write(response.read())
	f.close()
	print "done!"

if not os.path.exists("data/adult.p") or not os.path.exists("data/attrib_dict.p"):
	# Dataset init
	attrib_dict = {}
	for ix in range(15):
		attrib_dict[ix] = [None]
	records = []

	# Conversion #1
	print "converting data to int attributes...",
	for l in open("data/adult.data", "r").readlines():
		r_ = l.replace('\r', '').replace('\n', '').replace(', ', ',').split(',')

		if len(r_) < 15:
			continue

		r = []
		for ix, a in enumerate(r_):
			try:
				a_ix = attrib_dict[ix].index(a)
			except ValueError:
				a_ix = len(attrib_dict[ix])
				attrib_dict[ix].append(a)
			r.append(a_ix)
		records.append(r)
	print "done!"
	print "num records:", len(records)

	print "writing cache...",
	pickle.dump(records, open("data/adult.p", "w+"))
	pickle.dump(attrib_dict, open("data/attrib_dict.p", "w+"))
	print "done!"
elif not os.path.exists("data/adult_bin.p"):
	print "loading cache...",
	attrib_dict = pickle.load(open("data/attrib_dict.p", "r"))
	records = pickle.load(open("data/adult.p", "r"))
	print "done!"

# Conversion #2
if not os.path.exists("data/adult_bin.p"):
	maxes = [str(int(math.ceil(math.log(len(attrib_dict[ix]), 2)))) for ix in range(len(attrib_dict.keys()))]
	records2 = []
	for ix, r in enumerate(records):
		r2s = ""
		for ix, v in enumerate(r):
			r2s += ('{0:0'+maxes[ix]+'b}').format(v)

		r2 = [int(_) for _ in r2s]
		records2.append(r2)

	print "writing cache...",
	pickle.dump(records2, open("data/adult_bin.p", "w+"))
	print "done!"
else:
	print "loading cache...",
	records2 = pickle.load(open("data/adult_bin.p", "r"))
	print "done!"

# Write CSV format for individual fingerprinting
attrs = {ix:[] for ix in range(80)}
f = open("data/users.csv", "w+")
for ix, r in enumerate(records2):
	# if ix == 1000: # limit it if you want a smaller dataset for quick experimentation
	# 	break

	line = ""
	for ix2, v in enumerate(r):
		if v == 1:
			line += str(ix2)+";"
			attrs[ix2].append(ix)
	f.write(line+"\n")
f.close()

f = open("data/attrs.csv", "w+")
for a in sorted(attrs.keys()):
	# print attrs[a]
	line = ""
	for v in attrs[a]:
		line += str(v)+";"
	f.write(line+"\n")
f.close()
