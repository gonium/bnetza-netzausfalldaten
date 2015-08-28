# vim:fileencoding=utf-8
# -*- coding: utf8 -*-
import matplotlib.pyplot as plt
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

vids = np.unique(ungeplant['VID'])
anz_gemeldete_vids = len(vids)
print "Von 887 Stromnetzbetreibern wurden von %d Versorgungsunterbrechungen gemeldet (%2f%%)" % (anz_gemeldete_vids, anz_gemeldete_vids/887.0)

fig = plt.figure(figsize=(16, 9), dpi=75)
for i in vids:
  current = ungeplant[ungeplant['VID'] == i]
  current['cumsum'] = np.cumsum(current['Dauer'])
  plt.plot(current['Beginn'], current['cumsum'],
    'k-', label=u"%d"%i)
plt.xlabel("Zeit")
plt.ylabel("Ungeplante Unterbrechungsdauer [Minuten]")
plt.yscale('log')
plt.tight_layout()
plt.savefig("images/kummulierte_ausfallzeit.png", bbox_inches='tight')
