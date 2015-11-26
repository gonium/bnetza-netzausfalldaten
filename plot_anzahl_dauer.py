# vim:fileencoding=utf-8
# -*- coding: utf8 -*-
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import argparse

cmd_parser = argparse.ArgumentParser()
cmd_parser.add_argument("data", help="pickle/*.pkl file with processed VID data")
args = cmd_parser.parse_args()

print "Slurping data from %s, storing into " % (args.data)
df = pd.read_pickle(args.data)
print "Datatypes: \n%s" % df.dtypes


plt.plot(df['AnzahlAusfaelle'], df['MittlereDauer'], 'k.')
plt.xscale('log')
plt.yscale('log')
plt.xlabel(u"Anzahl der gemeldeten Ausfälle")
plt.ylabel(u"Mittlere Ausfalldauer [Minuten]")
plt.savefig('images/anzahl_dauer.png', format='png')


