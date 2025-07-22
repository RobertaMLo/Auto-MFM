#!/bin/bash


FREQ_LIST=(4 40 80) 
## Inzio con 3 frequenze che sono : npop x ngen x nfreqs = 8 * 50 * 3 = 1200 

# Numero massimo di job paralleli
N_JOBS=3

# Lancia l'ottimizzazione in parallelo per ogni frequenza
parallel -j $N_JOBS "python3 multi_obj_opt_mfm_3freq.py --freqs {} > log_opt_NSGA2{}.txt 2>&1" ::: "${FREQ_LIST[@]}"

