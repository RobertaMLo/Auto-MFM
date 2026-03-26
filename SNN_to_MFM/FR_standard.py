"""
=======================================================================================================
======================== COMPUTING THE POPULATION-SPECIFIC WORKING FREQUENCY ==========================
=======================================================================================================

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

Authors:
code prepared by: robilorenzi && marialauradegrazia
Feb, 2025
========================================================================================================
"""


from cerebellum.analysis.spiking_results import BasicSimulationReport, SimResultsTable
from bsb import from_storage
import numpy as np
import pandas as pd
import os
import argparse


def main():


    parser = argparse.ArgumentParser(description="\
                                    Script to compute the average firing rate from SNN.\
                                    Usage: recursive_stim_MF_BSB4 hdf5_file output_dir [options]\
                                     ")

    parser.add_argument("hdf5_file", help="network filename (with path)")
    parser.add_argument("sim_nio_name", help="FULL path of the folder containing nio files created during simulation")
    parser.add_argument("csv_suffix", help="suffix of the csv file -- without extention", default = '_fr_for_TF')
    parser.add_argument("--sim_type", help="name of the simulation in the hdf5 file", default='basal_activity')
    parser.add_argument("--freq_init", help="Initial frequency[Hz] for which I want compute the FR - MUST BE SAME OF SIM", type=int, default=4)
    parser.add_argument("--freq_last", help="Ending frequency[Hz] for which I want compute the FR - MUST BE SAME OF SIM", type=int, default=81)
    parser.add_argument("--df", help="frequency resolution - MUST BE SAME OF SIM", type=int, default=4)
    parser.add_argument("--t_tr", help="transient time to discared", type=float, default=200.)
    parser.add_argument("--t_stop", help="length of the sim", type=float, default=5000.)



    args = parser.parse_args()

    reco = args.hdf5_file
    sim_nio_path = args.sim_nio_name

    fmin = args.freq_init
    fmax = args.freq_last
    df = args.df

    snn_fr_outdir = reco+'_SNNoutput'

    csv_name_suffix = args.csv_suffix #without the extension - working frequency for numTF saved in these csv stored in the WORKING DIRECTORY (4 csv file)

    scaffold = from_storage(reco)
    mean_fr = {}
    std_fr = {}

    stims = np.arange(fmin,fmax,df)
    os.makedirs(snn_fr_outdir, exist_ok=True) #checking or creating the output_dir

    for i in range(fmin,fmax,df):
        nio_folder = './'+sim_nio_path+'/'+sim_nio_path+'_'+str(i)
        report = BasicSimulationReport(scaffold, simulation_name=args.sim_type, folder_nio=nio_folder, time_from=args.t_tr, time_to=args.t_stop)
        #report.print_report('sim_rec'+str(i)+'.pdf')
        table = SimResultsTable(fig_size=(10, 10), scaffold=scaffold, simulation_name=args.sim_type,
                                all_spikes=report.all_spikes, nb_neurons=report.nb_neurons, populations=report.populations,
                                dict_colors=report.colors, time_from=report.time_from, time_to=report.time_to)
        table.update()
        firing_rates = table.get_firing_rates()
        # For each cell in pop, it computes the average firing rate, table.get_firing_rates() provides the average FR for the sim.
	    # E.g., firing_rates['PC'] = (69), for each PC in scaffold it computes the avg FR
        #print(firing_rates)
        
        for pop in report.populations:
            np.save(snn_fr_outdir+'/'+str(i)+'_'+str(pop)+'_SNNsim.npy', firing_rates[pop])
            mean_fr[pop,i] = np.mean(firing_rates[pop]) # mean_fr is a dict with 2 keys (pop name, f) and the population mean computed from firing rates
            std_fr[pop,i] = np.std(firing_rates[pop])

    ## To save the mean firing rate and standard deviation stored in the dict above into a csv file (required for the numTF computation pipeline)
    mean_fr_pop = []
    std_fr_pop = []

    for pop in report.populations:
        print('Computing FR of ', pop)
        for i in stims:
            mean_fr_pop.append(mean_fr[pop, i])
            std_fr_pop.append(std_fr[pop,i])
            
        df = pd.DataFrame({
		        'stims': stims,
		        'media': mean_fr_pop,
		        'std': std_fr_pop
	        })
        name_csv = str(pop)+csv_name_suffix+'.csv'
        df.to_csv(name_csv, index=False, header=False)
        del(df)
        mean_fr_pop = []
        std_fr_pop = []
    
    print('SNN simulation saved in: ', os.getcwd())
    

if __name__ == "__main__":
    main()
