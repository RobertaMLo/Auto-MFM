#!/bin/bash

# Set fixed parameters [ms]
TIME_FROM="200.0"
TIME_TO="5000.0"
DT="0.1"

## Zmin
#FILE_NIO_FOLDER="./new_nios/"
## Zplus
#FILE_NIO_FOLDER="./new_nios_zplusIe400/"

##vitro zmin
FILE_NIO_FOLDER="./new_nios_vitro/"

# Run GNU parallel to execute Python scripts in parallel for folders from results_4 to results_80

seq 4 4 201 | parallel -j 1 "python3 results_ana.py  ${FILE_NIO_FOLDER}nio_files_{} --time_from $TIME_FROM --time_to $TIME_TO --dt $DT > ./log_{}.txt 2>&1"

#python3 results_ana.py ./bsbzebrine_zmin_new/results_0 --time_from $TIME_FROM --time_to $TIME_TO --dt $DT
