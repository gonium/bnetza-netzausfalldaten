# vim:fileencoding=utf-8
# -*- coding: utf8 -*-
import numpy as np
import pandas as pd
import argparse


cmd_parser = argparse.ArgumentParser()
cmd_parser.add_argument("inputfile", help="pickle/*.pkl file with staged data")
cmd_parser.add_argument("outputfile", help="pickle/*.pkl file with processed VID data")
args = cmd_parser.parse_args()

print "Slurping data from %s, storing into %s" % (args.inputfile, args.outputfile)
alldata = pd.read_pickle(args.inputfile)
print "Datatypes: \n%s" % alldata.dtypes

vids = np.unique(alldata['VID'])
print "Insgesamt %d Versorger-IDs (VID) gefunden" % len(vids)

def calc_mtbf(series):
  return series.diff().mean(skipna=True)

data = {}
for v in vids:
  vid_data = alldata[alldata['VID'] == v]
  ausfallbeginn = vid_data['Beginn']
  anzahl = len(ausfallbeginn)
  mtbf = calc_mtbf(ausfallbeginn)
  mean_dauer = np.mean(vid_data['Dauer'])
  mean_ktrafo_produkt = np.mean(vid_data['ktrafo_produkt'])
  print "VID %d: %d Ausfälle, MTBF: %s, Mittlere Dauer: %.2f, Mittleres KTrafo-Produkt %.2f"% (v, anzahl, mtbf, mean_dauer, mean_ktrafo_produkt)
  data[v] = {
      'AnzahlAusfaelle': anzahl,
      'MTBF': mtbf,
      'MittlereDauer': mean_dauer,
      'MittleresKtrafoProdukt': mean_ktrafo_produkt
    }
df = pd.DataFrame.from_dict(data, orient='index')
df['MTBF_minutes'] = df['MTBF'].apply(lambda x: x/np.timedelta64(60,'s'))
print df.describe()

print "Saving to output file %s" %args.outputfile
df.to_pickle(args.outputfile)
