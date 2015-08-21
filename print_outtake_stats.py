# vim:fileencoding=utf-8
# -*- coding: utf8 -*-
#import matplotlib.pyplot as plt
#import matplotlib.mlab as mlab
#import numpy as np
import pandas as pd
#import datetime as dt
import argparse

cmd_parser = argparse.ArgumentParser()
cmd_parser.add_argument("datafile", help="pickle/*.pkl file with staged data")
args = cmd_parser.parse_args()

print "Slurping data from %s" % (args.datafile)
alldata = pd.read_pickle(args.datafile)
all_outtakes = alldata.shape[0]
print "Total of %i outtakes" % (all_outtakes)
art_types = alldata['Art'].cat.categories
print "Ausfallarten:"
for i in art_types:
  count = alldata[alldata['Art'] == i].shape[0]
  print "* %s: %i, %.2f%%" % (i, count, count*100.0/all_outtakes)

anlass_types = alldata['Anlass'].cat.categories
print u"Ausfallanlässe:"
for i in anlass_types:
  count = alldata[alldata['Anlass'] == i].shape[0]
  print "* %s: %i, %.2f%%" % (i, count, count*100.0/all_outtakes)

netzebene_types = alldata['Netzebene'].cat.categories
print u"Ausfälle auf den Netzebenen:"
for i in netzebene_types:
  count = alldata[alldata['Netzebene'] == i].shape[0]
  print "* %s: %i, %.2f%%" % (i, count, count*100.0/all_outtakes)
