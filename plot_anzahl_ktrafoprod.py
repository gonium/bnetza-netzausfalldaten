# vim:fileencoding=utf-8
# -*- coding: utf8 -*-
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns
import pandas as pd
import numpy as np
import argparse

cmd_parser = argparse.ArgumentParser()
cmd_parser.add_argument("data", help="pickle/*.pkl file with processed VID data")
args = cmd_parser.parse_args()

print "Slurping data from %s, storing into " % (args.data)
df = pd.read_pickle(args.data)
print "Datatypes: \n%s" % df.dtypes

#plt.style.use('ggplot')
plt.plot(df['AnzahlAusfaelle'], df['MittleresKtrafoProdukt'], 'k.')
plt.xscale('log')
plt.yscale('log')
plt.xlabel(u"Anzahl der gemeldeten Ausfälle")
plt.ylabel(u"Ausfallgröße [MW-Minuten bzw. MVA-Minuten]")
plt.savefig('images/anzahl_ktrafoprodukt-scatter.png', format='png')

plt.clf()
plt.hist2d(np.log(df['AnzahlAusfaelle']),
    np.log(df['MittleresKtrafoProdukt']),
    (20,20))
plt.colorbar()
plt.xlabel(u"Anzahl der gemeldeten Ausfälle")
plt.ylabel(u"Ausfallgröße [MW-Minuten bzw. MVA-Minuten]")
plt.savefig('images/anzahl_ktrafoprodukt-heatmap.png', format='png')


plt.clf()
sns.jointplot(x="AnzahlAusfaelle", y="MittleresKtrafoProdukt", 
    data=df,
    kind="kde",
    joint_kws={'xscale':'log', 'yscale':'log'});
plt.xscale('log')
plt.yscale('log')
plt.savefig('images/anzahl_ktrafoprodukt-jointplot.png', format='png')
