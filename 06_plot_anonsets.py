import pickle
import sys
from collections import Counter

# Get kmap it from:
#   https://github.com/gaborgulyas/kmap -- get "kmap.py"
# Which will also need:
#   https://github.com/gaborgulyas/SelectPoints -- get "selectpoints.py"
from kmap import plot_kmap

from common import *

config, outpath = load_config("config_999.json")

anonsetsizes = pickle.load(open(outpath.replace(".csv", ".p"), "r"))

ixs = []
for ix in range(len(anonsetsizes)):
	if anonsetsizes[ix] == 0:
		ixs.append(ix)
for ctr, ix in enumerate(ixs):
	del anonsetsizes[ix-ctr]

xy = Counter(anonsetsizes)

plot_kmap([len(anonsetsizes), xy], data_raw=False, title="Anonymity set sizes", filename=outpath.replace(".csv", "_anon_set_sizes.png"), plot_heatmap=False, plot_annotation=[[1, 3], [10, 50000]], annotation_params=dict(radius=[.2, .1], distance=[.33, .75], linestyle=dict(color='r', width=1, style='--'), location=['right', 'top']), titlelabelsize=30, axlabelsize=30, textsize=28, annotationsize=26, plot_legend=False)
