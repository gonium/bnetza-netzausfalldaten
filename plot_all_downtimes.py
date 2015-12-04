# vim:fileencoding=utf-8
# -*- coding: utf8 -*-
import matplotlib.pyplot as plt
#import matplotlib.mlab as mlab
import numpy as np
import pandas as pd
import datetime as dt
import argparse
import matplotlib.ticker as mtick


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

#ungeplant_hoes = ungeplant[ungeplant['Netzebene'] == u"HoeS"]
#ungeplant_hs = ungeplant[ungeplant['Netzebene'] == u"HS"]
#ungeplant_ms = ungeplant[ungeplant['Netzebene'] == u"MS"]
#ungeplant_ns = ungeplant[ungeplant['Netzebene'] == u"NS"]
#print "Drawing"
#fig = plt.figure(figsize=(16, 9), dpi=75)
#plt.title(u"Übersicht der ungeplanten Ausfälle")
#plt.xlabel("Zeit [MESZ]")
#plt.ylabel("MVA/MW * Unterbrechungsdauer [VAmin/MWmin]")
#plt.plot(ungeplant_ns['Beginn'].values, ungeplant_ns["ktrafo_produkt"].values,
#  'k.', label=u"Niederspannungsebene (%d)" % len(ungeplant_ns))
#plt.plot(ungeplant_ms['Beginn'].values, ungeplant_ms["ktrafo_produkt"].values,
#  'b.', label=u"Mittelspannungsebene (%d)" % len(ungeplant_ms))
#plt.plot(ungeplant_hs['Beginn'].values, ungeplant_hs["ktrafo_produkt"].values,
#  'r*', label=u"Hochspannungsebene (%d)" % len(ungeplant_hs), markersize=20.0)
#plt.plot(ungeplant_hoes['Beginn'].values, ungeplant_hoes["ktrafo_produkt"].values,
#  'y*', label=u"Höchstspannungsebene (%d)" % len(ungeplant_hoes), markersize=20.0)
#plt.yscale('log')
#legend=plt.legend(loc="best")
#plt.tight_layout()
#plt.savefig("images/all_downtimes.png", bbox_inches='tight')
#
plt.clf()
width=20
fig = plt.figure(figsize=(16, 9), dpi=75)
ax = fig.add_subplot(111)
plt.title(u"Monatssummen der ungeplanten Ausfälle")
plt.xlabel("Monat")
plt.ylabel("GVA/GW * Unterbrechungsdauer [GAmin/GWmin]")
ungeplant = ungeplant.set_index(pd.DatetimeIndex(ungeplant['Beginn']))
ungeplant_monat=ungeplant.resample('1M', how='sum')
plt.bar(ungeplant_monat.index, ungeplant_monat["ktrafo_produkt"].values/1000,
    width, color='r')
ax.yaxis.set_major_formatter(mtick.FormatStrFormatter("%d"))
locs, labels = plt.yticks()
plt.setp(labels, rotation=30)
plt.tight_layout()
plt.savefig("images/monthly_downtimes.png", bbox_inches='tight')
