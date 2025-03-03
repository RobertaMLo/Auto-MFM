"""
================================================================================
PIPELINE TO RUN A PARAMETERS SWEEP with BSB4
================================================================================

Parameter of interest: rate of the background noise
Goal:   Simulate different cortical input to get the physiological frequency span
        of each population (Mossy, Glomerolous, Granule Cells, Golgi Cells,
        Purkinje Cells, Basket Cells, Stellate Cells)

************
Please cite:
- Geminiani A., Casellato C., D’Angelo E., Pedrocchi A.;
Complex Electroresponsive Dynamics in Olivocerebellar Neurons Represented With
Extended-Generalized Leaky Integrate and Fire Models. Front CompNeuro, 13 (2019)
https://www.frontiersin.org/articles/10.3389/fncom.2019.00035

- De Schepper, R., Geminiani, A., Masoli, S. et al.
Model simulations unveil the structure-function-dynamics relationship of the
cerebellar cortical microcircuit. Commun Biol 5, 1240 (2022).
https://doi.org/10.1038/s42003-022-04213-y

-  Lorenzi RM, Geminiani A, Zerlaut Y, et al.
A multi-layer mean-field model of the cerebellum embedding microstructure and
population-specific dynamics. PLoS Comput Biol 19(9): e1011434. (2023)
https://doi.org/10.1371/journal.pcbi.1011434
************
By using this code, you agree to collaborate wuth us and sharing any results with the authors.
================================================================================
version: v1
author: robertalorenzi
================================================================================
"""

from scipy import signal
from neo import io
from bsb import Scaffold, from_storage, parse_configuration_file
from pprint import pprint
#import pandas as pd
import numpy as np
import os
from os.path import join, realpath, isfile, exists
from os import listdir, makedirs
import argparse
import random
import string

def main():


    parser = argparse.ArgumentParser(description="\
                                    Script to run recursive stimulation.\
                                    Usage: recursive_stim_MF_BSB4 hdf5_file output_dir [options]\
                                     ")

    parser.add_argument("hdf5_file", help="network filename (with path)")
    parser.add_argument("output_dir", help="directory where to save the nio files. Stim Hz will be added at the end of the name")
    parser.add_argument("--freq_init", help="Initial frequency[Hz]", type=int, default=0)
    parser.add_argument("--freq_last", help="Ending frequency[Hz]", type=int, default=81)
    parser.add_argument("--df", help="frequency resolution", type=int, default=4)
    parser.add_argument("--Ie_pc", help="Ie pc to srt zmin zplus", type=float, default=700.)
    parser.add_argument("--n_core", help="number of core selected in mpi command", type=int, default=6)

    args = parser.parse_args()

    hdf5_file = args.hdf5_file
    results_folder_name = args.output_dir
    freq_init = args.freq_init
    freq_last = args.freq_last
    df = args.df

    #hdf5_file = "/home/bcc/projects/BSB4_demo/cerebellum/bsbzebrine_zmin/cerebellum_basal.hdf5"
    #results_folder_name = '/home/bcc/projects/BSB4_demo/cerebellum/bsbzebrine_zmin/results'
    #freq_init = 0
    #freq_last = 81
    #df = 4

    # ==============================================================================
    # ======================= LOAD CONFIGURATION ===================================
    # ==============================================================================

    #yaml_file = "/home/bcc/projects/BSB4_demo/my-project/my-config_Zm.yaml"
    # Importing the configuration file (BSB4 = .yaml) - package of BSB4
    #cfg = parse_configuration_file(yaml_file, "yaml")

    # printing the key-value pairs in the configuration file
    # 4zebrine: check Ie of Purkinje cells in cell_types
    #keys = ["name", "storage", "network", "regions", "partitions", "morphologies", "cell_types", "placement", "connectivity", "simulations"]
    #keys = ["simulations"]
    #for k in keys:
    #    pprint(cfg.__tree__()[k])

    # Define the population names, their abbreviations and their colors
    order_ct = ["mossy", "granule", "golgi", "purkinje", "basket", "stellate"]
    abv_ct = ["mf", "GrC", "GoC", "PC", "BC", "SC"]

    print('Neuronal Populations: ', order_ct)

    
    # ==============================================================================
    # ======================= RECURSIVE SIMULATIONS ================================
    # ==============================================================================

    for i in np.arange(freq_init,freq_last,df):

        ## Loading the network (here to reset the network at each iteration)
        network = from_storage(hdf5_file)
        #network.simulations["basal_activity"].cell_models["purkinje_cell"].constants["I_e"]=300.
        network.simulations["basal_activity"].cell_models["purkinje_cell"].constants["I_e"]=args.Ie_pc
        # # Check Parameters
        duration_sim = network.simulations["basal_activity"].duration
        dt = network.simulations["basal_activity"].resolution
        Ie_PC = network.simulations["basal_activity"].cell_models["purkinje_cell"].constants["I_e"]
        print("Simulation length [ms] ", duration_sim)
        print("Simulation dt [ms] ", dt)
        print("Purkoinje Cell Ie: ", Ie_PC)
        
        ## Setting the stimulus
        network.simulations.basal_activity.devices.background_noise.rate = i *1.0 #float
        print('============================== '
              'stimulation input = ',network.simulations.basal_activity.devices.background_noise.rate)

        ## Creating the output folder for each input rate

        results_folder_name_sim = results_folder_name+'_'+str(i)

        #RESULTS_FOLDER = realpath(results_folder_name_sim)
        #if not exists(RESULTS_FOLDER):
        #    makedirs(RESULTS_FOLDER)

        if os.path.exists(results_folder_name_sim):
            print('Folder %s for num TF has been already created!' % results_folder_name_sim)
        else:
            try:
                os.mkdir(results_folder_name_sim)
            except OSError:
                print("Creation of the directory %s failed" % results_folder_name_sim)
            else:
                print("Successfully created the directory %s " % results_folder_name_sim)

        ## Generation of an alpha-numeric ID for the mpirun files
        characters = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(characters) for _ in range(args.n_core))
        print('Alphanumeric ID: ', random_string)

        ## Running the simulation
        results = network.run_simulation("basal_activity")
        print(results)

        ## Writing the nio (I HOPE BABE)
        results.write(os.path.join(results_folder_name_sim,'back_noise'+str(i)+'_'+random_string+'.nio'), mode='rw')



if __name__ == "__main__":
    main()
