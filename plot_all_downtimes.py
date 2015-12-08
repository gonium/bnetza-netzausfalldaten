# vim:fileencoding=utf-8
# -*- coding: utf8 -*-
import matplotlib.pyplot as plt
plt.style.use('ggplot')
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
geplant = alldata[alldata['Art']==u"geplant"]
ungeplant = ungeplant.set_index(pd.DatetimeIndex(ungeplant['Beginn']))
ungeplant_monat=ungeplant.resample('1M', how='sum')
geplant = geplant.set_index(pd.DatetimeIndex(geplant['Beginn']))
geplant_monat=geplant.resample('1M', how='sum')

ungeplant_hoes = ungeplant[ungeplant['Netzebene'] == u"HoeS"]
ungeplant_hs = ungeplant[ungeplant['Netzebene'] == u"HS"]
ungeplant_ms = ungeplant[ungeplant['Netzebene'] == u"MS"]
ungeplant_ns = ungeplant[ungeplant['Netzebene'] == u"NS"]

geplant_hoes = geplant[geplant['Netzebene'] == u"HoeS"]
geplant_hs = geplant[geplant['Netzebene'] == u"HS"]
geplant_ms = geplant[geplant['Netzebene'] == u"MS"]
geplant_ns = geplant[geplant['Netzebene'] == u"NS"]


print "Drawing"

plt.clf()
width=20
fig = plt.figure(figsize=(16, 9), dpi=75)
ax = fig.add_subplot(111)
plt.title(u"Monatssummen der ungeplanten Ausfälle")
plt.xlabel("Monat")
plt.ylabel("Ausgefallene Leistung * Unterbrechungsdauer [GVAmin/GWmin]")
plt.bar(ungeplant_monat.index, ungeplant_monat["ktrafo_produkt"].values/1000,
    width, color='r')
ax.yaxis.set_major_formatter(mtick.FormatStrFormatter("%d"))
locs, labels = plt.yticks()
plt.setp(labels, rotation=30)
locs, labels = plt.xticks()
plt.setp(labels, rotation=30)
plt.tight_layout()
plt.savefig("images/monthly_failure_downtimes.png", bbox_inches='tight')

plt.clf()
width=20
fig = plt.figure(figsize=(16, 9), dpi=75)
ax = fig.add_subplot(111)
plt.title(u"Monatssummen der geplanten Ausfälle")
plt.xlabel("Monat")
plt.ylabel("Ausgefallene Leistung * Unterbrechungsdauer [GVAmin/GWmin]")
plt.bar(geplant_monat.index, geplant_monat["ktrafo_produkt"].values/1000,
    width, color='k')
ax.yaxis.set_major_formatter(mtick.FormatStrFormatter("%d"))
locs, labels = plt.yticks()
plt.setp(labels, rotation=30)
locs, labels = plt.xticks()
plt.setp(labels, rotation=30)
plt.tight_layout()
plt.savefig("images/monthly_planned_downtimes.png", bbox_inches='tight')

plt.clf()
width=10
fig = plt.figure(figsize=(16, 9), dpi=75)
ax = fig.add_subplot(111)
plt.title(u"Monatssummen der Ausfälle")
plt.xlabel("Monat")
plt.ylabel("Ausgefallene Leistung * Unterbrechungsdauer [GVAmin/GWmin]")
plt.bar(ungeplant_monat.index, ungeplant_monat["ktrafo_produkt"].values/1000,
    width, color='r', label=u"ungeplante Ausfälle")
plt.bar(geplant_monat.index + pd.DateOffset(days=15), geplant_monat["ktrafo_produkt"].values/1000,
    width, color='k', label=u"geplante Ausfälle")
ax.yaxis.set_major_formatter(mtick.FormatStrFormatter("%d"))
locs, labels = plt.yticks()
plt.setp(labels, rotation=30)
locs, labels = plt.xticks()
plt.setp(labels, rotation=30)
plt.legend(loc="best")
plt.tight_layout()
plt.savefig("images/monthly_combined_downtimes.png", bbox_inches='tight')

plt.clf()
fig = plt.figure(figsize=(16, 9), dpi=75)
plt.title(u"Übersicht der ungeplanten Ausfälle")
plt.xlabel("Zeit [MESZ]")
plt.ylabel("Ausgefallene Leistung * Unterbrechungsdauer [MVAmin/MWmin]")
plt.plot(ungeplant_ns['Beginn'].values, ungeplant_ns["ktrafo_produkt"].values,
  'k.', label=u"Niederspannungsebene (%d)" % len(ungeplant_ns))
plt.plot(ungeplant_ms['Beginn'].values, ungeplant_ms["ktrafo_produkt"].values,
  'b.', label=u"Mittelspannungsebene (%d)" % len(ungeplant_ms))
plt.plot(ungeplant_hs['Beginn'].values, ungeplant_hs["ktrafo_produkt"].values,
  'r*', label=u"Hochspannungsebene (%d)" % len(ungeplant_hs), markersize=20.0)
plt.plot(ungeplant_hoes['Beginn'].values, ungeplant_hoes["ktrafo_produkt"].values,
  'y*', label=u"Höchstspannungsebene (%d)" % len(ungeplant_hoes), markersize=20.0)
plt.yscale('log')
legend=plt.legend(loc="best")
plt.tight_layout()
plt.savefig("images/all_failure_downtimes.png", bbox_inches='tight')

plt.clf()
fig = plt.figure(figsize=(16, 9), dpi=75)
plt.title(u"Übersicht der geplanten Ausfälle")
plt.xlabel("Zeit [MESZ]")
plt.ylabel("Ausgefallene Leistung * Unterbrechungsdauer [MVAmin/MWmin]")
plt.plot(geplant_ns['Beginn'].values, geplant_ns["ktrafo_produkt"].values,
  'k.', label=u"Niederspannungsebene (%d)" % len(geplant_ns))
plt.plot(geplant_ms['Beginn'].values, geplant_ms["ktrafo_produkt"].values,
  'b.', label=u"Mittelspannungsebene (%d)" % len(geplant_ms))
plt.plot(geplant_hs['Beginn'].values, geplant_hs["ktrafo_produkt"].values,
  'r*', label=u"Hochspannungsebene (%d)" % len(geplant_hs), markersize=20.0)
plt.plot(geplant_hoes['Beginn'].values, geplant_hoes["ktrafo_produkt"].values,
  'y*', label=u"Höchstspannungsebene (%d)" % len(geplant_hoes), markersize=20.0)
plt.yscale('log')
legend=plt.legend(loc="best")
plt.tight_layout()
plt.savefig("images/all_planned_downtimes.png", bbox_inches='tight')

