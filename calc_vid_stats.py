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
  vid_data_ungeplant = alldata[(alldata['VID'] == v) & (alldata['Art']
    == "ungeplant")]
  vid_data_geplant = alldata[(alldata['VID'] == v) & (alldata['Art'] ==
    "geplant")]
  ausfallbeginn_ungeplant = vid_data_ungeplant['Beginn']
  ausfallbeginn_geplant = vid_data_geplant['Beginn']
  anzahl_ungeplant = len(ausfallbeginn_ungeplant)
  anzahl_geplant = len(ausfallbeginn_geplant)
  mtbf_ungeplant = calc_mtbf(ausfallbeginn_ungeplant)
  mtbf_geplant = calc_mtbf(ausfallbeginn_geplant)
  mean_dauer_ungeplant = np.mean(vid_data_ungeplant['Dauer'])
  mean_dauer_geplant = np.mean(vid_data_geplant['Dauer'])
  mean_ktrafo_produkt_ungeplant = np.mean(vid_data_ungeplant['ktrafo_produkt'])
  mean_ktrafo_produkt_geplant = np.mean(vid_data_geplant['ktrafo_produkt'])
  print "VID %d - ungeplant: %d Ausfälle, MTBF: %s, Mittlere Dauer: %.2f, Mittleres KTrafo-Produkt %.2f" % (v, anzahl_ungeplant,
    mtbf_ungeplant, mean_dauer_ungeplant, mean_ktrafo_produkt_ungeplant)
  print "VID %d - geplant: %d Ausfälle, MTBF: %s, Mittlere Dauer: %.2f, Mittleres KTrafo-Produkt %.2f" % (v, anzahl_geplant,
    mtbf_geplant, mean_dauer_geplant, mean_ktrafo_produkt_geplant)
  data[v] = {
      'AnzahlAusfaelleUngeplant': anzahl_ungeplant,
      'MTBFUngeplant': mtbf_ungeplant,
      'MittlereDauerUngeplant': mean_dauer_ungeplant,
      'MittleresKtrafoProduktUngeplant': mean_ktrafo_produkt_ungeplant,
      'AnzahlAusfaelleGeplant': anzahl_geplant,
      'MTBFGeplant': mtbf_geplant,
      'MittlereDauerGeplant': mean_dauer_geplant,
      'MittleresKtrafoProduktGeplant': mean_ktrafo_produkt_geplant
    }
df = pd.DataFrame.from_dict(data, orient='index')
df['MTBFUngeplant_minutes'] = df['MTBFUngeplant'].apply(lambda x: x/np.timedelta64(60,'s'))
df['MTBFGeplant_minutes'] = df['MTBFGeplant'].apply(lambda x: x/np.timedelta64(60,'s'))
print df.describe()

print "Saving to output file %s" %args.outputfile
df.to_pickle(args.outputfile)
