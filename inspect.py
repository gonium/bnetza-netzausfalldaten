# vim:fileencoding=utf-8
# -*- coding: utf8 -*-
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

first_outtake=np.min(alldata['Beginn'])
last_outtake=np.max(alldata['Beginn'])
print "Erster Ausfall: %s, letzter Ausfall: %s" % (first_outtake,
    last_outtake)

print "Insgesamt %d Versorger-IDs (VID) gefunden" % len(np.unique(alldata['VID']))

