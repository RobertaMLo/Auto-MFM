#!/bin/bash

OUTPUT_DIR="/home/bcc/projects/BSB4_demo/cerebellum_zmin_Ie1.2/"

PYTHON_SCRIPT="run_mean_field_simulation_backnoise.py"


START=84
END=201
STEP=4

N_CORE=6

seq $START $STEP $END | parallel -j $N_CORE "python3 \"$PYTHON_SCRIPT\" -FOLDER \"$OUTPUT_DIR\" -f_backnoise {} -save_sim True"

echo "Now running the constructive validity"

python3 run_mean_field_constr_validity.py -path_mf ./ -path_snn ./

## I BROKE MY PC WITH THE OPTIONS BELOW:

## parallel sim (8 core here)
#MAX_JOBS=6
#JOBS=0

#f=$START

#while [ "$f" -le "$END" ]; do
# for ((f=$START; f<=$END; f+=$STEP)); do # THIS IS OK AS WELL BUT MUST BE RUN  WITH bash <file_name> because it's not supported by other shell types.
#    echo "Running simulation with f_backnoise=$f"
    
#    python3 "$PYTHON_SCRIPT" -FOLDER "$OUTPUT_DIR" -f_backnoise "$f" &

#    ((JOBS++))
    
    # Check on n max jobs
#    if (( JOBS >= MAX_JOBS )); then
#        wait
#        JOBS=0
#    fi
    
#    f =$((f + STEP)) #to be commented when use the for
    
#done

# wait all process
#wait

#echo "All simulations completed."
