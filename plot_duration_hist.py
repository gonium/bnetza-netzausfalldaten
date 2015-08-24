# vim:fileencoding=utf-8
# -*- coding: utf8 -*-
import matplotlib.pyplot as plt
#import matplotlib.mlab as mlab
import numpy as np
import pandas as pd
import argparse

cmd_parser = argparse.ArgumentParser()
cmd_parser.add_argument("datafile", help="pickle/*.pkl file with staged data")
args = cmd_parser.parse_args()

print "Slurping data from %s" % (args.datafile)
alldata = pd.read_pickle(args.datafile)
print alldata.dtypes
first_outtake=np.min(alldata['Beginn'])
last_outtake=np.max(alldata['Beginn'])

print "Erster Ausfall: %s, letzter Ausfall: %s" % (first_outtake,
    last_outtake)

ungeplant = alldata[alldata['Art']==u"ungeplant"]
ungeplant_hoes = ungeplant[ungeplant['Netzebene'] == u"HöS"]
ungeplant_hs = ungeplant[ungeplant['Netzebene'] == u"HS"]
ungeplant_ms = ungeplant[ungeplant['Netzebene'] == u"MS"]
ungeplant_ns = ungeplant[ungeplant['Netzebene'] == u"NS"]


filtered = ungeplant[ungeplant['Dauer'] < 2000]
hist, bins = np.histogram(filtered['Dauer'], bins=1000)
f_median = np.median(filtered['Dauer'])
median_label = "Median der Ausfalldauer: %.1f Minuten" % f_median
print median_label
print "Drawing"
fig = plt.figure(figsize=(16, 9), dpi=75)
ax = fig.add_subplot(111)
plt.title(u"Histogramm der Ausfalldauer")
width = 0.7 * (bins[1] - bins[0])
center = (bins[:-1] + bins[1:]) / 2
plt.bar(center, hist, align='center', width=width, facecolor='green',
    edgecolor='green', alpha=0.7)
plt.plot([f_median, f_median], [0, np.max(hist)], color='r', linestyle='-',
    linewidth=2)
plt.text(f_median + 15, np.max(hist), median_label)
plt.xlim((-10, 1500))
ax = fig.gca()
ax.set_xticks(np.arange(0,np.max(center), 60))
locs, labels = plt.xticks()
plt.setp(labels, rotation=30)
plt.xlabel("Ausfalldauer [Minuten]")
plt.ylabel(u"Häufigkeit")
plt.grid()
plt.tight_layout()
plt.savefig("images/hist_downtime_duration.png", bbox_inches='tight')
