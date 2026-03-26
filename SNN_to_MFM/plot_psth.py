#from cerebellar_models.analysis.spiking_results import BasicSimulationReport
from cerebellum.analysis.spiking_results import (
    BasicSimulationReport
)
from bsb import from_storage
import numpy as np
import os
import matplotlib.pyplot as plt


path = "/home/bcc/projects/BSB4_demo/cerebellum_0.5.0/cerebellum"
sim_name = "basal_activity"
nio_fold = "./new_nios/nio_files_80"

# ================== PARAMETRI ==================
base_folder = '4Hz_mf_stim'

out_data_folder = '80Hz_mf_stim_psth_data'
out_plot_folder = '80Hz_mf_stim_psth'

nb_bins = 35
DO_PLOT = True

transient_ms = 10.0
color_dict = {
    'mossy_fibers': 'black',
    'granule_cell': 'red',
    'golgi_cell': 'blue',
    'purkinje_cell': 'green',
    'basket_cell': 'orange',
    'stellate_cell': 'orange'
}

os.makedirs(out_data_folder, exist_ok=True)
os.makedirs(out_plot_folder, exist_ok=True)

scaffold = from_storage(path+'/mouse_cerebellum.hdf5')
report = BasicSimulationReport(
    scaffold,
    simulation_name=sim_name,
    folder_nio=nio_fold#base_folder
)

time_from = report.time_from + transient_ms
time_to = report.time_to

bin_times = np.linspace(time_from, time_to, nb_bins)
bin_width_ms = bin_times[1] - bin_times[0]
bin_width_s = bin_width_ms / 1000.0
bin_centers = 0.5 * (bin_times[:-1] + bin_times[1:])

loc_spikes = report.get_filt_spikes()

for pop_idx, population in enumerate(report.populations):

    spike_times = loc_spikes[pop_idx].magnitude
    nb_neurons = report.nb_neurons[pop_idx]
    spike_times = spike_times[spike_times >= time_from]

    if nb_neurons == 0 or len(spike_times) == 0:
        psth = np.zeros(len(bin_times) - 1)
    else:
        weights = np.ones_like(spike_times) / (nb_neurons * bin_width_s)
        psth, _ = np.histogram(
            spike_times,
            bins=bin_times,
            weights=weights
        )
    np.savez(
        f'{out_data_folder}/{population}_psth.npz',
        psth=psth,
        bin_times=bin_times,
        bin_centers=bin_centers,
        bin_width_ms=bin_width_ms,
        time_from=time_from,
        time_to=time_to,
        population=population,
        nb_neurons=nb_neurons,
        transient_ms=transient_ms
    )

    if DO_PLOT:
        color = color_dict.get(population, 'gray')

        plt.figure(figsize=(8, 6))
        plt.bar(
            bin_centers,
            psth,
            width=bin_width_ms,
            color=color,
            alpha=0.7,
            align='center'
        )

        plt.title(f'PSTH {population}')
        plt.xlabel('Time [ms]')
        plt.ylabel('Firing rate [Hz]')
        plt.xlim([time_from, time_to])

        plt.tight_layout()
        plt.savefig(
            f'{out_plot_folder}/{population}_psth.png',
            dpi=300
        )
        plt.close()

    print(f'Processed {population}')

