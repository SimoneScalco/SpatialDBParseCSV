#!/usr/bin/env bash

# Checks if the results directory exists and cleans the environment
if [  -d "results" ]; then

  echo "[MAIN] Cleaning environment..."
  rm -r results

fi

# Creates the output subdirectories
mkdir results
mkdir results/create_tables
mkdir results/insert_queries
mkdir results/insert_queries/raw

# Parses the CSV file and specifies the column division
python parseCSV.py R04_indicatori_2011_areecensimento.csv 6,6,-1 83,7_6,6 98,7_6,6 104,7_6,6 116,7_6,6 147,7_6,6

#python parseCSV.py 6,13,89,104,110,122,153 R04_indicatori_2011_localita.csv

#python parseCSV.py R04_indicatori_2011_sezioni.csv 6, 87, 102, 108, 120, 151

# Merges the files contained in the first subdirectory
python mergeFiles.py results/create_tables/ .sql

# Merges the files contained in the second subdirectory
python mergeFiles.py results/insert_queries/ .sql

#Remove duplicates
python removeDuplicates.py results/insert_queries/DIRECTORY_MERGE.sql

#Remapping table names
python remap.py results/create_tables/DIRECTORY_MERGE.sql census_area_0:COMUNI census_area_1:POPOLAZIONE_RESIDENTE census_area_2:STRANIERI_RESIDENTI census_area_3:ABITAZIONI census_area_4:FAMIGLIE census_area_5:EDIFICI

python remap.py results/insert_queries/DIRECTORY_MERGE.sql census_area_0:COMUNI census_area_1:POPOLAZIONE_RESIDENTE census_area_2:STRANIERI_RESIDENTI census_area_3:ABITAZIONI census_area_4:FAMIGLIE census_area_5:EDIFICI

#Merge all DIRECTORY_MERGE
python mergeAll.py DIRECTORY_MERGE.sql DB.sql