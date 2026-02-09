#!/bin/bash

OUTPUT_DIR="./"

PYTHON_SCRIPT="run_mean_field_simulation_backnoise.py"

##### BRUTTO HARD CODED!! DEVI ANDARE DENTRO E SISTEMARE LE TF A SECONDA DI CONFIRAZIONE PERCHÈ

#NTWK="CRBL_CONFIG_AUTOMFM_AWAKE_FIT_6"

NTWK="CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5"

ALPHA_LIST="2.1 2.4 1.6 5.4" 
#"3.00 2.51 4.31 9.24" #THR SLOPE

#for_backnoise
START=4 #4
END=81
STEP=4
#for_stim_step
#START=10
#END=150
#STEP=10

N_SIM=100

for n in $(seq 0 1 $N_SIM); do

  echo "#SIMULATION $n out of $N_SIM"

  OUT_FOLDER_NEW="20260123_${NTWK}_PSTHNEW_CLUST_${n}"
  mkdir -p "${OUT_FOLDER_NEW}"

  #N_CORE=1
  #seq $START $STEP $END | parallel -j $N_CORE "python3 \"$PYTHON_SCRIPT\" -FOLDER \"$OUTPUT_DIR\" -NTWK \"$NTWK\" -f_backnoise {} -alfa $ALPHA_LIST -save_sim True"

  for f in $(seq $START $STEP $END); do
      python3 "$PYTHON_SCRIPT" \
          -FOLDER "$OUTPUT_DIR" \
          -NTWK "$NTWK" \
          -f_backnoise "$f" \
          -alfa $ALPHA_LIST \
          -save_sim True
  done



#echo "Now running the constructive validity"
python3 run_mean_field_constr_validity.py -f_start_end $START $END $STEP -path_mf ./ -path_snn ./ -NTWK "$NTWK" -outdir "$OUT_FOLDER_NEW"

  LC_NUMERIC=C ## Otherwise with 1.f it creates with , like 4,0.
  for i in $(seq -f "%.1f" $START $STEP $END); do
      DIR="${OUTPUT_DIR}${i}_${NTWK}"
      if [ -d "$DIR" ]; then
          echo "Moving $DIR to $OUT_FOLDER_NEW/"
          mv "$DIR" "$OUT_FOLDER_NEW"/
      else
          echo "Directory \"$DIR\" not found"
      fi
  done

done
