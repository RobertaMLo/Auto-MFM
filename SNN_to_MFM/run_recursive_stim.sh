#!/bin/bash

SCAFFOLD="mouse_cerebellum.hdf5"
OUTPUTDIR="./new_nios_zplusIe400/nio_files_" 

# Doing simulation
echo "***********************************************************************"
echo "I am doing SNN simulations"
echo "***********************************************************************"
#mpirun -n 6 python recursive_stim_MF_BSB4.py "$SCAFFOLD" "$OUTPUTDIR" --freq_init 84 --freq_last 201 --Ie_pc 700.

# Computing SNN Firing rate used as working frequency for num TF computation
echo "***********************************************************************"
echo "I am computing your working frequency from the simulations just ended"
echo "***********************************************************************"
python FR_standard.py "$SCAFFOLD" "$OUTPUTDIR" --freq_init 4 --freq_last 201

