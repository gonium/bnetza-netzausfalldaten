# vim:fileencoding=utf-8
# -*- coding: utf8 -*-
import matplotlib.pyplot as plt
plt.style.use('ggplot')
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
first_outtake=np.min(alldata['Beginn'])
last_outtake=np.max(alldata['Beginn'])

print "Erster Ausfall: %s, letzter Ausfall: %s" % (first_outtake,
    last_outtake)

ungeplant = alldata[alldata['Art']==u"ungeplant"]

vids = np.unique(ungeplant['VID'])
anz_gemeldete_vids = len(vids)
print "Von 887 Stromnetzbetreibern wurden von %d Versorgungsunterbrechungen gemeldet (%2f%%)" % (anz_gemeldete_vids,
anz_gemeldete_vids/887.0*100)

# Reorder according to Begin
ungeplant = ungeplant.set_index(pd.DatetimeIndex(ungeplant['Beginn']))
ungeplant.sort_index(inplace=True)

# calculate overall cummulative sum for ausfallid and duration
# todo: stacking is broken.
ungeplant['ausfallnr'] = np.arange(0, len(ungeplant.index), 1)
ungeplant['cumDauer'] = np.cumsum(ungeplant['Dauer'].astype(np.float64))
print ungeplant.dtypes

# Sample ten VIDs for plotting
vids = np.random.choice(vids, 10, replace=False)
print "Will plot VIDs ", vids

fig = plt.figure(figsize=(16, 9), dpi=75)
for i in vids:
  current = ungeplant[ungeplant['VID'] == i]
  current['cumsum'] = np.cumsum(current['Dauer'])
  plt.plot(current['Beginn'].values, current['cumsum'].values,
    'k.')
  plt.plot(current['Beginn'].values, current['cumsum'].values,
    'k-')
  plt.text(np.max(current['Beginn'].values),
    np.max(current['cumsum'].values),
    "%d" % i, horizontalalignment="left", 
    verticalalignment="bottom",
    weight="bold", color="blue"
    )
plt.plot(ungeplant['Beginn'].values, 
    (ungeplant['cumDauer'].values/anz_gemeldete_vids),
    'r-', linewidth=2, label=u"Durchschnitt aller Versorger")
plt.title("Kummulierte ungeplante Unterbrechungsdauer, Versorger-ID=[%s]" % ', '.join([str(v)
  for v in vids]))
plt.xlabel("Zeit")
plt.ylabel("Ungeplante Unterbrechungsdauer [Minuten]")
#plt.yscale('log')
plt.legend(loc="best")
plt.tight_layout()
plt.savefig("images/kummulierte_ausfallzeit.png", bbox_inches='tight')

plt.clf()
fig = plt.figure(figsize=(16, 9), dpi=75)
for i in vids:
  # calculate stats for the current vid
  current = ungeplant[ungeplant['VID'] == i]
  current['sequenznummer'] = np.arange(0, len(current.index), 1)
  plt.plot(current['Beginn'].values, current['sequenznummer'].values,
    'k-')
  plt.plot(current['Beginn'].values, current['sequenznummer'].values,
    'k.')
  plt.text(np.max(current['Beginn'].values),
    np.max(current['sequenznummer'].values),
    "%d" % i, horizontalalignment="left", 
    verticalalignment="bottom",
    weight="bold", color="blue"
    )
plt.plot(ungeplant['Beginn'].values, (ungeplant['ausfallnr'].values /
  anz_gemeldete_vids), 'r-', linewidth=2, label=u"Durchschnitt aller Versorger")
plt.title("Kummulierte Anzahl der ungeplanten Unterbrechungen, Versorger-ID=[%s]" % ', '.join([str(v) for v in vids]))
plt.xlabel("Zeit")
plt.ylabel("Anzahl der ungeplanten Unterbrechungen")
#plt.yscale('log')
plt.tight_layout()
plt.legend(loc="best")
plt.savefig("images/kummulierte_unterbrechungsanzahl.png", bbox_inches='tight')
