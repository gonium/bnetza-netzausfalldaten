# vim:fileencoding=utf-8
# -*- coding: utf8 -*-
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import argparse


cmd_parser = argparse.ArgumentParser()
cmd_parser.add_argument("datafile", help="pickle/*.pkl file with staged data")
args = cmd_parser.parse_args()

print "Slurping data from %s" % (args.datafile)
alldata = pd.read_pickle(args.datafile)
print "Datatypes: \n%s" % alldata.dtypes

vids = np.unique(alldata['VID'])
print "Insgesamt %d Versorger-IDs (VID) gefunden" % len(vids)

def calc_mtbf(series):
  return series.diff().mean(skipna=True)

data = {}
for v in vids:
  ausfallbeginn = alldata[alldata['VID'] == v]['Beginn']
  anzahl = len(ausfallbeginn)
  mtbf = calc_mtbf(ausfallbeginn)
  print "VID %d: %d Ausfälle, MTBF: %s"% (v, anzahl, mtbf)
  data[v] = {'AnzahlAusfaelle': anzahl, 'MTBF': mtbf}
df = pd.DataFrame.from_dict(data, orient='index')
print df.describe()

plt.plot(df['AnzahlAusfaelle'], df['MTBF'], 'k.')
plt.savefig('images/anzahl_mtbf.png', format='png')
