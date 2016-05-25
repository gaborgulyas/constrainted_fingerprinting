import matplotlib
import matplotlib.pyplot as plt
from common import *

config, outpath = load_config("config_999.json")

# Process data
fplen = {x: 0 for x in range(100)}
for l in open(outpath, "r").readlines():
	r = [int(float(x)) for x in l.replace('\r', '').replace('\n', '').split(';')]
	ln = len(r)
	if ln not in fplen.keys():
		fplen[ln] = 0
	fplen[ln] += 1

matplotlib.rcParams.update({'font.size': 22})

# Plot data
fig, ax = plt.subplots()
xs = sorted(fplen.keys())
ys = [fplen[x] for x in xs]
ax.plot(xs, ys, "k-")

YMAX = max(ys) * 1.2

# Average fingerprint length
avg = 0.0
for x in sorted(fplen.keys()):
	avg += fplen[x]*x
avg = avg / sum(fplen.values())

ax.plot([avg, avg], [0, YMAX], "k--", label= None)
ax.annotate("%.1f" % avg + " attrs on average",
    xy=(avg+.2, 0.4*YMAX), xycoords='data',
    xytext=(avg+1, 0.6*YMAX), textcoords='data',
    size=13, va="center", ha="left",
    arrowprops=dict(color="k", arrowstyle="->"),
    color="k"
)

# Fingerprint limit
ax.plot([config["limit"], config["limit"]], [0, YMAX], "k--", label= None)
ax.annotate("Limit ("+str(config["limit"])+")",
	xy=(config["limit"]+.2, 0.5*YMAX), xycoords='data',
	xytext=(config["limit"]+2, 0.7*YMAX), textcoords='data',
	size=13, va="center", ha="left",
	arrowprops=dict(color="k", arrowstyle="->"),
	color="k"
)

ax.set_xticks(range(0, 21, 2))

# Ratio of users under and above the fingerprint limit
num_ok = 0
num_lng = 0
for x in xs:
	if x <= config["limit"]:
		num_ok += fplen[x]
	else:
		num_lng += fplen[x]

num_ok = 100*float(num_ok) / sum(fplen.values())
num_lng = 100*float(num_lng) / sum(fplen.values())

ax.fill_between(range(config["limit"]+1), [0]*(config["limit"]+1), ys[0:(config["limit"]+1)], facecolor='blue', alpha=0.5)
plt.text(5, 600, "%.1f%%" % num_ok, fontdict=dict(size=13, color="white", weight='bold'), rotation=-45)
ax.fill_between(range(config["limit"], config["limit"]+len(ys[10:])), [0]*len(ys[10:]), ys[10:], facecolor='red', alpha=0.5)
plt.text(config["limit"]+.2, 550, "%.1f%%" % num_lng, fontdict=dict(size=13, color="white", weight='bold'), rotation=-45)

ax.set_xlabel("Length of Fingerprints")
ax.set_ylabel("Number of Users")
plt.tick_params(axis='both', which='major', labelsize=14)
plt.ylim(0, YMAX)
plt.xlim(0, 2*config["limit"])

plt.tight_layout()
plt.savefig(outpath.replace('.csv', '.png'))
