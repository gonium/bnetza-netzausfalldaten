# vim:fileencoding=utf-8
# -*- coding: utf8 -*-
import matplotlib.pyplot as plt
import pylab as P
#import matplotlib.mlab as mlab
import numpy as np
import pandas as pd
import datetime as dt
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
print "Drawing"
fig = plt.figure(figsize=(16, 9), dpi=75)
ax = fig.add_subplot(111)
plt.title(u"Histogramm der Ausfalldauer")
n, bins, patches = ax.hist(ungeplant['Dauer'], 50, facecolor='green', alpha=0.75)
plt.tight_layout()
plt.savefig("images/hist_downtime_duration.png", bbox_inches='tight')
