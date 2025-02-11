from cerebellum.analysis.spiking_results import BasicSimulationReport, SimResultsTable
from bsb import from_storage
import numpy as np
import pandas as pd

reco = 'mouse_cerebellum.hdf5'

scaffold = from_storage(reco)
mean_fr = {}
std_fr = {}
nio_folder = './new_nios/nio_files_4'
stims = np.arange(4,81,4)

for i in range(4,81,4):
    nio_folder = './new_nios/nio_files_'+str(i)
    report = BasicSimulationReport(scaffold, simulation_name='basal_activity', folder_nio=nio_folder, time_from=200., time_to=5000.)
    #report.print_report('sim_rec'+str(i)+'.pdf')
    table = SimResultsTable(fig_size=(10, 10), scaffold=scaffold, simulation_name='basal_activity', 
                            all_spikes=report.all_spikes, nb_neurons=report.nb_neurons, populations=report.populations,
                            dict_colors=report.colors, time_from=report.time_from, time_to=report.time_to)
    table.update()
    firing_rates = table.get_firing_rates()
    for pop in report.populations:
    	mean_fr[pop,i] = np.mean(firing_rates[pop])
    	std_fr[pop,i] = np.std(firing_rates[pop])
    
mean_fr_pop = []
std_fr_pop = []
for pop in report.populations:
	for i in stims:
		mean_fr_pop.append(mean_fr[pop, i])
		std_fr_pop.append(std_fr[pop,i])
	
	df = pd.DataFrame({
		'stims': stims,
		'media': mean_fr_pop,
		'std': std_fr_pop	
	})
	name_csv = str(pop)+'_fr_for_TF_plus.csv'
	df.to_csv(name_csv, index=False, header=False)
	del(df)
	mean_fr_pop = []
	std_fr_pop = []
