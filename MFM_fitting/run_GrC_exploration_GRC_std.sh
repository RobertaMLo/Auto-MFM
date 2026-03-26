#!/bin/bash

ROOT_DIR='./'                                       #where outputs will be saved
#NTWK="CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5"             #Netowrk with syn params
#CELL="GrC_IB2KO"                                   #cell type
CELL="GrC"


NTWK="CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5_1" 
python3 numTF_computation_BSB.py "$ROOT_DIR" "$CELL" "$NTWK"
##trick: since I cannot forcast YYMMDD_hhmmss of the TF folder just created above,
##I took whatever ends with NTWK and I select the latest created
LATEST_FOLDER=$(ls -td *_"$NTWK"* | head -n 1)
echo "Numerical TF folder created:" "$LATEST_FOLDER"
python3 plot2D_numTF.py -FOLDER "$LATEST_FOLDER"



NTWK="CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5_2" 
python3 numTF_computation_BSB.py "$ROOT_DIR" "$CELL" "$NTWK"
LATEST_FOLDER=$(ls -td *_"$NTWK"* | head -n 1)
echo "Numerical TF folder created:" "$LATEST_FOLDER"
python3 plot2D_numTF.py -FOLDER "$LATEST_FOLDER"



NTWK="CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5_3" 
python3 numTF_computation_BSB.py "$ROOT_DIR" "$CELL" "$NTWK"
LATEST_FOLDER=$(ls -td *_"$NTWK"* | head -n 1)
echo "Numerical TF folder created:" "$LATEST_FOLDER"
python3 plot2D_numTF.py -FOLDER "$LATEST_FOLDER"


NTWK="CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5_4" 
python3 numTF_computation_BSB.py "$ROOT_DIR" "$CELL" "$NTWK"
LATEST_FOLDER=$(ls -td *_"$NTWK"* | head -n 1)
echo "Numerical TF folder created:" "$LATEST_FOLDER"
python3 plot2D_numTF.py -FOLDER "$LATEST_FOLDER"


NTWK="CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5_5" 
python3 numTF_computation_BSB.py "$ROOT_DIR" "$CELL" "$NTWK"
LATEST_FOLDER=$(ls -td *_"$NTWK"* | head -n 1)
echo "Numerical TF folder created:" "$LATEST_FOLDER"
python3 plot2D_numTF.py -FOLDER "$LATEST_FOLDER"


NTWK="CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5_5_bis" 
python3 numTF_computation_BSB.py "$ROOT_DIR" "$CELL" "$NTWK"
LATEST_FOLDER=$(ls -td *_"$NTWK"* | head -n 1)
echo "Numerical TF folder created:" "$LATEST_FOLDER"
python3 plot2D_numTF.py -FOLDER "$LATEST_FOLDER"


NTWK="CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5_6" 
python3 numTF_computation_BSB.py "$ROOT_DIR" "$CELL" "$NTWK"
LATEST_FOLDER=$(ls -td *_"$NTWK"* | head -n 1)
echo "Numerical TF folder created:" "$LATEST_FOLDER"
python3 plot2D_numTF.py -FOLDER "$LATEST_FOLDER"


NTWK="CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5_7" 
python3 numTF_computation_BSB.py "$ROOT_DIR" "$CELL" "$NTWK"
LATEST_FOLDER=$(ls -td *_"$NTWK"* | head -n 1)
echo "Numerical TF folder created:" "$LATEST_FOLDER"
python3 plot2D_numTF.py -FOLDER "$LATEST_FOLDER"


NTWK="CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5_8" 
python3 numTF_computation_BSB.py "$ROOT_DIR" "$CELL" "$NTWK"
LATEST_FOLDER=$(ls -td *_"$NTWK"* | head -n 1)
echo "Numerical TF folder created:" "$LATEST_FOLDER"
python3 plot2D_numTF.py -FOLDER "$LATEST_FOLDER"


NTWK="CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5_9" 
python3 numTF_computation_BSB.py "$ROOT_DIR" "$CELL" "$NTWK"
LATEST_FOLDER=$(ls -td *_"$NTWK"* | head -n 1)
echo "Numerical TF folder created:" "$LATEST_FOLDER"
python3 plot2D_numTF.py -FOLDER "$LATEST_FOLDER"


