# vim:fileencoding=utf-8
# -*- coding: utf8 -*-
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import argparse

cmd_parser = argparse.ArgumentParser()
cmd_parser.add_argument("data", help="pickle/*.pkl file with processed VID data")
args = cmd_parser.parse_args()

print "Slurping data from %s" % (args.data)
df = pd.read_pickle(args.data)
print "Datatypes: \n%s" % df.dtypes

mtbfungeplant_minutes_median = np.median(df['MTBFUngeplant_minutes'])
mtbfungeplant_minutes_min = np.min(df['MTBFUngeplant_minutes'])
mtbfungeplant_minutes_max = np.max(df['MTBFUngeplant_minutes'])
dauerungeplant_median = np.median(df['MittlereDauerUngeplant'])
dauerungeplant_min = np.min(df['MittlereDauerUngeplant'])
dauerungeplant_max = np.max(df['MittlereDauerUngeplant'])

mtbfgeplant_minutes_median = np.median(df['MTBFGeplant_minutes'])
mtbfgeplant_minutes_min = np.min(df['MTBFGeplant_minutes'])
mtbfgeplant_minutes_max = np.max(df['MTBFGeplant_minutes'])
dauergeplant_median = np.median(df['MittlereDauerGeplant'])
dauergeplant_min = np.min(df['MittlereDauerGeplant'])
dauergeplant_max = np.max(df['MittlereDauerGeplant'])

plotxmin = mtbfgeplant_minutes_min
plotxmax = mtbfungeplant_minutes_max
plotymin = dauergeplant_min
plotymax = dauerungeplant_max

label_geplant = u"Geplante Ausfälle - Median MTBF: %.0f, Dauer: %0.f Min." % (mtbfgeplant_minutes_median, dauergeplant_median)
label_ungeplant = u"Ungeplante Ausfälle - Median MTBF: %.0f, Dauer: %0.f Min." % (mtbfungeplant_minutes_median, dauerungeplant_median)

fig = plt.figure(figsize=(16, 9), dpi=75)
ax = fig.add_subplot(111)
plt.plot(df['MTBFGeplant_minutes'], df['MittlereDauerGeplant'],
  'k.', label=label_geplant)
plt.plot(df['MTBFUngeplant_minutes'], df['MittlereDauerUngeplant'],
  'r.', label=label_ungeplant)
plt.plot((mtbfgeplant_minutes_median, mtbfgeplant_minutes_median),
    (plotymin, plotymax), 'k-', linewidth=2)
plt.plot((plotxmin, plotxmax),
    (dauergeplant_median, dauergeplant_median), 'k-', linewidth=2)
plt.plot((mtbfungeplant_minutes_median, mtbfungeplant_minutes_median),
    (plotymin, plotymax), 'r-', linewidth=2)
plt.plot((plotxmin, plotxmax),
    (dauerungeplant_median, dauerungeplant_median), 'r-', linewidth=2)
plt.title(u'Ausfälle aller %d Netzbetreiber 2007-2013' % len(np.unique(df.index)))
plt.xscale('log')
plt.yscale('log')
plt.xlim((plotxmin, plotxmax))
plt.ylim((plotymin, plotymax))
plt.legend(loc="best", prop={"size": 12})
plt.xlabel(u"Mittlere Zeit zwischen zwei Ausfällen (MTBF) [Minuten]")
plt.ylabel(u"Mittlere Ausfalldauer [Minuten]")
plt.tight_layout()
plt.savefig('images/mtbf_dauer.png', format='png')


