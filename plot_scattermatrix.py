# vim:fileencoding=utf-8
# -*- coding: utf8 -*-
import matplotlib.pyplot as plt
#import matplotlib.mlab as mlab
import numpy as np
import pandas as pd
import datetime as dt
import argparse
from pandas.tools.plotting import scatter_matrix

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

scatter_matrix(alldata, alpha=0.2, figsize=(6,6), diagonal='kde')
