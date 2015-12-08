# vim:fileencoding=utf-8
# -*- coding: utf8 -*-
import matplotlib.pyplot as plt
plt.style.use('ggplot')
#import matplotlib.mlab as mlab
import numpy as np
import pandas as pd
import datetime as dt
import argparse

cmd_parser = argparse.ArgumentParser()
cmd_parser.add_argument("data", help="pickle/*.pkl file with vid data")
args = cmd_parser.parse_args()

print "Slurping data from %s" % (args.data)
df = pd.read_pickle(args.data)
print "Datatypes: \n%s" % df.dtypes

print "Drawing"
fig = plt.figure(figsize=(16, 9), dpi=75)
plt.title(u"Ausfälle aller Versorger 2008-2013")
plt.xlabel(u"Anzahl geplante Ausfälle")
plt.ylabel(u"Anzahl ungeplante Ausfälle")
plt.xscale('log')
plt.yscale('log')
plt.plot(df['AnzahlAusfaelleGeplant'].values, df['AnzahlAusfaelleUngeplant'].values,
  'k.', label=u"Versorger")
x = np.linspace(*plt.xlim())
plt.plot(x, x, 'r')
plt.tight_layout()
plt.savefig("images/anzahl_geplant_vs_ungeplant.png", bbox_inches='tight')

plt.clf()
fig = plt.figure(figsize=(16, 9), dpi=75)
plt.title(u"Durchschnittliche Ausfallgröße (MVA/MW x Unterbrechungsdauer) aller Versorger 2008-2013")
plt.xlabel(u"Geplant [VAmin/MWmin]")
plt.ylabel(u"Ungeplant: [VAmin/MWmin]")
plt.xscale('log')
plt.yscale('log')
plt.plot(df['MittleresKtrafoProduktGeplant'].values, df['MittleresKtrafoProduktUngeplant'].values, 'k.', label=u"Versorger")
x = np.linspace(*plt.xlim())
plt.plot(x, x, 'r')
plt.tight_layout()
plt.savefig("images/ktrafo_geplant_vs_ungeplant.png", bbox_inches='tight')
