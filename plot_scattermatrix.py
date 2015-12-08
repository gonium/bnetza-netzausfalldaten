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
df = pd.read_pickle(args.datafile)
print df.dtypes
print "I counted %d samples." % df.shape[0]

samplesize=np.min((df.shape[0], 1000))
print "Sampling %d elements" % samplesize
df = df.loc[np.random.choice(df.index, samplesize, replace=False)]

scatter_matrix(df, alpha=0.2, figsize=(25,25))#, diagonal='kde')
locs, labels = plt.yticks()
plt.setp(labels, rotation=30)
locs, labels = plt.xticks()
plt.setp(labels, rotation=30)
plt.savefig("images/scattermatrix.png", bbox_inches='tight')
