#!/bin/bash -l
#SBATCH --job-name=MFCLUST
#SBATCH --time=168:59:59
#SBATCH --ntasks=32
#SBACTH --cpus-per-task=1
#SBATCH --partition=neuro
#SBATCH --mem-per-cpu=8G

#SBATCH -D /home/neuro_img/Users/Roberta/cerebellum_zmin_plv_Ie780_debug_corrected/

source ../mfm/bin/activate

sh run_constr_validity.sh
