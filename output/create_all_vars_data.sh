#!/usr/bin/env bash

echo "Untarring data archive"
tar -xvzf vars_20180204.tar.gz

echo "Writing header"
head -1 ./vars_20180204/all_vars-764001-1529150.csv > all_vars.csv

echo "Writing CSVs to one file _all_vars.csv_"
tail -q -n +2  ./vars_20180204/*.csv >> all_vars.csv



echo "Moving all_vars.csv to input_metadata directory"
mv all_vars.csv ../input_metadata/all_vars_ctrl_m.csv

echo "Clean up the trash"
rm -rf ./vars_20180204/

echo "You still need to run echo sed -e \"s/^M//\" ../input_metadata/all_vars_ctrl_m.csv > ../input_metadata/all_vars.csv"