#!/usr/bin/env bash

echo "Please install xlsx2csv:"
echo " $ easy_install xlsx2csv"

find . -iname "*.xlsx" | while read f; do
  outfile="$f".csv
  echo "$f -> $outfile"
  xlsx2csv "$f" "$outfile"
done
