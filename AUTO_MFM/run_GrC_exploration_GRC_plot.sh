#!/bin/bash

ROOT_DIR='./'                                       #where outputs will be saved
#NTWK="CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5"              #Netowrk with syn params
#CELL="GrC_IB2KO"                                    #cell type
CELL="GrC"

for i in $(seq 1 1 8); do
	NAME="GrC_CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5_${i}_tsim5"
      	FOLDER=$(ls -d *_$NAME)
	echo $FOLDER
  python3 plot2D_numTF.py -FOLDER $FOLDER
done

