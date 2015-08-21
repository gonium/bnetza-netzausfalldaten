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
ungeplant_hoes = ungeplant[ungeplant['Netzebene'] == u"HöS"]
ungeplant_hs = ungeplant[ungeplant['Netzebene'] == u"HS"]
ungeplant_ms = ungeplant[ungeplant['Netzebene'] == u"MS"]
ungeplant_ns = ungeplant[ungeplant['Netzebene'] == u"NS"]
print "Drawing"
fig = plt.figure(figsize=(16, 9), dpi=75)
plt.title(u"Übersicht der ungeplanten Ausfälle")
plt.xlabel("Zeit [MESZ]")
plt.ylabel("ktrafo_produkt")
plt.plot(ungeplant_ns['Beginn'], ungeplant_ns["ktrafo_produkt"],
  'k.', label=u"Niederspannungsebene")
plt.plot(ungeplant_ms['Beginn'], ungeplant_ms["ktrafo_produkt"],
  'b.', label=u"Mittelspannungsebene")
plt.plot(ungeplant_hs['Beginn'], ungeplant_hs["ktrafo_produkt"],
  'r*', label=u"Hochspannungsebene", markersize=20.0)
plt.plot(ungeplant_hoes['Beginn'], ungeplant_hoes["ktrafo_produkt"],
  'y*', label=u"Höchstspannungsebene", markersize=20.0)
plt.yscale('log')
legend=plt.legend(loc="best")
plt.tight_layout()
plt.savefig("images/all_downtimes.png", bbox_inches='tight')


