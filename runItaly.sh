#!/usr/bin/env bash

###############################################
################## SEZIONI ####################
###############################################

let i=1

for fileName in results/DatasetUnziped/*.csv; do
    echo "$fileName"


    ./clearResults.sh

    python parseCSV.py $fileName 6,6,-1 11,7,6 87,7,7 102,7,7 108,7,7 120,7,7 151,7,7

    # Merges the files contained in the first subdirectory
    python mergeFiles.py results/create_tables/ .sql

    # Merges the files contained in the second subdirectory
    python mergeFiles.py results/insert_queries/ .sql

    #Remove duplicates
    python removeDuplicates.py results/insert_queries/DIRECTORY_MERGE.sql

    #Remapping table names
    python remap.py results/create_tables/DIRECTORY_MERGE.sql census_area_0:COMUNI census_area_1:SEZIONI census_area_2:POPOLAZIONE_RESIDENTE census_area_3:STRANIERI_RESIDENTI census_area_4:ABITAZIONI census_area_5:FAMIGLIE census_area_6:EDIFICI

    python remap.py results/insert_queries/DIRECTORY_MERGE.sql census_area_0:COMUNI census_area_1:SEZIONI census_area_2:POPOLAZIONE_RESIDENTE census_area_3:STRANIERI_RESIDENTI census_area_4:ABITAZIONI census_area_5:FAMIGLIE census_area_6:EDIFICI

    #Merge all DIRECTORY_MERGE
    #python mergeAll.py DIRECTORY_MERGE.sql DB_sezioni.sql drop_all_tables.sql
    cp results/insert_queries/DIRECTORY_MERGE.sql results/R{$i}.sql

    echo "[Main] SEZIONI $fileName COMPLETED i=$i"

    let i=i+1

done

cp results/create_tables/DIRECTORY_MERGE.sql results/CREATE_ALL.sql
###############################################
############### EXTRA INFO ####################
###############################################

./clearResults.sh

cp Elenco_comuni_2011.csv results/.
python number_format.py results/Elenco_comuni_2011.csv

python parseCSV.py results/Elenco_comuni_2011.csv 24,6,-1

# Merges the files contained in the first subdirectory
python mergeFiles.py results/create_tables/ .sql

# Merges the files contained in the second subdirectory
python mergeFiles.py results/insert_queries/ .sql

#Remove duplicates
python removeDuplicates.py results/insert_queries/DIRECTORY_MERGE.sql

#Remapping table names
python remap.py results/create_tables/DIRECTORY_MERGE.sql census_area_0:LOC_EXTRA "SUPERFICIE (in KMQ):SUPERFICIE_KMQ"

python remap.py results/insert_queries/DIRECTORY_MERGE.sql census_area_0:LOC_EXTRA "SUPERFICIE (in KMQ):SUPERFICIE_KMQ" SUPERFICIEinKMQ:SUPERFICIE_KMQ


#Merge all DIRECTORY_MERGE
python mergeAll.py DIRECTORY_MERGE.sql DB_EXTRA_elenco_comuni.sql