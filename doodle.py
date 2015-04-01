import pandas as pd
import argparse

cmd_parser = argparse.ArgumentParser()
cmd_parser.add_argument("datafile", help="the datafile to use (xlsx)")
args = cmd_parser.parse_args()

print "Slurping %s" % args.datafile

xl = pd.ExcelFile(args.datafile)
print xl.sheet_names
df = xl.parse(0)

print df.head()

# http://stackoverflow.com/a/17335754
# Rename columns using df.columns = ['W','X','Y','Z']



