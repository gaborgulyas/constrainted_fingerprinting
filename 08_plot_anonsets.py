
import cPickle as pickle
import sys
import gzip
import os
from collections import Counter
from common import *

# Get kmap it from:
#   https://github.com/gaborgulyas/kmap -- get "kmap.py"
# Which will also need:
#   https://github.com/gaborgulyas/SelectPoints -- get "selectpoints.py"
from kmap import plot_kmap

config, outpath = load_config("config_group.json")

K = config["max_sig_size"]
OUTPUT_DATA_DIR = config["output_path"]

for s in range(2, K+1):
	[signature, e_classes] = pickle.load(gzip.open(OUTPUT_DATA_DIR + "equivalence_classes_%d.p.gz" % s, 'r'))

	data = []
	for ec in e_classes:
		data.append(len(ec))

	plot_kmap(
		[sum(data), Counter(data)], data_raw=False, as_partitions=True,
		title="Fonts", filename=OUTPUT_DATA_DIR + "equivalence_classes_%d.png" %s,
		plot_annotation=[[1, 3], [10, 50000]], annotation_params=dict(radius=[.2, .1], distance=[.33, .65], linestyle=dict(color='r', width=1, style='--'), location=['right', 'top']),
		plot_heatmap=False,
		titlelabelsize=30, axlabelsize=30, textsize=28, annotationsize=26, plot_legend=False
	)
