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

# Parses the CSV file and specifies the column division
python parseCSV.py 2,18,25,26,147

# Merges the files contained in the first subdirectory
python mergeFiles.py results/create_tables/ .txt

# Merges the files contained in the second subdirectory
python mergeFiles.py results/insert_queries/ .txt