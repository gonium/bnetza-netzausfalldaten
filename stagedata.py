# -*- coding: utf8 -*-
import pandas as pd
import numpy as np
import argparse
import os
# pip install progressbar2
import progressbar as pb

cmd_parser = argparse.ArgumentParser()
cmd_parser.add_argument("datadir", help="directory containing the *.xlsx files")
cmd_parser.add_argument("outfile", help="pickle/.pkl file to create")
args = cmd_parser.parse_args()

print "Slurping data from %s, writing to %s" % (args.datadir,
    args.outfile)
files = sorted(os.listdir(args.datadir))

print "Loading datasets. This might take a while."
alldata = None
with pb.ProgressBar(maxval=len(files)) as progress:
  for idx, file in enumerate(files):
    xl = pd.ExcelFile( os.path.join(args.datadir, file))
    newdata = xl.parse(0)
    if idx == 0:
      alldata = newdata
    else:
      alldata = alldata.append(newdata, ignore_index=True)
    progress.update(idx)
print "Finished reading data into memory."

print "Data cleanup"
# http://stackoverflow.com/a/17335754
# Rename columns using df.columns = ['W','X','Y','Z']
alldata[['Beginn']] = pd.to_datetime(alldata['Beginn'], format="%Y-%m-%d %H:%M:%S.%f")

def label_netzebene(row):
  if row[u'HöS'] == 1:
    return u"HS"
  if row[u'HS'] == 1:
    return u"MS"
  if row[u'MS'] == 1:
    return u"MS"
  if row[u'NS'] == 1:
    return u"NS"

alldata['Netzebene'] = alldata.apply(lambda row: label_netzebene(row),
    axis=1)

for col in ['Art', 'Anlass', 'Netzebene']:
  alldata[col] = alldata[col].astype('category')


print alldata.head()
print alldata.dtypes

print "Writing output file"
alldata.to_pickle(args.outfile)




