# vim:fileencoding=utf-8
# -*- coding: utf8 -*-
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import pandas as pd
import numpy as np
import argparse

cmd_parser = argparse.ArgumentParser()
cmd_parser.add_argument("data", help="pickle/*.pkl file with processed VID data")
args = cmd_parser.parse_args()

print "Slurping data from %s, storing into " % (args.data)
df = pd.read_pickle(args.data)
print "Datatypes: \n%s" % df.dtypes


fig = plt.figure(figsize=(16, 9), dpi=75)
ax = fig.add_subplot(111)
plt.plot(df['AnzahlAusfaelleUngeplant'], df['MittlereDauerUngeplant'], 'r.',
    label=u"Ungeplante Ausfälle")
plt.plot(df['AnzahlAusfaelleGeplant'], df['MittlereDauerGeplant'], 'k.',
    label=u"Geplante Ausfälle")
plt.xscale('log')
plt.yscale('log')
plt.xlabel(u"Median: Anzahl der gemeldeten Ausfälle")
plt.ylabel(u"Median: Ausfalldauer [Minuten]")
plt.legend(loc="best")
plt.tight_layout()
plt.savefig('images/anzahl_dauer.png', format='png')

