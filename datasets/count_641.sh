#!/usr/bin/env bash

echo "Using CSV files to count unplanned outages of VID 641"

find . -iname "*.xlsx.csv" | while read f; do
  count=$(grep "^641," "$f" | grep "ungeplant" | wc -l)
  echo "$f: $count"
done
