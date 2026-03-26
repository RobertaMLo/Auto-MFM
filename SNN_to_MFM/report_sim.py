#from cerebellar_models.analysis.spiking_results import BasicSimulationReport
from cerebellum.analysis.spiking_results import (
    BasicSimulationReport
)

from bsb import from_storage
import numpy as np
import os

path = "/home/bcc/projects/BSB4_demo/cerebellum_0.5.0/cerebellum"
sim_name = "basal_activity"
nio_fold = "./new_nios/nio_files_4"

scaffold = from_storage(path+'/mouse_cerebellum.hdf5')
report = BasicSimulationReport(scaffold, simulation_name=sim_name, folder_nio=nio_fold)
report.print_report('40Hz_mf_stim.pdf')

nb_bins = 50   # time step dt= 10 ms
bin_times = np.linspace(report.time_from, report.time_to, nb_bins)
loc_spikes = report.get_filt_spikes()
os.makedirs(f'{report.folder_nio}_psth', exist_ok=True)
bin_width_ms = bin_times[1] - bin_times[0]
bin_width_s = bin_width_ms / 1000.0

out_dir = f'{report.folder_nio}_psth_data'
os.makedirs(out_dir, exist_ok=True)

for i, ct in enumerate(report.populations):
    times = loc_spikes[i].magnitude
    np.savez(
        f'{out_dir}/{ct}_psth_data.npz',
        spike_times=times,
        nb_neurons=report.nb_neurons[i],
        bin_times=bin_times,
        bin_width_ms=bin_width_ms,
        time_from=report.time_from,
        time_to=report.time_to,
        population=ct
    )
